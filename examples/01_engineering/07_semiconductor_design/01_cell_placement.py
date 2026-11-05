"""Place three cells on three sites with assignment costs and pairwise wire proxy."""
import qubitor
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import run
cells=['C1','C2','C3']; sites=['S1','S2','S3']; place=[[1,3,5],[2,1,4],[4,2,1]]
m=qubitor.Model('cell_placement'); x=m.binary_vars('place',(3,3))
for i in range(3): m.one_hot(x[i],name=f'cell_{i}_site')
for j in range(3): m.one_hot([x[i][j] for i in range(3)],name=f'site_{j}_cell')
for i in range(3):
    for j in range(3): m.add_linear(x[i][j],place[i][j])
# Encourage C1 and C2 to occupy nearby/paired sites (illustrative coupling).
m.add_quadratic(x[0][0],x[1][1],-1.0); m.add_quadratic(x[0][1],x[1][0],-1.0)
run(m,'Semiconductor / Cell placement (small assignment proxy)',penalty=10,details=lambda b:{cells[i]:sites[next(j for j in range(3) if b[i*3+j])] for i in range(3)})
