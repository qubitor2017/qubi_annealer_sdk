"""Maximum independent set: reward selected vertices, penalise adjacent selections."""
import qubitor
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import run
edges=[(0,1),(1,2),(2,3),(3,0),(1,3)]
n=4; reward=1.0; penalty=3.0
Q={(i,i):-reward for i in range(n)}
for u,v in edges:
    Q[(u,v)]=Q.get((u,v),0)+penalty/2; Q[(v,u)]=Q.get((v,u),0)+penalty/2
qubo=qubitor.from_qubo(Q,n=n)
run(qubo,'Computational complexity / Maximum Independent Set',details=lambda x:{'selected_vertices':[i for i,b in enumerate(x) if b],'independent_check':all(not(x[u] and x[v]) for u,v in edges)})
