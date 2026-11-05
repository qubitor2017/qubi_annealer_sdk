"""Choose one component per subsystem and penalise incompatible combinations."""
import qubitor
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import run
parts=[['P1-lowcost','P1-highperf'],['P2-light','P2-strong'],['P3-basic','P3-premium']]
cost=[3,6,2,5,2,4]; m=qubitor.Model('engineering_component_selection'); x=m.binary_vars('part',6)
for group in range(3): m.one_hot(x[2*group:2*group+2],name=f'subsystem_{group}')
for i,c in enumerate(cost): m.add_linear(x[i],c)
# Incompatible pair: high-performance first part with lightweight second part.
m.add_quadratic(x[1],x[2],12)
run(m,'Engineering design / Component selection with compatibility',penalty=12,details=lambda b:{'selected_components':[parts[g][next(i for i in range(2) if b[g*2+i])] for g in range(3)]})
