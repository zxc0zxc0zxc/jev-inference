import math
import string
import threading
from time import perf_counter

from .prompts import label_prompt
from .schemas import ChoiceScore, DecisionRequest, DecisionResponse


def normalize(scores: list[float], temperature: float) -> list[float]:
    if not scores or not all(math.isfinite(value) for value in scores):
        raise ValueError("model returned non-finite or empty scores")
    maximum = max(scores)
    weights = [math.exp((value - maximum) / temperature) for value in scores]
    total = sum(weights)
    return [value / total for value in weights]


class DecisionEngine:
    def __init__(
        self, model: str, device: str = "auto", max_input_tokens: int = 4096, dtype: str = "auto"
    ):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        if dtype not in {"auto", "float16", "bfloat16", "float32"}:
            raise ValueError("unsupported model dtype")
        self.model_id = model
        self.max_input_tokens = max_input_tokens
        self._lock = threading.Lock()
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.model = AutoModelForCausalLM.from_pretrained(
            model,
            device_map=device,
            torch_dtype="auto" if dtype == "auto" else getattr(torch, dtype),
            trust_remote_code=False,
        ).eval()
        self.torch = torch
        context_limit = getattr(self.model.config, "max_position_embeddings", max_input_tokens)
        self.max_input_tokens = min(max_input_tokens, context_limit)

    def _token_ids(self, labels: list[str]) -> list[int]:
        ids = [self.tokenizer.encode(label, add_special_tokens=False) for label in labels]
        if any(len(tokens) != 1 for tokens in ids):
            raise ValueError("this tokenizer does not support the required single-token labels")
        result = [tokens[0] for tokens in ids]
        if len(set(result)) != len(result) or any(
            token in self.tokenizer.all_special_ids for token in result
        ):
            raise ValueError("choice labels must map to distinct, non-special tokens")
        return result

    def _inputs(self, prompt: str):
        if self.tokenizer.chat_template:
            prompt = self.tokenizer.apply_chat_template(
                [{"role": "user", "content": prompt}],
                tokenize=False,
                add_generation_prompt=True,
                enable_thinking=False,
            )
            inputs = self.tokenizer(prompt, return_tensors="pt", add_special_tokens=False)
        else:
            inputs = self.tokenizer(prompt, return_tensors="pt")
        if inputs["input_ids"].shape[1] > self.max_input_tokens:
            raise ValueError(f"prompt exceeds {self.max_input_tokens} tokens; reduce the input")
        return inputs.to(self.model.device)

    def _logits(self, prompt: str):
        inputs = self._inputs(prompt)
        with self.torch.inference_mode():
            output = self.model(**inputs, use_cache=False)
        return output.logits[0, -1].float()

    def _sequence_score(self, prompt: str, choice: str) -> float:
        inputs = self._inputs(prompt)
        prefix_length = inputs["input_ids"].shape[1]
        target_ids = self.tokenizer.encode(choice, add_special_tokens=False)
        if not target_ids:
            raise ValueError("choice must tokenize to at least one token")
        if prefix_length + len(target_ids) > self.max_input_tokens:
            raise ValueError(f"prompt and choice exceed {self.max_input_tokens} tokens")
        targets = self.torch.tensor([target_ids], device=self.model.device)
        input_ids = self.torch.cat([inputs["input_ids"], targets], dim=1)
        attention_mask = self.torch.ones_like(input_ids)
        with self.torch.inference_mode():
            output = self.model(input_ids=input_ids, attention_mask=attention_mask, use_cache=False)
            # Position t-1 predicts token t, including the first continuation token.
            logits = output.logits[0, prefix_length - 1 : -1].float()
            log_probs = logits.log_softmax(dim=-1)
            selected = log_probs.gather(1, targets[0].unsqueeze(1))
            return selected.mean().item()

    def _scores(self, request: DecisionRequest) -> list[float]:
        if request.mode == "sequence_likelihood":
            prompt = (
                "Choose the best option for the context below. Reply with the exact option text "
                "and no explanation.\n\n"
                f"Context:\n{request.context}\n\nAllowed choices:\n"
                + "\n".join(request.choices)
                + "\n\nAnswer:"
            )
            return [self._sequence_score(prompt, choice) for choice in request.choices]

        if request.mode == "labels":
            labels = list(string.ascii_uppercase[: len(request.choices)])
            token_ids = self._token_ids(labels)
            prompt = label_prompt(request.context, request.choices)
            return self._logits(prompt)[token_ids].tolist()
        yes_id, no_id = self._token_ids(["Yes", "No"])
        scores = []
        for choice in request.choices:
            prompt = (
                "Decide whether the proposed choice is appropriate for the context. "
                "Reply with exactly Yes or No and no explanation.\n\n"
                f"Context:\n{request.context}\n\nProposed choice:\n{choice}\n\nAnswer:"
            )
            logits = self._logits(prompt)
            scores.append((logits[yes_id] - logits[no_id]).item())
        return scores

    def decide(self, request: DecisionRequest) -> DecisionResponse:
        with self._lock:
            started = perf_counter()
            scores = self._scores(request)
            probabilities = normalize(scores, request.temperature)
            index = max(range(len(scores)), key=scores.__getitem__)
            return DecisionResponse(
                model=self.model_id,
                mode=request.mode,
                choice=request.choices[index],
                index=index,
                choices=[
                    ChoiceScore(choice=choice, score=score, probability=probability)
                    for choice, score, probability in zip(request.choices, scores, probabilities)
                ],
                latency_ms=(perf_counter() - started) * 1000,
                forward_passes=1 if request.mode == "labels" else len(request.choices),
            )
