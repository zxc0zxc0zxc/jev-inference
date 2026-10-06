"""Pinned public JevBench data; model inputs exclude all provenance and gold fields."""

import hashlib
import json
import urllib.request
from pathlib import Path

from ._vendor.jevbench.tasks import Task

REVISION = "bb05a335bc809e61b20c0f745d25499a82b326fc"
SOURCE = "https://github.com/fstandhartinger/jevbench"
FILES = {
    "easy": "231df3c2c8e88a1a8c137ebe85de96ba70fabd330849098ac7b3c52c70b7172b",
    "original": "5c2414edb3006b8bfcb70fda433f0f9ca015759433849f8d3104328a1f7c4180",
    "hard": "89e9e6becb33ed88c1de7d42dcc87531b2fb64cfaef4e1986faf7c37b3f80ebb",
}


def load_public(directory: str = ".cache/jevbench-public") -> tuple[list[dict], dict]:
    root = Path(directory)
    root.mkdir(parents=True, exist_ok=True)
    records = []
    for tier, expected_hash in FILES.items():
        path = root / f"{tier}.jsonl"
        if not path.exists():
            url = f"https://raw.githubusercontent.com/fstandhartinger/jevbench/{REVISION}/datasets/public/{tier}.jsonl"
            with urllib.request.urlopen(url, timeout=60) as response:
                data = response.read()
            if hashlib.sha256(data).hexdigest() != expected_hash:
                raise ValueError(f"source hash mismatch for {tier}")
            path.write_bytes(data)
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected_hash:
            raise ValueError(f"source hash mismatch for {tier}")
        for line in path.read_text().splitlines():
            if line.strip():
                record = json.loads(line)
                task = Task.from_dict(record)
                if task.split != "public":
                    raise ValueError("only public JevBench records may be evaluated")
                records.append({"tier": tier, "task": record})
    if len({record["task"]["id"] for record in records}) != len(records):
        raise ValueError("duplicate JevBench task IDs")
    return records, {
        "repository": SOURCE,
        "revision": REVISION,
        "file_sha256": FILES,
        "scope": "231 published v1.2 easy/original/hard records; no sealed data",
    }


def option_text(task: Task, label: str) -> str:
    criteria = task.question.get("criteria")
    if task.question["type"] == "noul":
        description = (criteria or {}).get("true" if label == "yes" else "false")
    elif task.question["type"] == "score":
        description = criteria[int(label)] if criteria else None
    else:
        description = criteria.get(label) if isinstance(criteria, dict) else None
    if description is None:
        return label
    text = (
        description if isinstance(description, str) else json.dumps(description, ensure_ascii=False)
    )
    return f"{label}: {text}"


def case_for(task: Task, order: list[str]) -> dict:
    if len(order) != len(task.labels) or set(order) != set(task.labels):
        raise ValueError("permutation must preserve the canonical label set")
    state = (
        task.state if isinstance(task.state, str) else json.dumps(task.state, ensure_ascii=False)
    )
    context = (
        f"State:\n{state}\n\nQuestion type: {task.question['type']}\n"
        f"Instructions:\n{task.question['instructions']}"
    )
    return {
        "id": task.id,
        "context": context,
        "choices": [option_text(task, label) for label in order],
        "canonical_labels": order,
    }


def orders_for(task: Task, permutations: int) -> list[list[str]]:
    # Canonical order is never overwritten. Cyclic rotations contain no gold-dependent selection.
    return [
        task.labels[shift:] + task.labels[:shift]
        for shift in range(min(permutations + 1, len(task.labels)))
    ]
