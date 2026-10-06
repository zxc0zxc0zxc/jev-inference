import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from .benchmark import save_results, validate_cases


def main():
    parser = argparse.ArgumentParser(description="Benchmark generation versus logits on a CUDA GPU")
    parser.add_argument("--model", default="Qwen/Qwen2.5-0.5B-Instruct")
    parser.add_argument(
        "--dtype", choices=["auto", "float16", "bfloat16", "float32"], default="auto"
    )
    parser.add_argument("--dataset", default="benchmarks/classification30.json")
    parser.add_argument("--output", default="docs/benchmark-results.json")
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--modal", action="store_true")
    parser.add_argument("--gpu", default="T4")
    parser.add_argument("--secret", help="Modal Secret for private HF models")
    parser.add_argument("--device", default="cuda")
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error("--repeats must be positive")
    cases = validate_cases(json.loads(Path(args.dataset).read_text()))
    if args.modal:
        environment = os.environ.copy()
        environment.update(
            JEV_MODEL=args.model,
            JEV_DTYPE=args.dtype,
            JEV_GPU=args.gpu,
            JEV_MODAL_SECRET=args.secret or "",
        )
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "modal",
                "run",
                "-m",
                "jev_inference.benchmark_modal",
                "--dtype",
                args.dtype,
                "--dataset",
                args.dataset,
                "--output",
                args.output,
                "--repeats",
                str(args.repeats),
            ],
            env=environment,
            check=False,
        )
        raise SystemExit(result.returncode)
    from .benchmark import run_benchmark
    from .engine import DecisionEngine

    save_results(
        run_benchmark(
            DecisionEngine(args.model, args.device, dtype=args.dtype), cases, args.repeats
        ),
        args.output,
    )
