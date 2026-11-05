"""Option B2: supply Ising fields h and couplers J; SDK converts to symmetric QUBO."""
import qubitor

ising = qubitor.from_ising(
    h={0: -1.0, 1: 0.25, 2: 0.5},
    J={(0, 1): -0.75, (1, 2): 0.4},
    n=3,
    offset=0.0,
)
qubo = qubitor.compile(ising)
qubo.validate(require_symmetric=True)

result = qubitor.solve(qubo, backend="mock_exact")
spins = [2 * bit - 1 for bit in result.solution]
print("binary solution:", result.solution)
print("spin solution:", spins)
print("equivalent QUBO energy:", result.objective)
