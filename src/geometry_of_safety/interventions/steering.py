"""Activation steering.

At inference time, subtract alpha * r_l from the residual stream at layer l via
a forward hook. Non-destructive, so it is the fast path for iteration.

Not implemented yet.
"""
