## JevBench public-subset diagnostics

Public tasks from [JevBench](https://github.com/fstandhartinger/jevbench), pinned to `bb05a335bc809e61b20c0f745d25499a82b326fc`. This is a public-subset experiment, not an official leaderboard result. Gold answers and provenance never enter prompts.

| Model | Method | Scorer correct | Median ms | p95 ms | Peak MiB | Brier | ECE | Order changes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen/Qwen2.5-0.5B-Instruct | `generate_label` | 93/231 | 50.35 | 257.97 | 1132.3 | N/A | N/A | 61.0% |
| Qwen/Qwen2.5-0.5B-Instruct | `generate_json` | 89/231 | 204.89 | 1366.12 | 1134.9 | N/A | N/A | 35.5% |
| Qwen/Qwen2.5-0.5B-Instruct | `labels` | 97/231 | 26.78 | 160.74 | 2087.2 | 0.678 | 0.249 | 61.9% |
| Qwen/Qwen2.5-0.5B-Instruct | `independent` | 121/231 | 108.43 | 710.51 | 2045.3 | 0.595 | 0.099 | 0.9% |
| Qwen/Qwen2.5-0.5B-Instruct | `sequence_likelihood` | 123/231 | 115.31 | 741.33 | 2131.5 | 0.609 | 0.129 | 33.8% |
| Qwen/Qwen2.5-1.5B-Instruct | `generate_label` | 129/231 | 69.95 | 440.26 | 3307.8 | N/A | N/A | 35.5% |
| Qwen/Qwen2.5-1.5B-Instruct | `generate_json` | 135/231 | 217.18 | 653.52 | 3313.0 | N/A | N/A | 22.9% |
| Qwen/Qwen2.5-1.5B-Instruct | `labels` | 135/231 | 36.02 | 440.73 | 4094.0 | 0.654 | 0.285 | 29.9% |
| Qwen/Qwen2.5-1.5B-Instruct | `independent` | 139/231 | 140.13 | 1864.81 | 4051.5 | 0.561 | 0.200 | 0.4% |
| Qwen/Qwen2.5-1.5B-Instruct | `sequence_likelihood` | 133/231 | 176.27 | 1915.90 | 4133.5 | 0.556 | 0.108 | 21.6% |

For **Qwen/Qwen2.5-0.5B-Instruct**, restricted logits have **1.88x lower median latency** than same-prompt label generation, with **97/231** versus **93/231** correct decisions under the pinned scorer. Full-option sequence likelihood scores **123/231** at **115.3 ms**; independent scoring scores **121/231** at **108.4 ms**. These observed accuracy differences have no significance claim.

For **Qwen/Qwen2.5-1.5B-Instruct**, restricted logits have **1.94x lower median latency** than same-prompt label generation, with **135/231** versus **129/231** correct decisions under the pinned scorer. Full-option sequence likelihood scores **133/231** at **176.3 ms**; independent scoring scores **139/231** at **140.1 ms**. These observed accuracy differences have no significance claim.

Accuracy, latency and memory above use canonical presentations only. Order changes compare the canonical order with one cyclic rotation, matching canonical label IDs. Distribution accuracy uses the pinned upstream scorer, including its lexicographic canonical-label tie break; the API selects the first supplied option on a tie. Order changes compare the API choices. Invalid outputs count as incorrect; an invalid/valid change also counts as an order change. Two invalid outputs with no selected choice count as unchanged.

Brier is the multiclass sum; ECE uses ten equal-width bins and top-label confidence. Both use valid score distributions only. Generation returns choices, so its calibration metrics are N/A. Softmax of restricted logits, Yes/No margins or mean sequence log-likelihoods supplies relative weights, not calibrated correctness probabilities.

Label generation and restricted logits share the same prompt; JSON uses a separate canonical-label JSON prompt with full option rubrics. Independent scoring sees one option rubric at a time. Prompt differences prevent attributing every accuracy difference solely to inference.

`sequence_likelihood` teacher-forces every token of each full option, divides the summed conditional log-probabilities by option token count, and excludes EOS. It uses a shared full-option prompt and one forward per option. The prompt and continuation are tokenized separately. This differs from single-token label scoring.

### Recorded test rigs

**Qwen/Qwen2.5-0.5B-Instruct**

```json
{
  "timestamp_utc": "2026-10-06T22:08:39.042265+00:00",
  "model": "Qwen/Qwen2.5-0.5B-Instruct",
  "model_revision": "7ae557604adf67be50417f59c2c2f167def9a775",
  "dataset_sha256": "dc3995d8ae1e2fc8e81ce38431add509eb8bb39b85aadfd0c7c32079382dde51",
  "source": {
    "repository": "https://github.com/fstandhartinger/jevbench",
    "revision": "bb05a335bc809e61b20c0f745d25499a82b326fc",
    "file_sha256": {
      "easy": "231df3c2c8e88a1a8c137ebe85de96ba70fabd330849098ac7b3c52c70b7172b",
      "original": "5c2414edb3006b8bfcb70fda433f0f9ca015759433849f8d3104328a1f7c4180",
      "hard": "89e9e6becb33ed88c1de7d42dcc87531b2fb64cfaef4e1986faf7c37b3f80ebb"
    },
    "scope": "231 published v1.2 easy/original/hard records; no sealed data"
  },
  "source_sha256": {
    "engine.py": "f7d70685c416a78160459b8727e042d4acfbc7897b5ca89a6dce77661199fde3",
    "benchmark.py": "9d66a3971788f6776e710c2369623a125f94d00701eff8d45dd6e4f6a6fe52c1",
    "jevbench_runner.py": "e7a485fc3472d72fda946c1c92b64fe2b44df0c2681c8d749571a3bb01b02205",
    "jevbench_data.py": "7378cef626a1bea2bfd24fdc0d43eacb8ced05363cf0cce4447c74866f117640",
    "prompts.py": "e68e153d9f3998eb12a6307e9ae1bc17b265d2541de32facbb850f01542e0d8e"
  },
  "unique_tasks": 231,
  "presentations": 462,
  "requests": 2310,
  "repeats": 1,
  "permutations": 1,
  "host": {
    "platform": "Linux-4.19.0-gvisor-x86_64-with-glibc2.36",
    "visible_cpu_count": 17,
    "resource_limits_pinned": false,
    "cpu_model": "unknown",
    "host_visible_ram_mib": 347429.0546875,
    "cpu_cgroup_quota": null,
    "gpu_telemetry_after": "610.57.04, P0, 1590, 70.00",
    "gpu_telemetry_fields": [
      "driver_version",
      "pstate",
      "sm_clock_mhz",
      "power_limit_w"
    ],
    "note": "Host-visible resources are not container allocations; GPU telemetry is an end-of-run snapshot, not pinned clocks during measurement."
  },
  "gpu_compute_capability": [
    7,
    5
  ],
  "gpu": "Tesla T4",
  "gpu_total_mib": 14920.5,
  "dtype": "torch.float16",
  "python": "3.11.12",
  "versions": {
    "torch": "2.14.1",
    "transformers": "4.57.6",
    "accelerate": "1.15.0"
  },
  "cuda": "13.0",
  "max_input_tokens": 8192,
  "warmup_runs_per_method": 2,
  "batch_size": 1,
  "concurrency": 1,
  "generation_limits": {
    "generate_label": 16,
    "generate_json": 64
  },
  "greedy": true,
  "temperature": 1.0,
  "scorer": "vendored JevBench v1.2 core; argmax label accuracy; ordinal EV MAE; supplementary v1.5-style Noul thresholds; no official composite",
  "timing": "tokenization + model + processing; CUDA synchronized; no HTTP or cold start",
  "calibration": "Brier multiclass sum; top-label ECE, 10 equal-width bins; only valid distributions on canonical presentations; label-only=N/A",
  "permutation": "one-position cyclic rotation by default; same canonical labels and rubrics",
  "failure_policy": "failed attempts count as incorrect; no truncation or dropped tasks"
}
```

**Qwen/Qwen2.5-1.5B-Instruct**

```json
{
  "timestamp_utc": "2026-10-06T22:13:08.212975+00:00",
  "model": "Qwen/Qwen2.5-1.5B-Instruct",
  "model_revision": "989aa7980e4cf806f80c7fef2b1adb7bc71aa306",
  "dataset_sha256": "dc3995d8ae1e2fc8e81ce38431add509eb8bb39b85aadfd0c7c32079382dde51",
  "source": {
    "repository": "https://github.com/fstandhartinger/jevbench",
    "revision": "bb05a335bc809e61b20c0f745d25499a82b326fc",
    "file_sha256": {
      "easy": "231df3c2c8e88a1a8c137ebe85de96ba70fabd330849098ac7b3c52c70b7172b",
      "original": "5c2414edb3006b8bfcb70fda433f0f9ca015759433849f8d3104328a1f7c4180",
      "hard": "89e9e6becb33ed88c1de7d42dcc87531b2fb64cfaef4e1986faf7c37b3f80ebb"
    },
    "scope": "231 published v1.2 easy/original/hard records; no sealed data"
  },
  "source_sha256": {
    "engine.py": "f7d70685c416a78160459b8727e042d4acfbc7897b5ca89a6dce77661199fde3",
    "benchmark.py": "9d66a3971788f6776e710c2369623a125f94d00701eff8d45dd6e4f6a6fe52c1",
    "jevbench_runner.py": "e7a485fc3472d72fda946c1c92b64fe2b44df0c2681c8d749571a3bb01b02205",
    "jevbench_data.py": "7378cef626a1bea2bfd24fdc0d43eacb8ced05363cf0cce4447c74866f117640",
    "prompts.py": "e68e153d9f3998eb12a6307e9ae1bc17b265d2541de32facbb850f01542e0d8e"
  },
  "unique_tasks": 231,
  "presentations": 462,
  "requests": 2310,
  "repeats": 1,
  "permutations": 1,
  "host": {
    "platform": "Linux-4.19.0-gvisor-x86_64-with-glibc2.36",
    "visible_cpu_count": 17,
    "resource_limits_pinned": false,
    "cpu_model": "unknown",
    "host_visible_ram_mib": 347429.0625,
    "cpu_cgroup_quota": null,
    "gpu_telemetry_after": "610.57.04, P0, 1575, 70.00",
    "gpu_telemetry_fields": [
      "driver_version",
      "pstate",
      "sm_clock_mhz",
      "power_limit_w"
    ],
    "note": "Host-visible resources are not container allocations; GPU telemetry is an end-of-run snapshot, not pinned clocks during measurement."
  },
  "gpu_compute_capability": [
    7,
    5
  ],
  "gpu": "Tesla T4",
  "gpu_total_mib": 14920.5,
  "dtype": "torch.float16",
  "python": "3.11.12",
  "versions": {
    "torch": "2.14.1",
    "transformers": "4.57.6",
    "accelerate": "1.15.0"
  },
  "cuda": "13.0",
  "max_input_tokens": 8192,
  "warmup_runs_per_method": 2,
  "batch_size": 1,
  "concurrency": 1,
  "generation_limits": {
    "generate_label": 16,
    "generate_json": 64
  },
  "greedy": true,
  "temperature": 1.0,
  "scorer": "vendored JevBench v1.2 core; argmax label accuracy; ordinal EV MAE; supplementary v1.5-style Noul thresholds; no official composite",
  "timing": "tokenization + model + processing; CUDA synchronized; no HTTP or cold start",
  "calibration": "Brier multiclass sum; top-label ECE, 10 equal-width bins; only valid distributions on canonical presentations; label-only=N/A",
  "permutation": "one-position cyclic rotation by default; same canonical labels and rubrics",
  "failure_policy": "failed attempts count as incorrect; no truncation or dropped tasks"
}
```

Timing includes tokenization, inference and processing with CUDA synchronization; model loading, queueing and HTTP are excluded. Peak memory measures allocated PyTorch tensors including model weights, excluding allocator cache and CUDA context. Host-visible resources and GPU driver/clocks are snapshots, not pinned allocations. Each GPU job runs methods serially with batch size and concurrency one. Generation uses KV cache; scoring disables it. No quantization, torch.compile, TensorRT or vLLM is enabled. Different model jobs may overlap on separate Modal GPU allocations.

### Task breakdown

| Model | Method | Tier | Correct | Invalid | Failures |
| --- | --- | --- | --- | --- | --- |
| Qwen/Qwen2.5-0.5B-Instruct | `generate_label` | easy | 35/48 | 0 | 0 |
| Qwen/Qwen2.5-0.5B-Instruct | `generate_label` | hard | 31/111 | 15 | 0 |
| Qwen/Qwen2.5-0.5B-Instruct | `generate_label` | original | 27/72 | 2 | 0 |
| Qwen/Qwen2.5-0.5B-Instruct | `generate_json` | easy | 38/48 | 0 | 0 |
| Qwen/Qwen2.5-0.5B-Instruct | `generate_json` | hard | 27/111 | 18 | 0 |
| Qwen/Qwen2.5-0.5B-Instruct | `generate_json` | original | 24/72 | 1 | 0 |
| Qwen/Qwen2.5-0.5B-Instruct | `labels` | easy | 35/48 | 0 | 0 |
| Qwen/Qwen2.5-0.5B-Instruct | `labels` | hard | 35/111 | 0 | 0 |
| Qwen/Qwen2.5-0.5B-Instruct | `labels` | original | 27/72 | 0 | 0 |
| Qwen/Qwen2.5-0.5B-Instruct | `independent` | easy | 46/48 | 0 | 0 |
| Qwen/Qwen2.5-0.5B-Instruct | `independent` | hard | 38/111 | 0 | 0 |
| Qwen/Qwen2.5-0.5B-Instruct | `independent` | original | 37/72 | 0 | 0 |
| Qwen/Qwen2.5-0.5B-Instruct | `sequence_likelihood` | easy | 44/48 | 0 | 0 |
| Qwen/Qwen2.5-0.5B-Instruct | `sequence_likelihood` | hard | 44/111 | 0 | 0 |
| Qwen/Qwen2.5-0.5B-Instruct | `sequence_likelihood` | original | 35/72 | 0 | 0 |
| Qwen/Qwen2.5-1.5B-Instruct | `generate_label` | easy | 45/48 | 2 | 0 |
| Qwen/Qwen2.5-1.5B-Instruct | `generate_label` | hard | 42/111 | 7 | 0 |
| Qwen/Qwen2.5-1.5B-Instruct | `generate_label` | original | 42/72 | 1 | 0 |
| Qwen/Qwen2.5-1.5B-Instruct | `generate_json` | easy | 46/48 | 0 | 0 |
| Qwen/Qwen2.5-1.5B-Instruct | `generate_json` | hard | 46/111 | 0 | 0 |
| Qwen/Qwen2.5-1.5B-Instruct | `generate_json` | original | 43/72 | 0 | 0 |
| Qwen/Qwen2.5-1.5B-Instruct | `labels` | easy | 47/48 | 0 | 0 |
| Qwen/Qwen2.5-1.5B-Instruct | `labels` | hard | 46/111 | 0 | 0 |
| Qwen/Qwen2.5-1.5B-Instruct | `labels` | original | 42/72 | 0 | 0 |
| Qwen/Qwen2.5-1.5B-Instruct | `independent` | easy | 48/48 | 0 | 0 |
| Qwen/Qwen2.5-1.5B-Instruct | `independent` | hard | 41/111 | 0 | 0 |
| Qwen/Qwen2.5-1.5B-Instruct | `independent` | original | 50/72 | 0 | 0 |
| Qwen/Qwen2.5-1.5B-Instruct | `sequence_likelihood` | easy | 47/48 | 0 | 0 |
| Qwen/Qwen2.5-1.5B-Instruct | `sequence_likelihood` | hard | 41/111 | 0 | 0 |
| Qwen/Qwen2.5-1.5B-Instruct | `sequence_likelihood` | original | 45/72 | 0 | 0 |

### Accuracy by task type

| Model | Method | Type | Correct | Invalid |
| --- | --- | --- | --- | --- |
| Qwen/Qwen2.5-0.5B-Instruct | `generate_label` | choice | 54/139 | 13 |
| Qwen/Qwen2.5-0.5B-Instruct | `generate_label` | noul | 36/74 | 3 |
| Qwen/Qwen2.5-0.5B-Instruct | `generate_label` | score | 3/18 | 1 |
| Qwen/Qwen2.5-0.5B-Instruct | `generate_json` | choice | 55/139 | 7 |
| Qwen/Qwen2.5-0.5B-Instruct | `generate_json` | noul | 29/74 | 10 |
| Qwen/Qwen2.5-0.5B-Instruct | `generate_json` | score | 5/18 | 2 |
| Qwen/Qwen2.5-0.5B-Instruct | `labels` | choice | 58/139 | 0 |
| Qwen/Qwen2.5-0.5B-Instruct | `labels` | noul | 36/74 | 0 |
| Qwen/Qwen2.5-0.5B-Instruct | `labels` | score | 3/18 | 0 |
| Qwen/Qwen2.5-0.5B-Instruct | `independent` | choice | 71/139 | 0 |
| Qwen/Qwen2.5-0.5B-Instruct | `independent` | noul | 42/74 | 0 |
| Qwen/Qwen2.5-0.5B-Instruct | `independent` | score | 8/18 | 0 |
| Qwen/Qwen2.5-0.5B-Instruct | `sequence_likelihood` | choice | 71/139 | 0 |
| Qwen/Qwen2.5-0.5B-Instruct | `sequence_likelihood` | noul | 46/74 | 0 |
| Qwen/Qwen2.5-0.5B-Instruct | `sequence_likelihood` | score | 6/18 | 0 |
| Qwen/Qwen2.5-1.5B-Instruct | `generate_label` | choice | 85/139 | 3 |
| Qwen/Qwen2.5-1.5B-Instruct | `generate_label` | noul | 37/74 | 6 |
| Qwen/Qwen2.5-1.5B-Instruct | `generate_label` | score | 7/18 | 1 |
| Qwen/Qwen2.5-1.5B-Instruct | `generate_json` | choice | 90/139 | 0 |
| Qwen/Qwen2.5-1.5B-Instruct | `generate_json` | noul | 40/74 | 0 |
| Qwen/Qwen2.5-1.5B-Instruct | `generate_json` | score | 5/18 | 0 |
| Qwen/Qwen2.5-1.5B-Instruct | `labels` | choice | 87/139 | 0 |
| Qwen/Qwen2.5-1.5B-Instruct | `labels` | noul | 41/74 | 0 |
| Qwen/Qwen2.5-1.5B-Instruct | `labels` | score | 7/18 | 0 |
| Qwen/Qwen2.5-1.5B-Instruct | `independent` | choice | 83/139 | 0 |
| Qwen/Qwen2.5-1.5B-Instruct | `independent` | noul | 43/74 | 0 |
| Qwen/Qwen2.5-1.5B-Instruct | `independent` | score | 13/18 | 0 |
| Qwen/Qwen2.5-1.5B-Instruct | `sequence_likelihood` | choice | 84/139 | 0 |
| Qwen/Qwen2.5-1.5B-Instruct | `sequence_likelihood` | noul | 43/74 | 0 |
| Qwen/Qwen2.5-1.5B-Instruct | `sequence_likelihood` | score | 6/18 | 0 |

### Additional diagnostics

| Model | Method | Returned choice correct | Valid distribution n | Valid order pairs | Mean order TV | Ordinal MAE | Noul threshold accuracy | Noul abstentions | Gold probability TV |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen/Qwen2.5-0.5B-Instruct | `generate_label` | 93/231 | 0 | 202 | N/A | 1.000 | 0.486 | 3 | N/A |
| Qwen/Qwen2.5-0.5B-Instruct | `generate_json` | 89/231 | 0 | 205 | N/A | 0.938 | 0.392 | 10 | N/A |
| Qwen/Qwen2.5-0.5B-Instruct | `labels` | 97/231 | 231 | 231 | 0.430 | 0.934 | 0.243 | 43 | 0.305 |
| Qwen/Qwen2.5-0.5B-Instruct | `independent` | 122/231 | 231 | 231 | 0.000 | 0.867 | 0.081 | 62 | 0.259 |
| Qwen/Qwen2.5-0.5B-Instruct | `sequence_likelihood` | 123/231 | 231 | 231 | 0.059 | 0.877 | 0.000 | 74 | 0.306 |
| Qwen/Qwen2.5-1.5B-Instruct | `generate_label` | 129/231 | 0 | 208 | N/A | 0.882 | 0.500 | 6 | N/A |
| Qwen/Qwen2.5-1.5B-Instruct | `generate_json` | 135/231 | 0 | 231 | N/A | 1.500 | 0.541 | 0 | N/A |
| Qwen/Qwen2.5-1.5B-Instruct | `labels` | 135/231 | 231 | 231 | 0.255 | 0.998 | 0.378 | 23 | 0.451 |
| Qwen/Qwen2.5-1.5B-Instruct | `independent` | 138/231 | 231 | 231 | 0.000 | 0.369 | 0.473 | 23 | 0.387 |
| Qwen/Qwen2.5-1.5B-Instruct | `sequence_likelihood` | 133/231 | 231 | 231 | 0.070 | 0.933 | 0.000 | 74 | 0.278 |

Ordinal MAE uses expected value for distribution methods and the selected level for generation, on valid ordinal predictions. Noul distribution decisions use P(yes) >= 0.8 for Yes, <= 0.2 for No, otherwise abstain; abstentions count as incorrect. Generation has no confidence threshold; its missing or invalid Noul decisions are included in the abstention count. These are supplementary typed diagnostics, not the official v1.5 composite. Gold probability TV measures fidelity on tasks with an explicitly supplied reference distribution; see raw summaries for denominators.

### Selected order changes

| Model | Method | Task | Canonical choice | Rotated choice |
| --- | --- | --- | --- | --- |
| Qwen/Qwen2.5-0.5B-Instruct | `generate_label` | easy-intent-00 | track_order | cancel_order |
| Qwen/Qwen2.5-0.5B-Instruct | `generate_json` | easy-intent-09 | set_alarm | send_message |
| Qwen/Qwen2.5-0.5B-Instruct | `labels` | easy-intent-00 | track_order | cancel_order |
| Qwen/Qwen2.5-0.5B-Instruct | `independent` | hard-opus-c-temporal_numeric-06 | sep_15_office_chair | sep_21_client_dinner |
| Qwen/Qwen2.5-0.5B-Instruct | `sequence_likelihood` | easy-intent-09 | set_alarm | send_message |
| Qwen/Qwen2.5-1.5B-Instruct | `generate_label` | easy-fact-05 | yes | no |
| Qwen/Qwen2.5-1.5B-Instruct | `generate_json` | easy-fact-04 | no | yes |
| Qwen/Qwen2.5-1.5B-Instruct | `labels` | easy-fact-05 | yes | no |
| Qwen/Qwen2.5-1.5B-Instruct | `independent` | hard-sol-c-multi_hop-12 | digital_copy_only | supervised_delivery |
| Qwen/Qwen2.5-1.5B-Instruct | `sequence_likelihood` | easy-extraction-01 | credit_card | cash |
