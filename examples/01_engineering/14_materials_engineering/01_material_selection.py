"""Choose material grades for two components using synthetic cost/performance scores."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import qubitor
from _common import run
materials=['Aluminium','Steel','Titanium']; components=['Frame','Joint']; cost=[[3,4,7],[2,5,8]]
m=qubitor.Model('material_selection'); x=m.binary_vars('material',(2,3))
for i in range(2): m.one_hot(x[i],name=f'component_{i}_material')
for i in range(2):
    for j in range(3): m.add_linear(x[i][j],cost[i][j])
# Avoid an illustrative galvanic/material mismatch for one pair.
m.add_quadratic(x[0][0],x[1][1],5)
run(m,'Materials engineering / Material selection',penalty=10,details=lambda b:{components[i]:materials[next(j for j in range(3) if b[i*3+j])] for i in range(2)})
