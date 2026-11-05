"""Demonstrate Option A (model builder) and Option B (direct QUBO)."""
import qubitor

# Option A: customer builds variables, objective and equality constraint.
m = qubitor.Model('choose_one')
x = m.binary_vars('x', 3)
m.minimize(3*x[0] + x[1] + 2*x[2])
m.add_constraint(x[0] + x[1] + x[2] == 1, name='choose_exactly_one')
ra = qubitor.solve(m, backend='mock_exact', penalty=20)
print('Option A:', ra.solution, 'energy=', ra.objective)

# Option B: customer supplies an already formulated symmetric QUBO.
q = qubitor.from_qubo([[-3.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, -2.0]])
rb = qubitor.solve(q, backend='mock_exact')
print('Option B:', rb.solution, 'energy=', rb.objective)
