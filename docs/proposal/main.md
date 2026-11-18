# Motivation

RLHF and DPO produce aligned LLMs that reliably refuse harmful requests
but alignment is fragile. @arditi2024refusal showed that refusal is
mediated by a *single linear direction* in the residual stream.
Orthogonalizing all weight matrices against this direction removes
refusal while preserving most general capabilities. Crucially, this is
not a vulnerability of any specific model: gradient-based alignment
naturally produces linear geometric structure, so the attack is a
fundamental property of the training paradigm.

Understanding *where* and *why* this fragility exists is a prerequisite
for building safety mechanisms that are genuinely robust. We study the
geometric structure of refusal, its limits, and the tradeoffs a defender
must accept. This directly concerns the self-supervised pre-training
pipeline: the brittleness originates in how fine-tuning modifies the
base model's weight space, not in any specific architecture.

# Related Work

**Representation Engineering.** @zou2023representation showed that
high-level concepts (honesty, morality, emotion) have linear
representations in activation space, extractable via contrastive pairs.
Abliteration applies this methodology to the "refusal" concept.

**Refusal as a linear direction.** @arditi2024refusal identified a
single refusal direction via mean-difference of activations on harmful
versus harmless prompts, and demonstrated both inference-time steering
and permanent weight orthogonalization across Llama, Mistral, Gemma, and
Qwen families.

**Alignment brittleness.** @yang2023finetuning showed that even benign
fine-tuning (e.g., on cooking data) partially removes safety alignment,
and @yang2023shadow demonstrated that $\sim$`<!-- -->`{=html}100
fine-tuning examples suffice for full bypass.

**Defense: Circuit Breakers.** @zou2024circuitbreakers proposed
Representation Rerouting (RR): instead of training the model to output a
refusal, train it to map harmful inputs to a random uninformative
representation, so harmful content cannot be generated coherently even
after ablation.

**Gap.** No prior work has (a) systematically identified which layers
are load-bearing for refusal, (b) tested whether the refusal direction
transfers cross-model, (c) demonstrated an adaptive attack on Circuit
Breakers, or (d) proposed multi-layer redundancy as a defense. We
address all four.

# Hypothesis

1.  Refusal signal is *not* uniformly distributed: a small subset of
    layers ($\leq$`<!-- -->`{=html}4 of 32) accounts for the majority of
    refusal behavior.

2.  Refusal directions are *partially* but not fully transferable across
    model families, reflecting architecture-specific alignment.

3.  Circuit Breakers is vulnerable to an adaptive attacker who extracts
    a new direction from the defended model using the same contrastive
    method.

4.  Forcing refusal to be encoded uniformly across all layers
    (multi-layer redundancy) increases attack cost but at a measurable
    capability cost, revealing a quantifiable robustness--capability
    Pareto frontier.

# Datasets

**Attack evaluation.** AdvBench [@zou2023universal]: 500 harmful
instructions spanning violence, misinformation, and illegal activity.

**Contrastive activation extraction.** AdvBench (harmful) paired with
the Alpaca instruction dataset [@alpaca] (harmless), matched in length.

**Capability evaluation.** MMLU [@hendrycks2021mmlu] (5-shot, 57 tasks)
and WikiText-2 perplexity.

**Models.** Llama-3.1-8B-Instruct and Mistral-7B-Instruct-v0.3, both
publicly available on HuggingFace and runnable in BF16 within 20 GB
VRAM.

# Methods

**Refusal direction extraction.** For each layer $\ell$, compute
$\hat{r}_\ell = \bar{a}_\ell^{\text{harm}} - \bar{a}_\ell^{\text{safe}}$
where $\bar{a}_\ell$ is the mean last-token residual stream activation.
Normalize to unit length.

**Activation steering.** At inference time, subtract
$\alpha \hat{r}_\ell$ from the residual stream at layer $\ell$ via a
forward hook. Non-destructive; useful for rapid iteration.

**Weight orthogonalization (abliteration).** For each weight matrix $W$,
compute $W \leftarrow W - (W\hat{r}_\ell)\hat{r}_\ell^\top$. Permanent;
used for final evaluations.

**Baselines.** (1) unmodified aligned model, (2) activation steering,
(3) full abliteration (all layers), (4) Circuit Breakers defense.

**Novel defense: multi-layer redundancy.** Fine-tune the aligned model
with an auxiliary loss that maximizes the refusal direction magnitude
uniformly across all layers, forcing no single layer to be critical. An
attacker must then ablate all 32 layers successfully.

# Experiments

**E1: Baseline reproduction.** Apply abliteration to
Llama-3.1-8B-Instruct and Mistral-7B-Instruct. Report refusal rate on
AdvBench and MMLU before/after.

**E2: Layer sensitivity analysis.** Ablate one layer at a time. Plot
refusal rate vs. layer index to identify load-bearing layers.

**E3: Direction transferability.** Extract $\hat{r}$ from Llama, apply
it to Mistral without re-extraction. Compare refusal reduction to the
model-specific baseline.

**E4: Partial ablation sweep.** Remove 10%, 25%, 50%, 75%, 100% of the
direction magnitude. Plot refusal rate and MMLU accuracy jointly to
visualize the robustness--capability curve.

**E5: Circuit Breakers + adaptive attack.** Implement the RR defense on
Mistral-7B. Test naive abliteration; then apply the adaptive attack
(extract a new direction from the defended model's activations). Report
whether refusal is recovered.

**E6: Multi-layer redundancy defense.** Fine-tune Llama-3.1-8B with the
redundancy loss. Test full abliteration (all layers) and report the
number of layers an attacker must target before refusal drops below 50%.

# Expected Outcome

E2 will show that 2--4 layers account for most refusal behavior in
vanilla models. E3 will show partial but imperfect cross-model transfer,
confirming that alignment is architecture-specific. E5 will show that an
adaptive attacker can defeat Circuit Breakers in the white-box setting,
suggesting the defense must go beyond rerouting. E6 will show that
multi-layer redundancy raises the attack cost (more layers must be
ablated) but at a quantifiable MMLU cost, yielding a concrete Pareto
frontier.

The principal contribution is empirical: a comprehensive map of the
geometric arms race between ablation attacks and safety defenses, with
the first measurement of the robustness--capability tradeoff under
adaptive attack conditions.
