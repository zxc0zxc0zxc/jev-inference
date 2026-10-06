"""Warmed, single-GPU classification benchmark; no HTTP latency included."""

import gc
import hashlib
import json
import math
import platform
import re
import statistics
import string
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path
from time import perf_counter

from .prompts import label_prompt
from .schemas import DecisionRequest

METHODS = ("generate_label", "generate_json", "labels", "independent")


def validate_cases(cases: list[dict]) -> list[dict]:
    if not cases:
        raise ValueError("benchmark dataset must not be empty")
    ids = set()
    for case in cases:
        DecisionRequest(context=case["context"], choices=case["choices"])
        if not isinstance(case["id"], str) or not case["id"] or case["id"] in ids:
            raise ValueError("case IDs must be nonempty and unique")
        if not isinstance(case["category"], str) or not case["category"]:
            raise ValueError("category must be nonempty")
        if case["answer"] not in case["choices"]:
            raise ValueError("expected answer must be an allowed choice")
        ids.add(case["id"])
    return cases


def dataset_hash(cases: list[dict]) -> str:
    canonical = json.dumps(cases, sort_keys=True, ensure_ascii=False).encode()
    return hashlib.sha256(canonical).hexdigest()


def parse_generation(text: str, choices: list[str], method: str) -> str | None:
    if method == "generate_label":
        match = re.fullmatch(r"([A-Z])[.)]?", text.strip())
        if match and (index := string.ascii_uppercase.index(match[1])) < len(choices):
            return choices[index]
        return None
    if method != "generate_json":
        raise ValueError(f"unknown generation method: {method}")
    try:
        result = json.loads(text)
    except json.JSONDecodeError:
        return None
    if isinstance(result, dict) and result.get("choice") in choices:
        return result["choice"]
    return None


def json_prompt(context: str, choices: list[str]) -> str:
    return (
        "Choose the best option for the context below. Reply only with a JSON object "
        'of the form {"choice": "exact option text"}, without explanation or markdown.\n\n'
        f"Context:\n{context}\n\nAllowed choices:\n"
        f"{json.dumps(choices, ensure_ascii=False)}\n\nJSON:"
    )


def generate_choice(engine, case: dict, method: str) -> dict:
    from transformers import GenerationConfig

    prompt = (
        label_prompt(case["context"], case["choices"])
        if method == "generate_label"
        else json_prompt(case["context"], case["choices"])
    )
    inputs = engine._inputs(prompt)
    limit = 16 if method == "generate_label" else 64
    eos = engine.model.generation_config.eos_token_id
    config = GenerationConfig(
        do_sample=False,
        num_beams=1,
        max_new_tokens=limit,
        use_cache=True,
        eos_token_id=eos,
        pad_token_id=engine.tokenizer.pad_token_id,
    )
    with engine.torch.inference_mode():
        output = engine.model.generate(**inputs, generation_config=config)
    tokens = output[0, inputs["input_ids"].shape[1] :].tolist()
    text = engine.tokenizer.decode(tokens, skip_special_tokens=True)
    eos_ids = eos if isinstance(eos, list) else [eos]
    return {
        "choice": parse_generation(text, case["choices"], method),
        "raw_output": text,
        "generated_tokens": len(tokens),
        "hit_token_limit": len(tokens) >= limit and tokens[-1] not in eos_ids,
        "input_tokens": inputs["input_ids"].shape[1],
    }


def run_choice(engine, case: dict, method: str) -> dict:
    if method.startswith("generate_"):
        return generate_choice(engine, case, method)
    result = engine.decide(
        DecisionRequest(context=case["context"], choices=case["choices"], mode=method)
    )
    return {
        "choice": result.choice,
        "probabilities": [item.probability for item in result.choices],
        "generated_tokens": 0,
        "hit_token_limit": False,
        "forward_passes": result.forward_passes,
    }


def measure(engine, case: dict, method: str) -> dict:
    return measure_operation(engine, lambda: run_choice(engine, case, method))


def measure_operation(engine, operation, capture_errors: bool = False) -> dict:
    cuda = engine.torch.cuda
    device = engine.model.device
    gc.collect()
    cuda.synchronize(device)
    baseline = cuda.memory_allocated(device)
    cuda.reset_peak_memory_stats(device)
    started = perf_counter()
    try:
        result = operation()
    except (ValueError, engine.torch.OutOfMemoryError) as error:
        if not capture_errors:
            raise
        result = {"choice": None, "error": f"{type(error).__name__}: {error}"}
    cuda.synchronize(device)
    elapsed_ms = (perf_counter() - started) * 1000
    peak = cuda.max_memory_allocated(device)
    return {
        **result,
        "latency_ms": elapsed_ms,
        "baseline_allocated_mib": baseline / 2**20,
        "peak_allocated_mib": peak / 2**20,
        "extra_peak_mib": (peak - baseline) / 2**20,
        "peak_reserved_mib": cuda.max_memory_reserved(device) / 2**20,
    }


def summarize(rows: list[dict]) -> dict:
    summary = {}
    for method in METHODS:
        selected = [row for row in rows if row["method"] == method]
        times = sorted(row["latency_ms_median"] for row in selected)
        count = len(selected)
        summary[method] = {
            "correct": sum(row["correct"] for row in selected),
            "total": count,
            "accuracy": sum(row["correct"] for row in selected) / count,
            "invalid_outputs": sum(row["choice"] is None for row in selected),
            "unstable_cases": sum(not row["stable_choice"] for row in selected),
            "token_limit_cases": sum(
                any(run["hit_token_limit"] for run in row["runs"]) for row in selected
            ),
            "latency_ms_median": statistics.median(times),
            "latency_ms_p95": times[math.ceil(0.95 * count) - 1],
            "max_peak_allocated_mib": max(row["peak_allocated_mib"] for row in selected),
            "max_extra_peak_mib": max(row["extra_peak_mib"] for row in selected),
        }
    return summary


def run_benchmark(engine, cases: list[dict], repeats: int = 3) -> dict:
    cases = validate_cases(cases)
    if repeats < 1:
        raise ValueError("repeats must be positive")
    device = engine.model.device
    if device.type != "cuda" or {p.device for p in engine.model.parameters()} != {device}:
        raise ValueError("benchmark requires a model entirely on one CUDA GPU")
    for method in METHODS:
        for _ in range(2):
            run_choice(engine, cases[0], method)
    engine.torch.cuda.synchronize(device)
    rows = []
    for case_index, case in enumerate(cases):
        runs = {method: [] for method in METHODS}
        for repeat in range(repeats):
            offset = (case_index + repeat) % len(METHODS)
            order = METHODS[offset:] + METHODS[:offset]
            for method in order:
                runs[method].append(measure(engine, case, method))
        for method in METHODS:
            measurements = runs[method]
            choice = measurements[0]["choice"]
            rows.append(
                {
                    "id": case["id"],
                    "category": case["category"],
                    "method": method,
                    "expected": case["answer"],
                    "choice": choice,
                    "correct": choice == case["answer"],
                    "stable_choice": all(run["choice"] == choice for run in measurements),
                    "latency_ms_median": statistics.median(
                        run["latency_ms"] for run in measurements
                    ),
                    "peak_allocated_mib": max(run["peak_allocated_mib"] for run in measurements),
                    "extra_peak_mib": max(run["extra_peak_mib"] for run in measurements),
                    "runs": measurements,
                }
            )
        print(f"[{case_index + 1}/{len(cases)}] {case['id']}", flush=True)
    properties = engine.torch.cuda.get_device_properties(device)
    return {
        "metadata": {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "model": engine.model_id,
            "model_revision": getattr(engine.model.config, "_commit_hash", None),
            "dataset_sha256": dataset_hash(cases),
            "cases": len(cases),
            "repeats": repeats,
            "warmup_runs_per_method": 2,
            "gpu": properties.name,
            "gpu_total_mib": properties.total_memory / 2**20,
            "dtype": str(engine.model.dtype),
            "python": platform.python_version(),
            "versions": {name: version(name) for name in ("torch", "transformers", "accelerate")},
            "cuda": engine.torch.version.cuda,
            "max_input_tokens": engine.max_input_tokens,
            "timing": "tokenization + model + decode/normalization; CUDA synchronized; no HTTP",
            "memory": "PyTorch CUDA allocator only; weights included; MiB = 2^20 bytes",
            "generation_limits": {"generate_label": 16, "generate_json": 64},
            "method_order": "rotated by case and repeat",
            "greedy": True,
            "accuracy_rule": "first repetition per case; invalid output counts as incorrect",
        },
        "dataset": cases,
        "summary": summarize(rows),
        "results": rows,
    }


def save_results(result: dict, output: str):
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(result["summary"], indent=2), flush=True)
    print(f"Saved {path}", flush=True)
