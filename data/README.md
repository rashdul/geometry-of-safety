# Data

Nothing in this directory is committed except this file. Datasets are downloaded
at run time from their original sources.

| Dataset | Used for | Source |
|---------|----------|--------|
| AdvBench harmful behaviors | Attack evaluation; harmful side of the contrastive pairs | `data/advbench/harmful_behaviors.csv` in [llm-attacks/llm-attacks](https://github.com/llm-attacks/llm-attacks) |
| Alpaca | Harmless side of the contrastive pairs, length-matched | `tatsu-lab/alpaca` on Hugging Face |
| MMLU | Capability evaluation (5-shot, 57 tasks) | `cais/mmlu` on Hugging Face |
| WikiText-2 | Perplexity | `Salesforce/wikitext` on Hugging Face |

AdvBench is used for both direction extraction and attack evaluation, so the two
uses need disjoint splits. The split is not decided yet (see `eval_split` in
`configs/defaults.yaml`).
