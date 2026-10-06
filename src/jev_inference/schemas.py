from typing import Literal

from pydantic import BaseModel, Field, field_validator


class DecisionRequest(BaseModel):
    context: str = Field(min_length=1, max_length=32000)
    choices: list[str] = Field(min_length=2, max_length=26)
    mode: Literal["labels", "independent", "sequence_likelihood"] = "labels"
    temperature: float = Field(default=1.0, gt=0, le=100, allow_inf_nan=False)

    @field_validator("context")
    @classmethod
    def nonempty_context(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("context must contain text")
        return value

    @field_validator("choices")
    @classmethod
    def valid_choices(cls, values: list[str]) -> list[str]:
        if any(not value.strip() or len(value) > 2000 for value in values):
            raise ValueError("each choice must contain 1–2000 characters")
        if len(set(values)) != len(values):
            raise ValueError("choices must be unique")
        return values


class ChoiceScore(BaseModel):
    choice: str
    score: float
    probability: float


class DecisionResponse(BaseModel):
    model: str
    mode: str
    choice: str
    index: int
    choices: list[ChoiceScore]
    latency_ms: float
    forward_passes: int
