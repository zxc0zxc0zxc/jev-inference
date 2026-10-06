# Full classification benchmark

Model: **Qwen/Qwen2.5-1.5B-Instruct**; GPU: **Tesla T4**.

| Method | Correct | Invalid | Median ms | p95 ms | Peak VRAM MiB | Extra MiB |
| --- | --- | --- | --- | --- | --- | --- |
| `generate_label` | 18/30 (60.0%) | 0 | 167.4 | 657.1 | 3033.9 | 81.4 |
| `generate_json` | 25/30 (83.3%) | 0 | 362.1 | 821.3 | 3035.3 | 82.8 |
| `labels` | 18/30 (60.0%) | 0 | 145.4 | 723.3 | 3132.6 | 180.0 |
| `independent` | 25/30 (83.3%) | 0 | 451.2 | 2178.9 | 3131.7 | 179.2 |

Latency is the median of 3 repetitions; memory is the maximum. Choice and correctness use the first repetition; Stable indicates whether the choice stayed the same across repetitions. Accuracy requires a parsed allowed choice; malformed generated outputs count as incorrect. Label parsing accepts a single uppercase letter with optional trailing dot or parenthesis; JSON parsing requires an object whose choice field matches an allowed option. Cached allocator memory (peak_reserved_mib in JSON) can carry over between methods and is not used for memory comparisons. Raw outputs and repetitions: [JSON](benchmark-results-qwen2.5-1.5b.json).

| Case | Method | Expected | Choice | Correct | ms | Peak MiB | Extra MiB | Stable |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sentiment-positive | generate_label | positive | positive | ✓ | 164.4 | 2960.3 | 7.8 | True |
| sentiment-positive | generate_json | positive | positive | ✓ | 327.8 | 2961.3 | 8.7 | True |
| sentiment-positive | labels | positive | positive | ✓ | 142.9 | 2978.0 | 25.5 | True |
| sentiment-positive | independent | positive | positive | ✓ | 439.6 | 2977.2 | 24.6 | True |
| sentiment-negative | generate_label | negative | negative | ✓ | 163.9 | 2960.5 | 8.0 | True |
| sentiment-negative | generate_json | negative | negative | ✓ | 329.7 | 2961.4 | 8.9 | True |
| sentiment-negative | labels | negative | negative | ✓ | 144.1 | 2978.6 | 26.1 | True |
| sentiment-negative | independent | negative | negative | ✓ | 443.8 | 2977.7 | 25.2 | True |
| sentiment-neutral | generate_label | neutral | neutral | ✓ | 163.8 | 2960.0 | 7.5 | True |
| sentiment-neutral | generate_json | neutral | neutral | ✓ | 328.4 | 2960.9 | 8.4 | True |
| sentiment-neutral | labels | neutral | neutral | ✓ | 142.2 | 2976.9 | 24.3 | True |
| sentiment-neutral | independent | neutral | neutral | ✓ | 439.9 | 2976.0 | 23.5 | True |
| topic-sports | generate_label | sports | sports | ✓ | 164.7 | 2960.3 | 7.8 | True |
| topic-sports | generate_json | sports | sports | ✓ | 330.2 | 2961.3 | 8.7 | True |
| topic-sports | labels | sports | sports | ✓ | 143.2 | 2978.0 | 25.5 | True |
| topic-sports | independent | sports | sports | ✓ | 439.9 | 2977.2 | 24.6 | True |
| topic-technology | generate_label | technology | technology | ✓ | 165.0 | 2960.2 | 7.6 | True |
| topic-technology | generate_json | technology | technology | ✓ | 329.8 | 2961.1 | 8.5 | True |
| topic-technology | labels | technology | technology | ✓ | 142.6 | 2977.5 | 24.9 | True |
| topic-technology | independent | technology | technology | ✓ | 442.1 | 2976.6 | 24.1 | True |
| topic-finance | generate_label | finance | finance | ✓ | 163.3 | 2960.2 | 7.6 | True |
| topic-finance | generate_json | finance | finance | ✓ | 328.3 | 2961.1 | 8.5 | True |
| topic-finance | labels | finance | finance | ✓ | 142.5 | 2977.5 | 24.9 | True |
| topic-finance | independent | finance | finance | ✓ | 442.2 | 2976.6 | 24.1 | True |
| intent-cancel | generate_label | cancel subscription | cancel subscription | ✓ | 165.9 | 2960.6 | 8.1 | True |
| intent-cancel | generate_json | cancel subscription | cancel subscription | ✓ | 365.5 | 2961.5 | 9.0 | True |
| intent-cancel | labels | cancel subscription | cancel subscription | ✓ | 143.3 | 2978.9 | 26.4 | True |
| intent-cancel | independent | cancel subscription | cancel subscription | ✓ | 445.0 | 2977.5 | 24.9 | True |
| intent-password | generate_label | reset password | reset password | ✓ | 165.7 | 2960.7 | 8.2 | True |
| intent-password | generate_json | reset password | reset password | ✓ | 364.8 | 2961.6 | 9.1 | True |
| intent-password | labels | reset password | reset password | ✓ | 143.7 | 2979.2 | 26.7 | True |
| intent-password | independent | reset password | reset password | ✓ | 446.3 | 2977.7 | 25.2 | True |
| intent-shipment | generate_label | track shipment | track shipment | ✓ | 164.6 | 2960.6 | 8.1 | True |
| intent-shipment | generate_json | track shipment | track shipment | ✓ | 367.5 | 2961.5 | 9.0 | True |
| intent-shipment | labels | track shipment | track shipment | ✓ | 143.2 | 2978.9 | 26.4 | True |
| intent-shipment | independent | track shipment | track shipment | ✓ | 445.9 | 2977.5 | 24.9 | True |
| priority-low | generate_label | P3 | P3 | ✓ | 168.9 | 2962.3 | 9.8 | True |
| priority-low | generate_json | P3 | P3 | ✓ | 373.1 | 2963.3 | 10.7 | True |
| priority-low | labels | P3 | P3 | ✓ | 146.4 | 2984.4 | 31.9 | True |
| priority-low | independent | P3 | P3 | ✓ | 457.4 | 2983.0 | 30.4 | True |
| priority-critical | generate_label | P1 | P3 | ✗ | 168.3 | 2962.6 | 10.1 | True |
| priority-critical | generate_json | P1 | P1 | ✓ | 367.6 | 2963.5 | 11.0 | True |
| priority-critical | labels | P1 | P3 | ✗ | 147.9 | 2985.3 | 32.7 | True |
| priority-critical | independent | P1 | P1 | ✓ | 460.0 | 2983.8 | 31.3 | True |
| priority-partial | generate_label | P2 | P3 | ✗ | 175.0 | 2962.7 | 10.2 | True |
| priority-partial | generate_json | P2 | P3 | ✗ | 336.7 | 2963.6 | 11.1 | True |
| priority-partial | labels | P2 | P3 | ✗ | 149.4 | 2985.6 | 33.0 | True |
| priority-partial | independent | P2 | P1 | ✗ | 462.2 | 2984.1 | 31.6 | True |
| risk-high | generate_label | high | low | ✗ | 167.1 | 2962.1 | 9.5 | True |
| risk-high | generate_json | high | high | ✓ | 302.1 | 2963.0 | 10.5 | True |
| risk-high | labels | high | low | ✗ | 146.8 | 2983.5 | 31.0 | True |
| risk-high | independent | high | high | ✓ | 452.8 | 2982.7 | 30.1 | True |
| risk-low | generate_label | low | low | ✓ | 169.1 | 2962.1 | 9.5 | True |
| risk-low | generate_json | low | low | ✓ | 332.7 | 2963.0 | 10.5 | True |
| risk-low | labels | low | low | ✓ | 147.1 | 2983.5 | 31.0 | True |
| risk-low | independent | low | low | ✓ | 455.3 | 2982.7 | 30.1 | True |
| risk-medium | generate_label | medium | low | ✗ | 168.8 | 2962.1 | 9.5 | True |
| risk-medium | generate_json | medium | medium | ✓ | 299.0 | 2963.0 | 10.5 | True |
| risk-medium | labels | medium | low | ✗ | 146.7 | 2983.5 | 31.0 | True |
| risk-medium | independent | medium | medium | ✓ | 454.3 | 2982.7 | 30.1 | True |
| action-heal | generate_label | heal | retreat | ✗ | 167.9 | 2962.4 | 9.9 | True |
| action-heal | generate_json | heal | heal | ✓ | 363.1 | 2963.5 | 11.0 | True |
| action-heal | labels | heal | retreat | ✗ | 146.0 | 2984.7 | 32.2 | True |
| action-heal | independent | heal | heal | ✓ | 462.6 | 2984.1 | 31.6 | True |
| action-retreat | generate_label | retreat | retreat | ✓ | 167.7 | 2962.4 | 9.9 | True |
| action-retreat | generate_json | retreat | retreat | ✓ | 367.4 | 2963.5 | 11.0 | True |
| action-retreat | labels | retreat | retreat | ✓ | 148.3 | 2984.7 | 32.2 | True |
| action-retreat | independent | retreat | retreat | ✓ | 461.3 | 2984.1 | 31.6 | True |
| action-attack | generate_label | attack | retreat | ✗ | 168.9 | 2962.4 | 9.9 | True |
| action-attack | generate_json | attack | heal | ✗ | 366.5 | 2963.5 | 11.0 | True |
| action-attack | labels | attack | retreat | ✗ | 146.6 | 2984.7 | 32.2 | True |
| action-attack | independent | attack | heal | ✗ | 458.6 | 2984.1 | 31.6 | True |
| arithmetic-multiply | generate_label | 56 | 56 | ✓ | 164.9 | 2960.1 | 7.5 | True |
| arithmetic-multiply | generate_json | 56 | 56 | ✓ | 361.0 | 2960.7 | 8.2 | True |
| arithmetic-multiply | labels | 56 | 56 | ✓ | 143.5 | 2977.2 | 24.6 | True |
| arithmetic-multiply | independent | 56 | 56 | ✓ | 443.3 | 2974.8 | 22.3 | True |
| arithmetic-subtract | generate_label | 63 | 67 | ✗ | 164.7 | 2960.3 | 7.8 | True |
| arithmetic-subtract | generate_json | 63 | 63 | ✓ | 360.0 | 2961.0 | 8.5 | True |
| arithmetic-subtract | labels | 63 | 67 | ✗ | 144.5 | 2978.0 | 25.5 | True |
| arithmetic-subtract | independent | 63 | 73 | ✗ | 444.4 | 2975.7 | 23.2 | True |
| arithmetic-compare | generate_label | 0.03 | 0.12 | ✗ | 165.5 | 2960.1 | 7.5 | True |
| arithmetic-compare | generate_json | 0.03 | 0.03 | ✓ | 427.0 | 2960.7 | 8.2 | True |
| arithmetic-compare | labels | 0.03 | 0.12 | ✗ | 143.6 | 2977.2 | 24.6 | True |
| arithmetic-compare | independent | 0.03 | 0.03 | ✓ | 442.4 | 2974.0 | 21.4 | True |
| logic-entailed | generate_label | entailed | entailed | ✓ | 172.9 | 2963.0 | 10.5 | True |
| logic-entailed | generate_json | entailed | entailed | ✓ | 376.7 | 2964.0 | 11.5 | True |
| logic-entailed | labels | entailed | entailed | ✓ | 149.3 | 2986.4 | 33.9 | True |
| logic-entailed | independent | entailed | entailed | ✓ | 463.1 | 2985.6 | 33.0 | True |
| logic-contradicted | generate_label | contradicted | contradicted | ✓ | 170.2 | 2962.8 | 10.3 | True |
| logic-contradicted | generate_json | contradicted | contradicted | ✓ | 412.0 | 2963.8 | 11.3 | True |
| logic-contradicted | labels | contradicted | contradicted | ✓ | 148.9 | 2985.9 | 33.3 | True |
| logic-contradicted | independent | contradicted | contradicted | ✓ | 460.5 | 2985.0 | 32.5 | True |
| logic-unknown | generate_label | unknown | entailed | ✗ | 170.2 | 2962.7 | 10.2 | True |
| logic-unknown | generate_json | unknown | entailed | ✗ | 370.1 | 2963.7 | 11.2 | True |
| logic-unknown | labels | unknown | entailed | ✗ | 148.1 | 2985.6 | 33.0 | True |
| logic-unknown | independent | unknown | entailed | ✗ | 459.5 | 2984.7 | 32.2 | True |
| sentiment-positive-short | generate_label | positive | positive | ✓ | 168.2 | 2960.6 | 8.1 | True |
| sentiment-positive-short | generate_json | positive | positive | ✓ | 331.1 | 2961.5 | 9.0 | True |
| sentiment-positive-short | labels | positive | positive | ✓ | 144.3 | 2978.9 | 26.4 | True |
| sentiment-positive-short | independent | positive | positive | ✓ | 449.6 | 2978.0 | 25.5 | True |
| sentiment-negative-short | generate_label | negative | negative | ✓ | 165.4 | 2960.6 | 8.1 | True |
| sentiment-negative-short | generate_json | negative | negative | ✓ | 329.4 | 2961.5 | 9.0 | True |
| sentiment-negative-short | labels | negative | negative | ✓ | 144.7 | 2978.9 | 26.4 | True |
| sentiment-negative-short | independent | negative | negative | ✓ | 448.8 | 2978.0 | 25.5 | True |
| sentiment-neutral-short | generate_label | neutral | positive | ✗ | 165.4 | 2960.4 | 7.9 | True |
| sentiment-neutral-short | generate_json | neutral | neutral | ✓ | 331.3 | 2961.3 | 8.8 | True |
| sentiment-neutral-short | labels | neutral | positive | ✗ | 144.6 | 2978.3 | 25.8 | True |
| sentiment-neutral-short | independent | neutral | neutral | ✓ | 447.7 | 2977.5 | 24.9 | True |
| logs-healthy | generate_label | healthy | failed | ✗ | 657.1 | 3033.9 | 81.4 | True |
| logs-healthy | generate_json | healthy | warning | ✗ | 823.4 | 3035.3 | 82.8 | True |
| logs-healthy | labels | healthy | failed | ✗ | 723.3 | 3132.6 | 180.0 | True |
| logs-healthy | independent | healthy | healthy | ✓ | 2184.5 | 3131.7 | 179.2 | True |
| logs-warning | generate_label | warning | failed | ✗ | 659.2 | 3033.5 | 81.0 | True |
| logs-warning | generate_json | warning | healthy | ✗ | 820.2 | 3034.8 | 82.2 | True |
| logs-warning | labels | warning | failed | ✗ | 723.6 | 3132.3 | 179.8 | True |
| logs-warning | independent | warning | warning | ✓ | 2178.9 | 3130.5 | 178.0 | True |
| logs-failed | generate_label | failed | failed | ✓ | 654.8 | 3031.4 | 78.9 | True |
| logs-failed | generate_json | failed | failed | ✓ | 821.3 | 3033.8 | 81.3 | True |
| logs-failed | labels | failed | failed | ✓ | 720.8 | 3129.3 | 176.8 | True |
| logs-failed | independent | failed | warning | ✗ | 2176.6 | 3128.5 | 175.9 | True |

## Metadata

```json
{
  "timestamp_utc": "2026-10-06T21:23:45.254571+00:00",
  "model": "Qwen/Qwen2.5-1.5B-Instruct",
  "model_revision": "989aa7980e4cf806f80c7fef2b1adb7bc71aa306",
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
