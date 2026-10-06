## Benchmark: 30 classification tasks across model sizes

Same 30 hand-labeled English tasks, **Tesla T4**, `torch.bfloat16`, 3 repetitions per task/method, two warmup runs per method. Both model runs use the same dataset SHA256, library versions, prompt templates, and measurement protocol.

| Model | Method | Correct | Invalid | Median ms | p95 ms | Peak VRAM MiB |
| --- | --- | --- | --- | --- | --- | --- |
| Qwen2.5-0.5B-Instruct | `generate_label` | 13/30 (43.3%) | 8 | 73.4 | 224.0 | 1018.0 |
| Qwen2.5-0.5B-Instruct | `generate_json` | 13/30 (43.3%) | 5 | 217.1 | 459.3 | 1020.1 |
| Qwen2.5-0.5B-Instruct | `labels` | 17/30 (56.7%) | 0 | 50.5 | 250.0 | 1129.7 |
| Qwen2.5-0.5B-Instruct | `independent` | 16/30 (53.3%) | 0 | 161.5 | 766.6 | 1128.9 |
| Qwen2.5-1.5B-Instruct | `generate_label` | 18/30 (60.0%) | 0 | 167.4 | 657.1 | 3033.9 |
| Qwen2.5-1.5B-Instruct | `generate_json` | 25/30 (83.3%) | 0 | 362.1 | 821.3 | 3035.3 |
| Qwen2.5-1.5B-Instruct | `labels` | 18/30 (60.0%) | 0 | 145.4 | 723.3 | 3132.6 |
| Qwen2.5-1.5B-Instruct | `independent` | 25/30 (83.3%) | 0 | 451.2 | 2178.9 | 3131.7 |

### Test rig and protocol

| Setting | Configuration |
| --- | --- |
| Platform | Modal, separate ephemeral GPU jobs; Debian slim Linux container |
| GPU | 1 × Tesla T4; 14920.5 MiB CUDA-visible VRAM |
| Precision | torch.bfloat16; no quantization |
| Software | Python 3.11.12; PyTorch 2.14.1; Transformers 4.57.6; Accelerate 1.15.0 |
| CUDA | 13.0 (PyTorch build version, not the NVIDIA driver version) |
| Workload | Batch size 1; one request at a time; no batching or concurrency |
| Context | 4096 token limit; 82–625 tokens in generation prompts |
| Generation | Greedy, 1 beam, stop at EOS; label cap 16 tokens; JSON cap 64 tokens |
| KV cache | Enabled for generate(); disabled for direct logits forwards |
| Warmup / repeats | 2 warmups per method on the first case; 3 measured repeats per case/method |
| Execution | Methods rotated by case/repeat; model runs sequential; no explicit torch.compile, TensorRT, or vLLM |
| Host / driver | CPU model, host RAM, NVIDIA driver, GPU clocks and power limits were not captured or pinned |
| Dataset SHA256 | `aa4943a1a92ed2f3b8cdd1ab3a5a7cfc586aa8ae4e2281fab2e171077a2dc116` |

BF16 is the actual auto-selected model dtype in these runs. T4 lacks native BF16 Tensor Core support; these are not optimized FP16-throughput results. See the [NVIDIA precision support matrix](https://docs.nvidia.com/deeplearning/tensorrt/pdf/TensorRT-Support-Matrix-Guide.pdf).

- **Qwen/Qwen2.5-0.5B-Instruct**: revision `7ae557604adf67be50417f59c2c2f167def9a775`; measured `2026-10-06T21:13:15.257937+00:00`.
- **Qwen/Qwen2.5-1.5B-Instruct**: revision `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`; measured `2026-10-06T21:23:45.254571+00:00`.

Median latency ratios (baseline median divided by logits median):

- **Qwen2.5-0.5B-Instruct**: **4.30×** versus JSON generation; **1.45×** versus label generation.
- **Qwen2.5-1.5B-Instruct**: **2.49×** versus JSON generation; **1.15×** versus label generation.

For **Qwen2.5-1.5B-Instruct**, the identical-prompt comparison scored **18/30** for label generation and **18/30** for logits. The separate JSON prompt scored **25/30**, and independent scoring scored **25/30**. A speed improvement from changing inference does not imply that a label prompt matches the quality of a JSON prompt.

`generate_label` uses the **same prompt** as `labels`, with greedy decoding until EOS (16-token cap). `generate_json` uses a separate JSON prompt and a 64-token cap. `labels` reads A/B/C logits in one forward; `independent` uses one yes/no forward per option. No training or prompt tuning between model runs.

Selected examples (choice and median latency):

| Case | Model | Expected | Generate JSON | Generate label | Logits | Independent |
| --- | --- | --- | --- | --- | --- | --- |
| `sentiment-neutral` | Qwen2.5-0.5B-Instruct | neutral | positive ✗ · 204.1 ms | INVALID ✗ · 124.0 ms | negative ✗ · 49.2 ms | negative ✗ · 157.9 ms |
| `sentiment-neutral` | Qwen2.5-1.5B-Instruct | neutral | neutral ✓ · 328.4 ms | neutral ✓ · 163.8 ms | neutral ✓ · 142.2 ms | neutral ✓ · 439.9 ms |
| `risk-high` | Qwen2.5-0.5B-Instruct | high | high ✓ · 206.6 ms | high ✓ · 72.0 ms | high ✓ · 51.9 ms | medium ✗ · 162.9 ms |
| `risk-high` | Qwen2.5-1.5B-Instruct | high | high ✓ · 302.1 ms | low ✗ · 167.1 ms | low ✗ · 146.8 ms | high ✓ · 452.8 ms |
| `logic-contradicted` | Qwen2.5-0.5B-Instruct | contradicted | unknown ✗ · 210.5 ms | INVALID ✗ · 156.6 ms | entailed ✗ · 51.2 ms | entailed ✗ · 164.5 ms |
| `logic-contradicted` | Qwen2.5-1.5B-Instruct | contradicted | contradicted ✓ · 412.0 ms | contradicted ✓ · 170.2 ms | contradicted ✓ · 148.9 ms | contradicted ✓ · 460.5 ms |
| `arithmetic-compare` | Qwen2.5-0.5B-Instruct | 0.03 | 0.03 ✓ · 295.6 ms | 0.9 ✗ · 71.4 ms | 0.9 ✗ · 49.3 ms | 0.9 ✗ · 158.8 ms |
| `arithmetic-compare` | Qwen2.5-1.5B-Instruct | 0.03 | 0.03 ✓ · 427.0 ms | 0.12 ✗ · 165.5 ms | 0.12 ✗ · 143.6 ms | 0.03 ✓ · 442.4 ms |

Timing includes tokenization, inference, and result processing with CUDA synchronization; network, queueing, model loading, and cold starts are excluded. Median/p95 are computed over per-task latency medians. Peak VRAM is the maximum allocated PyTorch tensor memory, including weights, excluding CUDA context and allocator cache. Per-request extra memory is included in the full reports.

Accuracy includes output-format compliance; unparseable generated answers count as incorrect and are listed separately as Invalid. Correct answer positions are balanced (10 A / 10 B / 10 C). This small diagnostic set does not establish general decision quality. JSON comparisons mix inference and prompt-format effects; use the label baseline for identical prompts. The current logits engine computes vocabulary logits for the entire input, so it can use more VRAM and be slower on long inputs than label generation.

Full evidence (all choices, raw outputs, timings, memory, and model revisions):

- **Qwen2.5-0.5B-Instruct**: [raw JSON](benchmark-results.json), [full table](benchmark-report.md).
- **Qwen2.5-1.5B-Instruct**: [raw JSON](benchmark-results-qwen2.5-1.5b.json), [full table](benchmark-report-qwen2.5-1.5b.md).

[Dataset](../benchmarks/classification30.json). 720 measured requests in total. Runs are sequential and not simultaneous. Reproduce after installing `.[modal]` and running `modal setup`:

```bash
python run_benchmark.py --modal --model Qwen/Qwen2.5-0.5B-Instruct --gpu T4 --repeats 3 --output docs/benchmark-results.json
python run_benchmark.py --modal --model Qwen/Qwen2.5-1.5B-Instruct --gpu T4 --repeats 3 --output docs/benchmark-results-qwen2.5-1.5b.json
python -m jev_inference.benchmark_report docs/benchmark-results.json --compare docs/benchmark-results-qwen2.5-1.5b.json --update-readme
```

For a local CUDA GPU, install `.[inference]` and omit `--modal`. These ephemeral benchmark jobs do not update the deployed API. Dependency versions and model revisions can change between runs; compare metadata before comparing results.
