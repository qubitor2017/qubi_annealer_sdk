"""Option B: direct Ising fields and couplers, converted to symmetric QUBO."""
import qubitor
ising=qubitor.from_ising(h={0:-1.0,1:0.25,2:0.5},J={(0,1):-0.75,(1,2):0.4},n=3)
qubo=qubitor.compile(ising)
r=qubitor.solve(qubo,backend='mock_exact')
print('Option B Ising result:',r.solution,'energy:',r.objective)
