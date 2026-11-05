"""Choose one cooling configuration per compute module (illustrative cost/thermal score)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import qubitor
from _common import run
modules=['CPU','GPU']; modes=['Air','Liquid','Immersion']; cost=[[4,6,8],[5,7,9]]
m=qubitor.Model('cooling_configuration'); x=m.binary_vars('cooling',(2,3))
for i in range(2): m.one_hot(x[i],name=f'module_{i}_cooling')
for i in range(2):
    for j in range(3): m.add_linear(x[i][j],cost[i][j])
# If both modules use air, add a thermal-load penalty.
m.add_quadratic(x[0][0],x[1][0],5)
run(m,'Thermal engineering / Cooling configuration',penalty=10,details=lambda b:{modules[i]:modes[next(j for j in range(3) if b[i*3+j])] for i in range(2)})
