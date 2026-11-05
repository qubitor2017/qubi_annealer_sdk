"""Choose compatible gear ratios for two gearbox stages (synthetic engineering data)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import qubitor
from _common import run
ratios=['1.5','2.0','2.5']; stage_cost=[3,2,4]
m=qubitor.Model('gear_train_selection'); x=m.binary_vars('ratio',(2,3))
for s in range(2): m.one_hot(x[s],name=f'stage_{s}_ratio')
for s in range(2):
    for r,c in enumerate(stage_cost): m.add_linear(x[s][r],c)
# Avoid extreme ratio mismatch between the two stages.
for a in range(3):
    for b in range(3):
        if abs(a-b)>1: m.add_quadratic(x[0][a],x[1][b],8)
run(m,'Mechanical engineering / Gear-train ratio selection',penalty=10,details=lambda b:{'stage_ratios':[ratios[next(i for i in range(3) if b[s*3+i])] for s in range(2)]})
