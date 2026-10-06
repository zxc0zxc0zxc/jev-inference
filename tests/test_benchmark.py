import json
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

import pytest

from jev_inference.benchmark import (
    METHODS,
    dataset_hash,
    parse_generation,
    run_benchmark,
    summarize,
    validate_cases,
)

DATASET = Path(__file__).resolve().parents[1] / "benchmarks/classification30.json"


def test_dataset_has_30_valid_cases_and_balanced_answer_positions():
    cases = validate_cases(json.loads(DATASET.read_text()))
    assert len(cases) == 30
    assert all(
        case["context"].isascii() and all(choice.isascii() for choice in case["choices"])
        for case in cases
    )
    assert Counter(case["choices"].index(case["answer"]) for case in cases) == {0: 10, 1: 10, 2: 10}


@pytest.mark.parametrize(
    "text, expected",
    [(" B\n", "heal"), ("C.", "retreat"), ("A because it is best", None), ("Z", None)],
)
def test_label_parser_rejects_explanations_and_out_of_range_labels(text, expected):
    assert parse_generation(text, ["attack", "heal", "retreat"], "generate_label") == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ('{"choice":"heal"}', "heal"),
        ('{"choice":"invented"}', None),
        ('["heal"]', None),
        ("not JSON", None),
        ('{"choice": ["heal"]}', None),
    ],
)
def test_json_parser_requires_an_allowed_choice(text, expected):
    assert parse_generation(text, ["attack", "heal"], "generate_json") == expected


def test_invalid_expected_answer_is_rejected():
    cases = json.loads(DATASET.read_text())
    cases[0]["answer"] = "missing"
    with pytest.raises(ValueError, match="expected answer"):
        validate_cases(cases)


def test_duplicate_ids_are_rejected():
    cases = json.loads(DATASET.read_text())
    cases[1]["id"] = cases[0]["id"]
    with pytest.raises(ValueError, match="unique"):
        validate_cases(cases)


def test_hash_is_stable_across_dict_key_order_but_detects_content_changes():
    cases = json.loads(DATASET.read_text())
    reordered = [dict(reversed(list(case.items()))) for case in cases]
    assert dataset_hash(cases) == dataset_hash(reordered)
    reordered[0]["context"] += "!"
    assert dataset_hash(cases) != dataset_hash(reordered)


def test_summary_counts_invalid_outputs_as_wrong_and_uses_case_medians():
    rows = []
    for method in METHODS:
        for index in range(20):
            rows.append(
                {
                    "method": method,
                    "correct": index > 0,
                    "choice": "x" if index else None,
                    "stable_choice": True,
                    "runs": [{"hit_token_limit": False}],
                    "latency_ms_median": index + 1,
                    "peak_allocated_mib": 100,
                    "extra_peak_mib": 10,
                }
            )
    summary = summarize(rows)["labels"]
    assert summary["correct"] == 19
    assert summary["invalid_outputs"] == 1
    assert summary["latency_ms_median"] == 10.5
    assert summary["latency_ms_p95"] == 19


def test_benchmark_rejects_cpu_instead_of_reporting_fake_cuda_memory():
    engine = SimpleNamespace(model=SimpleNamespace(device=SimpleNamespace(type="cpu")))
    with pytest.raises(ValueError, match="CUDA"):
        run_benchmark(engine, json.loads(DATASET.read_text()))


def test_measure_synchronizes_gpu_and_resets_memory_peak(monkeypatch):
    from jev_inference import benchmark

    events = []
    cuda = SimpleNamespace(
        synchronize=lambda device: events.append("sync"),
        memory_allocated=lambda device: 100 * 2**20,
        reset_peak_memory_stats=lambda device: events.append("reset"),
        max_memory_allocated=lambda device: 140 * 2**20,
        max_memory_reserved=lambda device: 200 * 2**20,
    )
    clock = iter([10, 10.05])
    monkeypatch.setattr(benchmark, "perf_counter", lambda: next(clock))
    monkeypatch.setattr(benchmark.gc, "collect", lambda: None)

    def infer(*args):
        events.append("infer")
        return {"choice": "a"}

    monkeypatch.setattr(benchmark, "run_choice", infer)
    engine = SimpleNamespace(
        torch=SimpleNamespace(cuda=cuda), model=SimpleNamespace(device="cuda:0")
    )
    result = benchmark.measure(engine, {}, "labels")
    assert events == ["sync", "reset", "infer", "sync"]
    assert result["latency_ms"] == pytest.approx(50)
    assert result["peak_allocated_mib"] == 140
    assert result["extra_peak_mib"] == 40


def test_readme_report_update_preserves_surrounding_content_and_is_idempotent():
    from jev_inference.benchmark_report import END, START, update_readme

    original = f"Intro\n{START}\nold\n{END}\nExisting documentation\n"
    updated = update_readme(original, "new results")
    assert updated == f"Intro\n{START}\nnew results\n{END}\nExisting documentation\n"
    assert update_readme(updated, "new results") == updated
    with pytest.raises(ValueError, match="incomplete"):
        update_readme(f"Intro {START}", "results")


def test_model_report_names_keep_existing_results_separate():
    from jev_inference.benchmark_report import full_report, report_path

    assert report_path(Path("docs/benchmark-results.json")) == Path("docs/benchmark-report.md")
    new_path = Path("docs/benchmark-results-qwen2.5-1.5b.json")
    assert report_path(new_path) == Path("docs/benchmark-report-qwen2.5-1.5b.md")
    saved = json.loads((DATASET.parents[1] / "docs/benchmark-results.json").read_text())
    report = full_report(saved, new_path.name)
    assert f"]({new_path.name})" in report


def test_comparison_rejects_different_datasets_or_measurement_settings():
    from copy import deepcopy

    from jev_inference.benchmark_report import validate_comparison

    reference = json.loads((DATASET.parents[1] / "docs/benchmark-results.json").read_text())
    other = deepcopy(reference)
    with pytest.raises(ValueError, match="different model"):
        validate_comparison([reference, other])
    other["metadata"]["model"] = "other-model"
    validate_comparison([reference, other])
    other["metadata"]["repeats"] = 1
    with pytest.raises(ValueError, match="repeats"):
        validate_comparison([reference, other])
    other = deepcopy(reference)
    other["metadata"]["model"] = "other-model"
    other["dataset"][0]["context"] += "changed"
    with pytest.raises(ValueError, match="datasets"):
        validate_comparison([reference, other])


def test_modal_benchmark_transmits_requested_model_explicitly(tmp_path, monkeypatch):
    from jev_inference import benchmark_modal

    dataset = tmp_path / "cases.json"
    dataset.write_text(DATASET.read_text())
    captured = {}

    def remote(cases, repeats, model, dtype):
        captured.update(model=model, repeats=repeats, count=len(cases), dtype=dtype)
        return {}

    monkeypatch.setattr(benchmark_modal, "model_id", "Qwen/Qwen2.5-1.5B-Instruct")
    monkeypatch.setattr(benchmark_modal, "evaluate", SimpleNamespace(remote=remote))
    monkeypatch.setattr("jev_inference.benchmark.save_results", lambda *args: None)
    benchmark_modal.main(str(dataset), str(tmp_path / "results.json"), 3, "float16")
    assert captured == {
        "model": "Qwen/Qwen2.5-1.5B-Instruct",
        "repeats": 3,
        "count": 30,
        "dtype": "float16",
    }


@pytest.mark.parametrize("module_name", ["cli", "benchmark_cli"])
def test_modal_launchers_accept_arbitrary_hugging_face_model_ids(monkeypatch, module_name):
    import importlib

    module = importlib.import_module(f"jev_inference.{module_name}")
    captured = {}

    def execute(command, env, check):
        captured.update(model=env["JEV_MODEL"], command=command)
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(
        module.sys, "argv", ["run.py", "--modal", "--model", "example/custom-causal-model"]
    )
    monkeypatch.setattr(module.subprocess, "run", execute)
    with pytest.raises(SystemExit) as result:
        module.main()
    assert result.value.code == 0
    assert captured["model"] == "example/custom-causal-model"
