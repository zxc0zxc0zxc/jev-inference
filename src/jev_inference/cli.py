import argparse
import os
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description="Serve choices from causal LM logits")
    parser.add_argument("--model", default="Qwen/Qwen2.5-0.5B-Instruct")
    parser.add_argument(
        "--dtype", choices=["auto", "float16", "bfloat16", "float32"], default="auto"
    )
    parser.add_argument("--modal", action="store_true", help="Deploy a persistent Modal API")
    parser.add_argument("--gpu", default="T4", help="Modal GPU type")
    parser.add_argument("--app-name", default="jev-inference")
    parser.add_argument("--secret", help="Modal Secret with JEV_API_KEY and/or HF_TOKEN")
    parser.add_argument("--device", default="auto", help="Local device: auto, cpu, cuda, mps")
    parser.add_argument("--max-input-tokens", type=int, default=4096)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    if args.max_input_tokens < 1:
        parser.error("--max-input-tokens must be positive")
    if args.modal:
        environment = os.environ.copy()
        environment.update(
            JEV_MODEL=args.model,
            JEV_DTYPE=args.dtype,
            JEV_GPU=args.gpu,
            JEV_APP_NAME=args.app_name,
            JEV_MAX_INPUT_TOKENS=str(args.max_input_tokens),
            JEV_MODAL_SECRET=args.secret or "",
        )
        result = subprocess.run(
            [sys.executable, "-m", "modal", "deploy", "-m", "jev_inference.modal_app"],
            env=environment,
            check=False,
        )
        raise SystemExit(result.returncode)
    import uvicorn

    from .api import create_app
    from .engine import DecisionEngine

    engine = DecisionEngine(args.model, args.device, args.max_input_tokens, args.dtype)
    uvicorn.run(create_app(engine), host=args.host, port=args.port)
