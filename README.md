# The Geometry of Safety

**Mapping and Hardening Refusal Mechanisms in Aligned Language Models**

Maaz Shamim and Rashed Aldulijan. Final project for the Fall 2026 NLP
self-supervised learning course at Johns Hopkins University.

Refusal in aligned LLMs is mediated by a single linear direction in the residual
stream (Arditi et al., 2024). Projecting that direction out of the weights
("abliteration") removes refusal while leaving most capabilities intact. This
project studies that fragility empirically: which layers carry the refusal
signal, whether the direction transfers across model families, whether the
Circuit Breakers defense survives an adaptive white-box attack, and whether
spreading refusal across all layers buys robustness, and at what capability cost.

The full proposal is in [docs/proposal/](docs/proposal/NLP_SSL_Project_26.pdf).

## Status

Scaffold only. The package modules and experiment scripts are placeholders that
describe what belongs in them. Nothing is implemented or run yet.

## Experiments

| ID | Experiment | Models | Reports |
|----|------------|--------|---------|
| E1 | Baseline reproduction: full abliteration | Llama, Mistral | Refusal rate and MMLU, before and after |
| E2 | Layer sensitivity: ablate one layer at a time | Llama, Mistral | Refusal rate vs. layer index |
| E3 | Direction transfer: Llama's direction applied to Mistral | Llama → Mistral | Refusal reduction vs. Mistral's own direction |
| E4 | Partial ablation sweep: 10, 25, 50, 75, 100% of the direction | Llama, Mistral | Refusal rate and MMLU jointly |
| E5 | Circuit Breakers under naive and adaptive abliteration | Mistral | Refusal rate under each attack |
| E6 | Multi-layer redundancy defense | Llama | Layers an attacker must ablate before refusal drops below 50%, and the MMLU cost |

Models are Llama-3.1-8B-Instruct and Mistral-7B-Instruct-v0.3. The proposal does
not name the models for E2 and E4; both are assumed.

## Layout

```
configs/
  defaults.yaml          settings shared by all experiments
  models/                one file per model (Hugging Face ID, dtype, dimensions)
  experiments/           one file per experiment, E1 to E6
data/                    downloaded datasets (git-ignored), see data/README.md
docs/proposal/           project proposal: LaTeX source and submitted PDF
notebooks/               exploratory analysis
results/                 final figures and tables, small enough to commit
scripts/                 one entry point per experiment
src/geometry_of_safety/
  data.py                AdvBench and Alpaca prompts, contrastive split
  models.py              model and tokenizer loading
  hooks.py               reading and writing the residual stream
  directions.py          refusal direction extraction
  interventions/         activation steering, weight orthogonalization
  defenses/              Circuit Breakers, multi-layer redundancy
  evaluation/            refusal rate, MMLU, WikiText-2 perplexity
tests/
```

Large run artifacts (activations, checkpoints, raw generations) go in `outputs/`,
which is git-ignored. Only figures and tables that belong in the report go in
`results/`.

## Setup

```bash
git clone https://github.com/rashdul/geometry-of-safety.git
cd geometry-of-safety
uv venv
uv pip install -e ".[dev]"
uv run pytest
```

Without uv: `python -m venv .venv`, activate it, then `pip install -e ".[dev]"`.

- **GPU.** The proposal budgets 20 GB of VRAM per model in bfloat16. If the
  default PyTorch wheel does not match your CUDA version (or you are on Windows,
  where the default wheel is CPU-only), install the right build from
  pytorch.org before the step above.
- **Model access.** Llama 3.1 is gated: request access on the
  [model page](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct), then run
  `huggingface-cli login`. Mistral-7B-Instruct-v0.3 needs no approval.

## Responsible use

This is safety research. Abliterated or otherwise unsafe checkpoints stay on the
machine that produced them: weight files are git-ignored and are not to be
uploaded anywhere. Harmful-prompt datasets are fetched from their original
sources and are not redistributed in this repository.
