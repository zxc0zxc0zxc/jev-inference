import math
import threading
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from jev_inference.api import create_app
from jev_inference.engine import DecisionEngine, normalize
from jev_inference.schemas import DecisionRequest


class FakeEngine(DecisionEngine):
    def __init__(self):
        self.model_id = "fake"
        self._lock = threading.Lock()

    def _scores(self, request):
        return [float(len(choice)) for choice in request.choices]


@pytest.fixture
def client():
    return TestClient(create_app(FakeEngine(), api_key="test-key"))


def test_distribution_is_stable_for_large_logits():
    probabilities = normalize([10000, 10001], 1)
    assert sum(probabilities) == pytest.approx(1)
    assert probabilities[1] == pytest.approx(0.7310585786)


@pytest.mark.parametrize("scores", [[], [math.nan], [math.inf]])
def test_invalid_model_scores_are_rejected(scores):
    with pytest.raises(ValueError):
        normalize(scores, 1)


def test_api_returns_choice_and_normalized_distribution(client):
    response = client.post(
        "/decide",
        headers={"Authorization": "Bearer test-key"},
        json={"context": "pick", "choices": ["a", "long"]},
    )
    assert response.status_code == 200
    result = response.json()
    assert result["choice"] == "long"
    assert result["index"] == 1
    assert result["forward_passes"] == 1
    assert sum(item["probability"] for item in result["choices"]) == pytest.approx(1)


@pytest.mark.parametrize(
    "payload",
    [
        {"context": " ", "choices": ["a", "b"]},
        {"context": "x", "choices": ["a", "a"]},
        {"context": "x", "choices": ["a"]},
        {"context": "x", "choices": ["a", "b"], "temperature": 0},
        {"context": "x", "choices": ["a", "b"], "mode": "generate"},
    ],
)
def test_invalid_requests_return_422(client, payload):
    assert (
        client.post(
            "/decide", json=payload, headers={"Authorization": "Bearer test-key"}
        ).status_code
        == 422
    )


def test_api_requires_configured_key(client):
    assert client.post("/decide", json={"context": "x", "choices": ["a", "b"]}).status_code == 401
    assert client.get("/health").json()["status"] == "ready"


def test_independent_scoring_does_not_include_other_options():
    engine = FakeEngine()
    engine._token_ids = lambda labels: [0, 1]
    prompts = []

    class Logits:
        def __getitem__(self, index):
            return self

        def __sub__(self, other):
            return self

        def item(self):
            return 1.0

    def logits(prompt):
        prompts.append(prompt)
        return Logits()

    engine._logits = logits
    request = DecisionRequest(context="state", choices=["attack", "heal"], mode="independent")
    scores = DecisionEngine._scores(engine, request)
    assert scores == [1, 1]
    assert "heal" not in prompts[0]
    assert "attack" not in prompts[1]
    first = prompts.copy()
    prompts.clear()
    DecisionEngine._scores(engine, request.model_copy(update={"choices": ["heal", "attack"]}))
    assert prompts == first[::-1]


def test_multi_token_label_is_rejected():
    engine = FakeEngine()
    engine.tokenizer = SimpleNamespace(encode=lambda *args, **kwargs: [1, 2])
    with pytest.raises(ValueError, match="single-token"):
        engine._token_ids(["A", "B"])


def test_inference_errors_are_reported_without_internal_details(client):
    engine = FakeEngine()

    def fail(request):
        raise RuntimeError("private detail")

    engine.decide = fail
    response = TestClient(create_app(engine, api_key="")).post(
        "/decide", json={"context": "x", "choices": ["a", "b"]}
    )
    assert response.status_code == 503
    assert "private detail" not in response.text


def test_sequence_likelihood_scores_full_text_without_label_tokens():
    engine = FakeEngine()
    seen = []
    engine._sequence_score = lambda prompt, choice: seen.append((prompt, choice)) or -len(choice)
    engine._token_ids = lambda _: pytest.fail("sequence scoring must not require label tokens")
    request = DecisionRequest(
        context="state",
        choices=["multi token answer", "another answer"],
        mode="sequence_likelihood",
    )
    assert DecisionEngine._scores(engine, request) == [-18, -14]
    assert [choice for _, choice in seen] == request.choices
    assert seen[0][0] == seen[1][0]
    assert "multi token answer" in seen[0][0]


def test_sequence_likelihood_rejects_combined_context_overflow_before_forward():
    engine = FakeEngine()
    engine.max_input_tokens = 4
    engine.model = SimpleNamespace(device="cpu")
    engine._inputs = lambda _: {"input_ids": SimpleNamespace(shape=(1, 3))}
    engine.tokenizer = SimpleNamespace(encode=lambda *args, **kwargs: [7, 8])
    with pytest.raises(ValueError, match="prompt and choice exceed"):
        engine._sequence_score("context", "two tokens")


def test_sequence_likelihood_rejects_empty_tokenization():
    engine = FakeEngine()
    engine.max_input_tokens = 4
    engine._inputs = lambda _: {"input_ids": SimpleNamespace(shape=(1, 3))}
    engine.tokenizer = SimpleNamespace(encode=lambda *args, **kwargs: [])
    with pytest.raises(ValueError, match="at least one token"):
        engine._sequence_score("context", "text")


def test_api_accepts_sequence_likelihood_mode(client):
    response = client.post(
        "/decide",
        headers={"Authorization": "Bearer test-key"},
        json={
            "context": "state",
            "choices": ["first option", "second option"],
            "mode": "sequence_likelihood",
        },
    )
    assert response.status_code == 200
    assert response.json()["forward_passes"] == 2


def test_sequence_likelihood_uses_shifted_positions_and_every_target_token():
    from contextlib import nullcontext

    class Tensor:
        def __init__(self, values):
            self.values = values
            self.shape = (len(values), len(values[0]))

        def __getitem__(self, key):
            if isinstance(key, tuple):
                batch, positions = key
                return Matrix(self.values[batch][positions])
            return Vector(self.values[key])

    class Vector:
        def __init__(self, values):
            self.values = values

        def unsqueeze(self, _):
            return self

    class Matrix:
        def __init__(self, values):
            self.values = values

        def float(self):
            return self

        def log_softmax(self, dim):
            assert dim == -1
            return Matrix(
                [
                    [value - math.log(sum(math.exp(v) for v in row)) for value in row]
                    for row in self.values
                ]
            )

        def gather(self, dim, targets):
            assert dim == 1
            assert len(self.values) == len(targets.values)
            return Matrix([[row[token]] for row, token in zip(self.values, targets.values)])

        def mean(self):
            return SimpleNamespace(
                item=lambda: sum(row[0] for row in self.values) / len(self.values)
            )

    calls = []

    def forward(**kwargs):
        calls.append(kwargs)
        # Prefix has two tokens. Its final position predicts target 1, then target 2.
        return SimpleNamespace(logits=Tensor([[[9, 0, 0], [0, 2, 0], [0, 0, 3], [9, 0, 0]]]))

    engine = FakeEngine()
    engine.max_input_tokens = 8
    engine._inputs = lambda _: {"input_ids": Tensor([[0, 0]])}
    engine.tokenizer = SimpleNamespace(encode=lambda *args, **kwargs: [1, 2])
    engine.model = SimpleNamespace(device="cpu")

    class Model:
        device = "cpu"

        def __call__(self, **kwargs):
            return forward(**kwargs)

    engine.model = Model()
    engine.torch = SimpleNamespace(
        tensor=lambda values, **kwargs: Tensor(values),
        cat=lambda tensors, dim: Tensor([tensors[0].values[0] + tensors[1].values[0]]),
        ones_like=lambda tensor: Tensor([[1] * tensor.shape[1]]),
        inference_mode=nullcontext,
    )
    expected = ((2 - math.log(math.exp(2) + 2)) + (3 - math.log(math.exp(3) + 2))) / 2
    assert engine._sequence_score("context", "two tokens") == pytest.approx(expected)
    assert len(calls) == 1
    assert calls[0]["input_ids"].values == [[0, 0, 1, 2]]
    assert calls[0]["use_cache"] is False


@pytest.mark.parametrize("dtype", ["auto", "float16", "bfloat16", "float32"])
def test_model_dtype_is_explicit_and_remote_code_remains_disabled(monkeypatch, dtype):
    import sys

    captured = {}
    torch = SimpleNamespace(float16=object(), bfloat16=object(), float32=object())
    model = SimpleNamespace(config=SimpleNamespace(max_position_embeddings=8192))
    model.eval = lambda: model

    def load_model(model_id, **kwargs):
        captured.update(kwargs)
        return model

    monkeypatch.setitem(sys.modules, "torch", torch)
    monkeypatch.setitem(
        sys.modules,
        "transformers",
        SimpleNamespace(
            AutoModelForCausalLM=SimpleNamespace(from_pretrained=load_model),
            AutoTokenizer=SimpleNamespace(from_pretrained=lambda _: object()),
        ),
    )
    DecisionEngine("example/model", device="cuda", dtype=dtype)
    assert captured["torch_dtype"] == ("auto" if dtype == "auto" else getattr(torch, dtype))
    assert captured["trust_remote_code"] is False
