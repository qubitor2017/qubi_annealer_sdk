# Two customer model-input options

Qubitor SDK 2.0 exposes the same two supported entry paths as SDK 1.2. Both converge on a validated,
symmetric `QuboModel` and then use the same backend submission path.

## Option A — model-building API

Customers define binary variables, a linear/quadratic objective and equality
constraints. The SDK compiles this supported subset into a symmetric QUBO.

```python
import qubitor

m = qubitor.Model("selection")
x = m.binary_vars("x", 3)
m.minimize(3*x[0] + x[1] + 2*x[2])
m.add_quadratic(x[0], x[2], 0.5)
m.add_constraint(x[0] + x[1] + x[2] == 1, name="one_selected")

qubo = qubitor.compile(m, penalty=10.0)
qubo.validate(require_symmetric=True)
result = qubitor.solve(qubo, backend="n512", port="/dev/ttyUSB0")
```

Available builder methods include `binary_var`, `binary_vars`, `minimize`,
`maximize`, `add_linear`, `add_quadratic`, `add_constraint` and `one_hot`.

Equality constraints are encoded with a positive finite penalty:
`penalty * (lhs - rhs)**2`. The caller must choose a penalty large enough to
make constraint violations unattractive relative to objective improvements.

## Option B — direct model input

### B1. Symmetric QUBO matrix

```python
Q = [[-2.0, 0.5], [0.5, -1.0]]
qubo = qubitor.from_qubo(Q, offset=0.0)
result = qubitor.solve(qubo, backend="n512", port="/dev/ttyUSB0")
```

A sparse mapping is also accepted, keyed by `(row, column)`, with `n=` supplied:

```python
qubo = qubitor.from_qubo({(0,0):-2, (0,1):0.5,
                           (1,0):0.5, (1,1):-1}, n=2)
```

The matrix convention is `E(x) = offset + x.T @ Q @ x`. The SDK rejects
non-square, non-finite, out-of-range and asymmetric input. It does not silently
symmetrise customer matrices.

### B2. Ising coefficients

```python
ising = qubitor.from_ising(
    h={0: -1.0, 1: 0.25},
    J={(0, 1): -0.75},
    n=2,
    offset=0.0,
)
qubo = qubitor.compile(ising)  # validated Ising -> symmetric QUBO conversion
result = qubitor.solve(qubo, backend="n512", port="/dev/ttyUSB0")
```

The Ising convention is `E(s) = offset + sum(h[i]*s[i]) +
sum(J[i,j]*s[i]*s[j])`, where each spin is in `{-1, +1}`. The SDK validates
field/coupler indices and finite coefficients before conversion.

## Shared backend submission

Use `qubitor.solve(model, backend="n512", port=...)` or
`backend="n1024"`. The default `mock_exact` backend is only a small-model local
test backend (up to 24 variables), not a hardware-performance backend. The
N=512 and N=1024 hardware paths remain subject to the supplied board, bitstream,
UART and coefficient-range requirements.

## Deliberate scope limits

Option A currently supports binary variables, linear/quadratic objective terms
and equality constraints. Inequalities, continuous/general integer variables,
automatic slack-variable conversion and arbitrary MILP/MIQP import are not
implemented. Option B accepts QUBO and Ising models, not arbitrary solver file
formats. PUBO remains a separate host-side quadratization path.
