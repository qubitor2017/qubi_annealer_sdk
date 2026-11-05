"""Select pump and valve options with a simple compatibility penalty."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import qubitor
from _common import run
pumps=['P1','P2']; valves=['V1','V2','V3']; m=qubitor.Model('pump_valve_configuration')
x=m.binary_vars('pump',2); y=m.binary_vars('valve',3); m.one_hot(x); m.one_hot(y)
for i,c in enumerate([4,3]): m.add_linear(x[i],c)
for i,c in enumerate([2,4,3]): m.add_linear(y[i],c)
# Pump P2 is incompatible with valve V1 in this toy model.
m.add_quadratic(x[1],y[0],10)
run(m,'Fluid engineering / Pump-valve configuration',penalty=10,details=lambda b:{'pump':pumps[next(i for i in range(2) if b[i])],'valve':valves[next(i for i in range(3) if b[2+i])]})
