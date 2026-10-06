import logging
import os
import secrets

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .schemas import DecisionRequest, DecisionResponse

logger = logging.getLogger(__name__)


def create_app(engine, api_key: str | None = None) -> FastAPI:
    api_key = api_key if api_key is not None else os.environ.get("JEV_API_KEY")
    app = FastAPI(title="Jev Inference", version="0.1.0")
    bearer = HTTPBearer(auto_error=False)

    def authorize(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)):
        if api_key and (
            credentials is None
            or not secrets.compare_digest(credentials.credentials.encode(), api_key.encode())
        ):
            raise HTTPException(status_code=401, detail="Invalid API key")

    @app.get("/health")
    def health():
        return {"status": "ready", "model": engine.model_id}

    @app.post("/decide", response_model=DecisionResponse, dependencies=[Depends(authorize)])
    def decide(request: DecisionRequest):
        try:
            return engine.decide(request)
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error
        except Exception as error:
            logger.exception("Decision inference failed")
            raise HTTPException(status_code=503, detail="Inference failed") from error

    return app
