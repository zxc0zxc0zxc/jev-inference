import json
from copy import deepcopy
from pathlib import Path

import pytest

from jev_inference._vendor.jevbench.tasks import Task
from jev_inference.jevbench_data import case_for, option_text, orders_for
from jev_inference.jevbench_runner import aggregate, order_metrics, outcome_for


def task(kind="choice"):
    return Task.from_dict(
        {
            "id": "example",
            "family": "policy",
            "state": {"request": "Run the task"},
            "question": {
                "type": kind,
                "instructions": "Follow this rubric",
                "criteria": {"accept": "Allowed", "reject": "Disallowed"},
            },
            "labels": ["accept", "reject"],
            "expected": "accept",
            "split": "public",
            "provenance": {"rationale": "secret gold rationale", "surface_answer": "reject"},
        }
    )


def test_model_prompt_excludes_gold_and_provenance():
    item = task()
    case = case_for(item, item.labels)
    assert "secret gold rationale" not in json.dumps(case)
    assert "expected" not in case
    assert "provenance" not in case
    assert case["choices"] == ["accept: Allowed", "reject: Disallowed"]


def test_rotation_preserves_labels_and_their_descriptions():
    item = task()
    orders = orders_for(item, 8)
    assert orders == [["accept", "reject"], ["reject", "accept"]]
    assert case_for(item, orders[1])["choices"] == ["reject: Disallowed", "accept: Allowed"]
    with pytest.raises(ValueError):
        case_for(item, ["accept", "accept"])


def test_noul_and_score_criteria_keep_canonical_meaning():
    item = task()
    item.question = {
        "type": "noul",
        "instructions": "Allowed?",
        "criteria": {"true": "Permitted", "false": "Forbidden"},
    }
    item.labels = ["no", "yes"]
    assert option_text(item, "yes") == "yes: Permitted"
    item.question = {"type": "score", "instructions": "Rate", "criteria": ["low", "high"]}
    item.labels = ["0", "1"]
    assert option_text(item, "1") == "1: high"


def row(prediction, probabilities=None):
    outcome = outcome_for(
        {"choice": prediction, **({"probs": probabilities} if probabilities else {})}, task()
    )
    return {
        "id": "example",
        "variant": 0,
        "choice": prediction,
        "outcome": outcome,
        "latency_ms_median": 10,
        "peak_allocated_mib": 100,
        "extra_peak_mib": 10,
        "runs": [{"hit_token_limit": False}],
    }


def test_label_only_has_no_fabricated_calibration():
    summary = aggregate([row("accept")], {"example": task()})
    assert summary["accuracy"] == 1
    assert summary["brier_mean"] is None
    assert summary["ece"] is None
    assert summary["calibration_n"] == 0


def test_calibration_uses_upstream_multiclass_brier_and_ece():
    summary = aggregate([row("accept", {"accept": 0.75, "reject": 0.25})], {"example": task()})
    assert summary["brier_mean"] == pytest.approx(0.125)
    assert summary["ece"]["ece"] == pytest.approx(0.25)
    assert summary["calibration_n"] == 1


def test_failed_outputs_count_as_incorrect_not_as_missing_tasks():
    summary = aggregate([row(None)], {"example": task()})
    assert summary["attempted"] == summary["scorable"] == 1
    assert summary["accuracy"] == 0
    assert summary["invalid_outputs"] == 1


def test_order_metrics_match_by_canonical_label_not_array_position():
    original = row("accept", {"accept": 0.75, "reject": 0.25})
    rotated = deepcopy(original)
    rotated["variant"] = 1
    rotated["outcome"]["probs"] = {"reject": 0.25, "accept": 0.75}
    metrics = order_metrics([original, rotated])
    assert metrics["decision_change_rate"] == 0
    assert metrics["probability_tv_mean"] == 0
    rotated.update(choice="reject")
    rotated["outcome"]["probs"] = {"accept": 0.25, "reject": 0.75}
    metrics = order_metrics([original, rotated])
    assert metrics["choice_flip_rate_valid_pairs"] == 1
    assert metrics["probability_tv_mean"] == pytest.approx(0.5)


def test_source_scoring_license_is_packaged():
    assert (Path(__file__).parents[1] / "src/jev_inference/_vendor/jevbench/LICENSE").exists()


def test_jevbench_has_sequence_baseline_without_changing_original_four():
    from jev_inference.benchmark import METHODS as original_methods
    from jev_inference.jevbench_runner import METHODS

    assert METHODS == (*original_methods, "sequence_likelihood")
    assert "sequence_likelihood" not in original_methods


def test_comparison_rejects_changed_inference_source():
    from jev_inference.jevbench_report import validate_comparison

    fields = (
        "dataset_sha256",
        "source",
        "source_sha256",
        "repeats",
        "permutations",
        "gpu",
        "dtype",
        "versions",
        "max_input_tokens",
        "warmup_runs_per_method",
        "batch_size",
        "concurrency",
        "generation_limits",
        "temperature",
    )
    result = {"metadata": dict.fromkeys(fields, "same"), "summary": {"labels": {}}}
    changed = deepcopy(result)
    changed["metadata"]["source_sha256"] = "different"
    with pytest.raises(ValueError, match="source_sha256"):
        validate_comparison([result, changed])


def test_host_metadata_handles_missing_nvidia_smi(monkeypatch):
    from jev_inference import jevbench_runner

    def missing(*args, **kwargs):
        raise FileNotFoundError("nvidia-smi unavailable")

    monkeypatch.setattr(jevbench_runner.subprocess, "run", missing)
    metadata = jevbench_runner.host_config()
    assert metadata["resource_limits_pinned"] is False
    assert metadata["gpu_telemetry_after"] is None


def test_cached_dataset_hash_mismatch_is_rejected_without_network(tmp_path, monkeypatch):
    from jev_inference import jevbench_data

    monkeypatch.setattr(jevbench_data, "FILES", {"easy": "a" * 64})
    (tmp_path / "easy.jsonl").write_text("modified public data")
    with pytest.raises(ValueError, match="source hash mismatch"):
        jevbench_data.load_public(str(tmp_path))


def test_failed_measurement_records_elapsed_time_and_memory(monkeypatch):
    from types import SimpleNamespace

    from jev_inference import benchmark

    clock = iter([2.0, 2.0125])
    monkeypatch.setattr(benchmark, "perf_counter", lambda: next(clock))
    cuda = SimpleNamespace(
        synchronize=lambda device: None,
        memory_allocated=lambda device: 10 * 2**20,
        reset_peak_memory_stats=lambda device: None,
        max_memory_allocated=lambda device: 15 * 2**20,
        max_memory_reserved=lambda device: 20 * 2**20,
    )
    engine = SimpleNamespace(
        torch=SimpleNamespace(cuda=cuda, OutOfMemoryError=MemoryError),
        model=SimpleNamespace(device="cuda"),
    )

    def fail():
        raise ValueError("context exceeds limit")

    result = benchmark.measure_operation(engine, fail, capture_errors=True)
    assert result["choice"] is None
    assert result["latency_ms"] == pytest.approx(12.5)
    assert result["peak_allocated_mib"] == 15
    assert result["extra_peak_mib"] == 5
    assert "context exceeds limit" in result["error"]


def test_report_supports_no_permutation_diagnostics():
    from jev_inference.jevbench_report import render

    summary = aggregate([row("accept")], {"example": task()})
    summary.update(order_sensitivity=order_metrics([row("accept")]), per_tier={}, per_type={})
    report = render(
        [
            {
                "metadata": {"model": "example/model"},
                "summary": {"generate_label": summary},
                "results": [],
            }
        ]
    )
    assert "example/model" in report
    assert "N/A" in report
    assert "N/A%" not in report
