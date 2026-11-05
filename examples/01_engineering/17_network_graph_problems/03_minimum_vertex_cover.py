"""Minimum vertex cover: every edge must have at least one selected endpoint."""
import qubitor
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import run
edges=[(0,1),(1,2),(2,3),(3,0),(0,2)]
n=4; p=4.0
Q={(i,i):1.0 for i in range(n)}; offset=p*len(edges)
for u,v in edges:
    Q[(u,u)]=Q.get((u,u),0)-p; Q[(v,v)]=Q.get((v,v),0)-p
    Q[(u,v)]=Q.get((u,v),0)+p/2; Q[(v,u)]=Q.get((v,u),0)+p/2
qubo=qubitor.from_qubo(Q,n=n,offset=offset)
run(qubo,'Computational complexity / Minimum Vertex Cover',details=lambda x:{'cover':[i for i,b in enumerate(x) if b],'all_edges_covered':all(x[u] or x[v] for u,v in edges)})
