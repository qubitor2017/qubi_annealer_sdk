"""Option B: direct symmetric QUBO matrix input."""
import qubitor
Q=[[-2.0,0.5,0.0],[0.5,-1.0,0.25],[0.0,0.25,-1.5]]
qubo=qubitor.from_qubo(Q,offset=0.25)
r=qubitor.solve(qubo,backend='mock_exact')
print('Option B QUBO:',r.solution,'energy:',r.objective)
