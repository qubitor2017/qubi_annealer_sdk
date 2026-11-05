"""Three-colouring as node-colour one-hot constraints plus edge conflicts."""
import qubitor
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import run
edges=[(0,1),(1,2),(2,0),(2,3)]; n=4; k=3; p=8.0
m=qubitor.Model('graph_coloring')
x=m.binary_vars('color',(n,k))
for i in range(n): m.one_hot(x[i],name=f'one_color_node_{i}')
for u,v in edges:
    for c in range(k): m.add_quadratic(x[u][c],x[v][c],p)
m.minimize(0*x[0][0])
run(m,'Computational complexity / Graph Coloring',penalty=p,details=lambda b:{'color_by_node':[next((c for c in range(k) if b[i*k+c]),None) for i in range(n)],'valid':all(not(b[u*k+c] and b[v*k+c]) for u,v in edges for c in range(k))})
