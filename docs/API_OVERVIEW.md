# API overview

- `qubitor.Model`: binary-variable model builder.
- `qubitor.QuboModel`: symmetric QUBO representation with energy evaluation.
- `qubitor.IsingModel`: Ising representation and conversion.
- `qubitor.PuboModel` / `qubitor.from_pubo`: higher-order binary polynomial representation and host-side quadratization.
- `qubitor.from_qubo`: import dense or sparse QUBO coefficients.
- `qubitor.from_ising`: import Ising fields and couplers.
- `qubitor.compile`: compile supported model representations to QUBO.
- `qubitor.solve`: execute with `mock_exact`, `n512`, `n1024`, `auto`, or a custom backend object.
- `qubitor.build_maxcut` / `decode_maxcut`: Max-Cut helper functions.

For the full examples and limitations, see the repository README.
