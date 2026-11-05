"""Option B1: supply a symmetric dense or sparse QUBO directly."""
import qubitor

# Energy convention: E(x) = offset + x.T @ Q @ x.
Q = [
    [-2.0, 0.5, 0.0],
    [0.5, -1.0, 1.0],
    [0.0, 1.0, -0.5],
]
qubo = qubitor.from_qubo(Q, offset=0.25, labels=["x0", "x1", "x2"])
qubo.validate(require_symmetric=True)

# Equivalent sparse form:
# qubo = qubitor.from_qubo({(0,0):-2, (0,1):0.5, (1,0):0.5,
#                           (1,1):-1, (1,2):1, (2,1):1, (2,2):-0.5}, n=3)

result = qubitor.solve(qubo, backend="mock_exact")
print("solution:", result.solution)
print("QUBO energy:", result.objective)
