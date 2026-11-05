"""Maximum Cut on a small weighted graph."""
import qubitor
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import run
edges = [(0,1),(1,2),(2,3),(3,0),(0,2)]
qubo = qubitor.build_maxcut(edges, n_nodes=4)
run(qubo, 'Computational complexity / Max-Cut', details=lambda x: {'cut_value': qubitor.decode_maxcut(x, edges), 'partition_A':[i for i,b in enumerate(x) if b==0], 'partition_B':[i for i,b in enumerate(x) if b==1]})
