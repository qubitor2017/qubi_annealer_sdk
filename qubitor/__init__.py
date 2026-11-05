"""Qubitor FPGA Optimization SDK: QUBO, PUBO, Ising and host-side backends."""
from .model import Model, Var, Expr, sum_expr
from .qubo import QuboModel, IsingModel, compile_model
from .pubo import PuboModel
from .result import SolveResult
from .backends.mock import MockExactBackend
from .backends.serial import Dense512Backend, Sparse1024Backend, SerialFPGA, SerialProtocolError
from .applications.maxcut import build_maxcut, decode_maxcut

__version__ = "2.0.0"


def from_qubo(Q, offset=0.0, labels=None, n=None):
    """Option B: import and validate a symmetric QUBO matrix or sparse coefficient map.

    Energy convention: offset + x.T @ Q @ x. Asymmetric matrices are rejected.
    """
    if isinstance(Q, dict):
        inferred = 1 + max(max(i, j) for i, j in Q) if Q else 0
        return QuboModel.from_sparse(inferred if n is None else n, Q, offset, labels)
    return QuboModel.from_dense(Q, offset, labels)


def from_ising(h, J, n=None, offset=0.0):
    """Option B: import Ising fields/couplers and validate their indices/values."""
    if n is None:
        indices = list(h) + [i for pair in J for i in pair]
        n = max(indices) + 1 if indices else 0
    return IsingModel(dict(h), dict(J), int(n), float(offset)).validate()


def from_pubo(terms, n, offset=0.0, labels=None):
    """Create a PUBO model from {tuple(variable_indices): coefficient}."""
    return PuboModel(int(n), dict(terms), float(offset), labels)


def compile(model, penalty=1000.0):
    """Compile Option A models or convert Option B Ising/PUBO inputs to symmetric QUBO."""
    if isinstance(model, QuboModel):
        return model.validate(require_symmetric=True)
    if isinstance(model, PuboModel):
        return model.quadratize(penalty=penalty)[0]
    if isinstance(model, IsingModel):
        return model.to_qubo()
    if isinstance(model, Model):
        return compile_model(model, penalty=penalty)
    raise TypeError("Expected qubitor.Model, QuboModel, PuboModel or IsingModel.")


def solve(model, backend="mock_exact", *, port=None, scale=None, penalty=1000.0, **kwargs):
    """Compile and solve. Hardware is opt-in via backend='n512' or 'n1024'.

    The default mock_exact backend is intended only for small local examples and
    tests (up to 24 variables). It is not an FPGA performance backend.
    """
    pubo_meta = None
    if isinstance(model, PuboModel):
        q, pubo_meta = model.quadratize(penalty=None if penalty == 1000.0 else penalty)
    else:
        q = compile(model, penalty=penalty)
    effective_scale = float(scale if scale is not None else (2.0 if q.source == "model_builder" else 1.0))
    if isinstance(backend, str):
        serial_kwargs = {k: kwargs[k] for k in ("timeout", "cooling", "seed") if k in kwargs}
        if backend == "mock_exact":
            engine = MockExactBackend()
        elif backend in ("n512", "fpga_n512_dense"):
            engine = Dense512Backend(port=port, scale=effective_scale, **serial_kwargs)
        elif backend in ("n1024", "fpga_n1024_sparse"):
            engine = Sparse1024Backend(port=port, scale=effective_scale, **serial_kwargs)
        elif backend == "auto":
            if q.n <= 512:
                engine = Dense512Backend(port=port, scale=effective_scale, **serial_kwargs)
            elif q.n <= 1024:
                engine = Sparse1024Backend(port=port, scale=effective_scale, **serial_kwargs)
            else:
                raise ValueError("No available Qubitor FPGA backend supports more than 1024 variables.")
        else:
            raise ValueError(f"Unknown backend {backend!r}.")
    else:
        engine = backend
    result = engine.solve(q, **kwargs)
    if pubo_meta is not None:
        result.solution = model.decode(result.solution, pubo_meta)
        result.objective = model.energy(result.solution)
        result.metadata.update({"pubo_quadratization": pubo_meta,
                                "objective_recomputed_from_original_pubo": True})
    return result
