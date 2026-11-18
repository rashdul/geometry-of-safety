"""Refusal direction extraction.

For each layer l, r_l = mean(a_l | harmful) - mean(a_l | harmless), where a_l is
the last-token residual stream activation, normalized to unit length.

Not implemented yet.
"""
