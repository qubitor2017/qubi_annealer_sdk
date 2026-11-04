"""Deprecated compatibility facade for the historical qubif_sdk API.

New projects should import qubitor. This shim preserves the old Max-Cut demo.
"""
from qubitor.compat.qubif_sdk import AnnealerClient, build_maxcut, decode_maxcut
__all__ = ["AnnealerClient", "build_maxcut", "decode_maxcut"]
