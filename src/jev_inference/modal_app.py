"""Modal application definition, configured by the launcher environment."""

import os

import modal

model_id = os.environ.get("JEV_MODEL", "Qwen/Qwen2.5-0.5B-Instruct")
model_dtype = os.environ.get("JEV_DTYPE", "auto")
max_tokens = int(os.environ.get("JEV_MAX_INPUT_TOKENS", "4096"))
secret_name = os.environ.get("JEV_MODAL_SECRET")
app = modal.App(os.environ.get("JEV_APP_NAME", "jev-inference"))
image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "torch>=2.4,<3",
        "transformers>=4.51,<5",
        "accelerate>=1,<2",
        "fastapi>=0.115,<1",
        "pydantic>=2.8,<3",
    )
    .env(
        {
            "HF_HOME": "/cache/huggingface",
            "JEV_MODEL": model_id,
            "JEV_DTYPE": model_dtype,
            "JEV_MAX_INPUT_TOKENS": str(max_tokens),
        }
    )
    .add_local_python_source("jev_inference")
)
cache = modal.Volume.from_name("jev-inference-model-cache", create_if_missing=True)


@app.function(
    image=image,
    gpu=os.environ.get("JEV_GPU", "T4"),
    volumes={"/cache": cache},
    secrets=[modal.Secret.from_name(secret_name)] if secret_name else [],
    timeout=900,
    scaledown_window=300,
    max_containers=1,
)
@modal.asgi_app()
def api():
    from jev_inference.api import create_app
    from jev_inference.engine import DecisionEngine

    engine = DecisionEngine(model_id, max_input_tokens=max_tokens, dtype=model_dtype)
    cache.commit()
    return create_app(engine)
