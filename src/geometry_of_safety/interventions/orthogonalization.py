"""Weight orthogonalization (abliteration).

Project the refusal direction r out of every matrix that writes to the residual
stream, so the model can no longer represent it. Permanent; used for final
evaluations. Supports partial removal (E4) and per-layer targeting (E2, E6).

Convention: the proposal writes the update as W <- W - (W r) r^T. For a PyTorch
weight of shape [d_out, d_in] whose output is the residual stream
(d_out = d_model), the equivalent update is W <- W - r r^T W.

Not implemented yet.
"""
