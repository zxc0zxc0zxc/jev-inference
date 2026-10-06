# Full classification benchmark

Model: **Qwen/Qwen2.5-0.5B-Instruct**; GPU: **Tesla T4**.

| Method | Correct | Invalid | Median ms | p95 ms | Peak VRAM MiB | Extra MiB |
| --- | --- | --- | --- | --- | --- | --- |
| `generate_label` | 13/30 (43.3%) | 8 | 73.4 | 224.0 | 1018.0 | 67.5 |
| `generate_json` | 13/30 (43.3%) | 5 | 217.1 | 459.3 | 1020.1 | 69.7 |
| `labels` | 17/30 (56.7%) | 0 | 50.5 | 250.0 | 1129.7 | 179.3 |
| `independent` | 16/30 (53.3%) | 0 | 161.5 | 766.6 | 1128.9 | 178.4 |

Latency is the median of 3 repetitions; memory is the maximum. Choice and correctness use the first repetition; Stable indicates whether the choice stayed the same across repetitions. Accuracy requires a parsed allowed choice; malformed generated outputs count as incorrect. Label parsing accepts a single uppercase letter with optional trailing dot or parenthesis; JSON parsing requires an object whose choice field matches an allowed option. Cached allocator memory (peak_reserved_mib in JSON) can carry over between methods and is not used for memory comparisons. Raw outputs and repetitions: [JSON](benchmark-results.json).

| Case | Method | Expected | Choice | Correct | ms | Peak MiB | Extra MiB | Stable |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sentiment-positive | generate_label | positive | positive | ✓ | 71.5 | 954.5 | 4.0 | True |
| sentiment-positive | generate_json | positive | positive | ✓ | 211.0 | 954.9 | 4.5 | True |
| sentiment-positive | labels | positive | positive | ✓ | 49.8 | 976.0 | 25.5 | True |
| sentiment-positive | independent | positive | positive | ✓ | 158.1 | 975.1 | 24.6 | True |
| sentiment-negative | generate_label | negative | INVALID | ✗ | 124.3 | 954.6 | 4.1 | True |
| sentiment-negative | generate_json | negative | negative | ✓ | 205.3 | 955.0 | 4.6 | True |
| sentiment-negative | labels | negative | negative | ✓ | 49.3 | 977.0 | 26.6 | True |
| sentiment-negative | independent | negative | negative | ✓ | 157.4 | 975.7 | 25.2 | True |
| sentiment-neutral | generate_label | neutral | INVALID | ✗ | 124.0 | 954.3 | 3.8 | True |
| sentiment-neutral | generate_json | neutral | positive | ✗ | 204.1 | 954.7 | 4.3 | True |
| sentiment-neutral | labels | neutral | negative | ✗ | 49.2 | 974.8 | 24.3 | True |
| sentiment-neutral | independent | neutral | negative | ✗ | 157.9 | 973.9 | 23.5 | True |
| topic-sports | generate_label | sports | sports | ✓ | 71.3 | 954.5 | 4.0 | True |
| topic-sports | generate_json | sports | sports | ✓ | 206.3 | 954.9 | 4.5 | True |
| topic-sports | labels | sports | sports | ✓ | 49.4 | 976.0 | 25.5 | True |
| topic-sports | independent | sports | sports | ✓ | 158.4 | 975.1 | 24.6 | True |
| topic-technology | generate_label | technology | technology | ✓ | 72.8 | 954.4 | 3.9 | True |
| topic-technology | generate_json | technology | technology | ✓ | 209.1 | 954.8 | 4.4 | True |
| topic-technology | labels | technology | technology | ✓ | 55.1 | 975.4 | 24.9 | True |
| topic-technology | independent | technology | technology | ✓ | 165.5 | 974.5 | 24.1 | True |
| topic-finance | generate_label | finance | finance | ✓ | 72.2 | 954.4 | 3.9 | True |
| topic-finance | generate_json | finance | finance | ✓ | 209.9 | 954.8 | 4.4 | True |
| topic-finance | labels | finance | finance | ✓ | 49.6 | 975.4 | 24.9 | True |
| topic-finance | independent | finance | finance | ✓ | 157.4 | 974.5 | 24.1 | True |
| intent-cancel | generate_label | cancel subscription | cancel subscription | ✓ | 71.9 | 954.6 | 4.2 | True |
| intent-cancel | generate_json | cancel subscription | cancel subscription | ✓ | 233.3 | 955.1 | 4.7 | True |
| intent-cancel | labels | cancel subscription | cancel subscription | ✓ | 49.6 | 977.0 | 26.6 | True |
| intent-cancel | independent | cancel subscription | cancel subscription | ✓ | 157.4 | 975.4 | 24.9 | True |
| intent-password | generate_label | reset password | reset password | ✓ | 72.9 | 954.7 | 4.2 | True |
| intent-password | generate_json | reset password | reset password | ✓ | 238.5 | 955.2 | 4.7 | True |
| intent-password | labels | reset password | reset password | ✓ | 49.4 | 977.1 | 26.7 | True |
| intent-password | independent | reset password | reset password | ✓ | 158.5 | 975.7 | 25.2 | True |
| intent-shipment | generate_label | track shipment | track shipment | ✓ | 72.5 | 954.6 | 4.2 | True |
| intent-shipment | generate_json | track shipment | cancel subscription | ✗ | 242.4 | 955.1 | 4.7 | True |
| intent-shipment | labels | track shipment | track shipment | ✓ | 49.8 | 977.0 | 26.6 | True |
| intent-shipment | independent | track shipment | track shipment | ✓ | 159.5 | 975.4 | 24.9 | True |
| priority-low | generate_label | P3 | P3 | ✓ | 73.3 | 955.6 | 5.2 | True |
| priority-low | generate_json | P3 | INVALID | ✗ | 267.0 | 956.9 | 6.4 | True |
| priority-low | labels | P3 | P3 | ✓ | 52.0 | 983.0 | 32.6 | True |
| priority-low | independent | P3 | P3 | ✓ | 162.4 | 980.9 | 30.4 | True |
| priority-critical | generate_label | P1 | P3 | ✗ | 73.4 | 955.8 | 5.3 | True |
| priority-critical | generate_json | P1 | INVALID | ✗ | 270.1 | 957.0 | 6.5 | True |
| priority-critical | labels | P1 | P3 | ✗ | 62.1 | 983.2 | 32.7 | True |
| priority-critical | independent | P1 | P3 | ✗ | 178.7 | 981.7 | 31.3 | True |
| priority-partial | generate_label | P2 | P3 | ✗ | 74.3 | 955.8 | 5.4 | True |
| priority-partial | generate_json | P2 | INVALID | ✗ | 276.6 | 957.0 | 6.5 | True |
| priority-partial | labels | P2 | P3 | ✗ | 51.4 | 983.5 | 33.0 | True |
| priority-partial | independent | P2 | P3 | ✗ | 166.8 | 982.0 | 31.6 | True |
| risk-high | generate_label | high | high | ✓ | 72.0 | 955.4 | 5.0 | True |
| risk-high | generate_json | high | high | ✓ | 206.6 | 956.0 | 5.6 | True |
| risk-high | labels | high | high | ✓ | 51.9 | 981.5 | 31.0 | True |
| risk-high | independent | high | medium | ✗ | 162.9 | 980.6 | 30.1 | True |
| risk-low | generate_label | low | high | ✗ | 72.5 | 955.4 | 5.0 | True |
| risk-low | generate_json | low | high | ✗ | 212.1 | 956.0 | 5.6 | True |
| risk-low | labels | low | high | ✗ | 50.4 | 981.5 | 31.0 | True |
| risk-low | independent | low | medium | ✗ | 161.2 | 980.6 | 30.1 | True |
| risk-medium | generate_label | medium | medium | ✓ | 73.4 | 955.4 | 5.0 | True |
| risk-medium | generate_json | medium | high | ✗ | 215.8 | 956.0 | 5.6 | True |
| risk-medium | labels | medium | medium | ✓ | 50.5 | 981.5 | 31.0 | True |
| risk-medium | independent | medium | medium | ✓ | 161.9 | 980.6 | 30.1 | True |
| action-heal | generate_label | heal | heal | ✓ | 74.5 | 955.7 | 5.2 | True |
| action-heal | generate_json | heal | attack | ✗ | 218.4 | 957.0 | 6.5 | True |
| action-heal | labels | heal | heal | ✓ | 51.3 | 983.0 | 32.6 | True |
| action-heal | independent | heal | attack | ✗ | 163.1 | 982.0 | 31.6 | True |
| action-retreat | generate_label | retreat | heal | ✗ | 72.6 | 955.7 | 5.2 | True |
| action-retreat | generate_json | retreat | attack | ✗ | 208.5 | 957.0 | 6.5 | True |
| action-retreat | labels | retreat | heal | ✗ | 50.9 | 983.0 | 32.6 | True |
| action-retreat | independent | retreat | retreat | ✓ | 163.5 | 982.0 | 31.6 | True |
| action-attack | generate_label | attack | heal | ✗ | 74.5 | 955.7 | 5.2 | True |
| action-attack | generate_json | attack | attack | ✓ | 210.4 | 957.0 | 6.5 | True |
| action-attack | labels | attack | heal | ✗ | 50.3 | 983.0 | 32.6 | True |
| action-attack | independent | attack | attack | ✓ | 162.7 | 982.0 | 31.6 | True |
| arithmetic-multiply | generate_label | 56 | 56 | ✓ | 71.4 | 954.3 | 3.9 | True |
| arithmetic-multiply | generate_json | 56 | INVALID | ✗ | 459.3 | 954.7 | 4.2 | True |
| arithmetic-multiply | labels | 56 | 56 | ✓ | 49.6 | 975.1 | 24.6 | True |
| arithmetic-multiply | independent | 56 | 64 | ✗ | 160.5 | 972.8 | 22.3 | True |
| arithmetic-subtract | generate_label | 63 | 67 | ✗ | 73.1 | 954.5 | 4.0 | True |
| arithmetic-subtract | generate_json | 63 | INVALID | ✗ | 465.5 | 954.8 | 4.4 | True |
| arithmetic-subtract | labels | 63 | 67 | ✗ | 49.6 | 976.0 | 25.5 | True |
| arithmetic-subtract | independent | 63 | 67 | ✗ | 159.6 | 973.6 | 23.2 | True |
| arithmetic-compare | generate_label | 0.03 | 0.9 | ✗ | 71.4 | 954.3 | 3.9 | True |
| arithmetic-compare | generate_json | 0.03 | 0.03 | ✓ | 295.6 | 954.7 | 4.2 | True |
| arithmetic-compare | labels | 0.03 | 0.9 | ✗ | 49.3 | 975.1 | 24.6 | True |
| arithmetic-compare | independent | 0.03 | 0.9 | ✗ | 158.8 | 971.9 | 21.4 | True |
| logic-entailed | generate_label | entailed | INVALID | ✗ | 159.4 | 956.0 | 5.6 | True |
| logic-entailed | generate_json | entailed | unknown | ✗ | 214.3 | 957.0 | 6.6 | True |
| logic-entailed | labels | entailed | entailed | ✓ | 50.8 | 985.0 | 34.6 | True |
| logic-entailed | independent | entailed | entailed | ✓ | 164.2 | 983.6 | 33.2 | True |
| logic-contradicted | generate_label | contradicted | INVALID | ✗ | 156.6 | 955.9 | 5.5 | True |
| logic-contradicted | generate_json | contradicted | unknown | ✗ | 210.5 | 957.0 | 6.6 | True |
| logic-contradicted | labels | contradicted | entailed | ✗ | 51.2 | 983.8 | 33.3 | True |
| logic-contradicted | independent | contradicted | entailed | ✗ | 164.5 | 983.6 | 33.2 | True |
| logic-unknown | generate_label | unknown | INVALID | ✗ | 157.8 | 955.8 | 5.4 | True |
| logic-unknown | generate_json | unknown | entailed | ✗ | 242.3 | 957.0 | 6.6 | True |
| logic-unknown | labels | unknown | entailed | ✗ | 51.1 | 983.5 | 33.0 | True |
| logic-unknown | independent | unknown | entailed | ✗ | 163.9 | 983.6 | 33.2 | True |
| sentiment-positive-short | generate_label | positive | INVALID | ✗ | 147.4 | 954.6 | 4.2 | True |
| sentiment-positive-short | generate_json | positive | positive | ✓ | 249.2 | 955.1 | 4.7 | True |
| sentiment-positive-short | labels | positive | positive | ✓ | 49.9 | 977.0 | 26.6 | True |
| sentiment-positive-short | independent | positive | positive | ✓ | 159.5 | 976.0 | 25.5 | True |
| sentiment-negative-short | generate_label | negative | INVALID | ✗ | 133.4 | 954.6 | 4.2 | True |
| sentiment-negative-short | generate_json | negative | negative | ✓ | 212.7 | 955.1 | 4.7 | True |
| sentiment-negative-short | labels | negative | negative | ✓ | 50.5 | 977.0 | 26.6 | True |
| sentiment-negative-short | independent | negative | negative | ✓ | 160.5 | 976.0 | 25.5 | True |
| sentiment-neutral-short | generate_label | neutral | INVALID | ✗ | 128.4 | 954.5 | 4.1 | True |
| sentiment-neutral-short | generate_json | neutral | positive | ✗ | 210.4 | 955.0 | 4.6 | True |
| sentiment-neutral-short | labels | neutral | negative | ✗ | 51.0 | 977.0 | 26.6 | True |
| sentiment-neutral-short | independent | neutral | positive | ✗ | 160.5 | 975.4 | 24.9 | True |
| logs-healthy | generate_label | healthy | healthy | ✓ | 224.0 | 1018.0 | 67.5 | True |
| logs-healthy | generate_json | healthy | failed | ✗ | 366.7 | 1020.1 | 69.7 | True |
| logs-healthy | labels | healthy | healthy | ✓ | 250.2 | 1129.7 | 179.3 | True |
| logs-healthy | independent | healthy | failed | ✗ | 769.1 | 1128.9 | 178.4 | True |
| logs-warning | generate_label | warning | healthy | ✗ | 224.5 | 1017.3 | 66.8 | True |
| logs-warning | generate_json | warning | failed | ✗ | 365.6 | 1019.4 | 69.0 | True |
| logs-warning | labels | warning | healthy | ✗ | 249.4 | 1129.5 | 179.1 | True |
| logs-warning | independent | warning | failed | ✗ | 766.6 | 1127.7 | 177.2 | True |
| logs-failed | generate_label | failed | healthy | ✗ | 224.0 | 1016.0 | 65.6 | True |
| logs-failed | generate_json | failed | failed | ✓ | 364.0 | 1017.8 | 67.3 | True |
| logs-failed | labels | failed | healthy | ✗ | 250.0 | 1126.5 | 176.1 | True |
| logs-failed | independent | failed | failed | ✓ | 766.0 | 1125.6 | 175.2 | True |

## Metadata

```json
{
  "timestamp_utc": "2026-10-06T21:13:15.257937+00:00",
  "model": "Qwen/Qwen2.5-0.5B-Instruct",
  "model_revision": "7ae557604adf67be50417f59c2c2f167def9a775",
  "dataset_sha256": "aa4943a1a92ed2f3b8cdd1ab3a5a7cfc586aa8ae4e2281fab2e171077a2dc116",
  "cases": 30,
  "repeats": 3,
  "warmup_runs_per_method": 2,
  "gpu": "Tesla T4",
  "gpu_total_mib": 14920.5,
  "dtype": "torch.bfloat16",
  "python": "3.11.12",
  "versions": {
    "torch": "2.14.1",
    "transformers": "4.57.6",
    "accelerate": "1.15.0"
  },
  "cuda": "13.0",
  "max_input_tokens": 4096,
  "timing": "tokenization + model + decode/normalization; CUDA synchronized; no HTTP",
  "memory": "PyTorch CUDA allocator only; weights included; MiB = 2^20 bytes",
  "generation_limits": {
    "generate_label": 16,
    "generate_json": 64
  },
  "method_order": "rotated by case and repeat",
  "greedy": true,
  "accuracy_rule": "first repetition per case; invalid output counts as incorrect"
}
```
