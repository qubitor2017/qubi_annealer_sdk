# Qubitor SDK 2.0.0 API overview

## Two model-input routes

| Route | Customer supplies | SDK responsibility | Output to backend |
|---|---|---|---|
| Option A: model builder | Binary variables, linear/quadratic objective, equality constraints | Validate builder model; apply equality penalties; compile symmetric QUBO | `QuboModel` |
| Option B1: direct QUBO | Dense matrix or sparse `(i,j) -> coefficient` map | Validate dimensions, indices, finite values and symmetry | `QuboModel` |
| Option B2: direct Ising | `h` fields, `J` couplers, dimension and optional offset | Validate spin indices/coefficients; convert Ising energy to symmetric QUBO | `QuboModel` |

All routes use `qubitor.solve(model, backend=...)` for backend submission.

## Option A symbols

- `Model(name)`
- `Model.binary_var(name)` / `Model.binary_vars(name, shape)`
- `Model.minimize(expr)` / `Model.maximize(expr)`
- `Model.add_linear(var, coefficient)`
- `Model.add_quadratic(var_a, var_b, coefficient)`
- `Model.add_constraint(expr == rhs, name=...)`
- `Model.one_hot(variables, name=...)`
- `qubitor.compile(model, penalty=...)`

Equality constraints are encoded with `penalty * (lhs-rhs)^2`. The penalty must
be positive and finite; selecting a sufficiently strong penalty remains the
model author's responsibility.

## Option B symbols

- `qubitor.from_qubo(dense_matrix, offset=..., labels=...)`
- `qubitor.from_qubo(sparse_coefficients, n=..., offset=...)`
- `qubitor.from_ising(h=..., J=..., n=..., offset=...)`
- `qubitor.compile(ising_model)`

QUBO energy convention: `offset + x.T @ Q @ x`, with binary `x`.
Ising energy convention: `offset + sum(h[i]*s[i]) + sum(J[i,j]*s[i]*s[j])`,
with spins `s[i]` in `{-1,+1}`. The public direct-QUBO API requires symmetric Q.

## Backends

- `mock_exact`: CPU brute force for small test models (up to 24 variables).
- `n512`: dense N=512 FPGA UART adapter.
- `n1024`: sparse N=1024 FPGA UART adapter.

Hardware is opt-in. The default backend is `mock_exact`.
