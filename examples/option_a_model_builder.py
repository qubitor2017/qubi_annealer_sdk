"""Option A: build a binary optimisation model; SDK compiles it to symmetric QUBO."""
import qubitor

model = qubitor.Model("choose_one_project")
x = model.binary_vars("project", 3)

# Minimise project costs, with a small interaction cost between projects 0 and 2.
model.minimize(3 * x[0] + 1 * x[1] + 2 * x[2])
model.add_quadratic(x[0], x[2], 0.5)

# Exactly one project must be selected.
model.add_constraint(x[0] + x[1] + x[2] == 1, name="select_exactly_one")

# Inspect the compiled symmetric QUBO before submitting it.
qubo = qubitor.compile(model, penalty=10.0)
qubo.validate(require_symmetric=True)
print("Compiled symmetric QUBO:", qubo.Q)
print("Dimension:", qubo.n, "offset:", qubo.offset)

# For a physical device use backend="n512" or backend="n1024" and supply port=...
result = qubitor.solve(qubo, backend="mock_exact")
print("solution:", result.solution)
print("compiled QUBO energy:", result.objective)
print("backend:", result.backend)
