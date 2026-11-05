"""Choose one process-unit configuration at each of two stages."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import qubitor
from _common import run
opts=['Standard','Energy-efficient','High-throughput']; m=qubitor.Model('process_train_selection'); x=m.binary_vars('unit',(2,3))
for i in range(2): m.one_hot(x[i],name=f'stage_{i}_configuration')
for i in range(2):
    for j,c in enumerate([[3,2,5],[4,3,2]][i]): m.add_linear(x[i][j],c)
# High-throughput first stage paired with standard second stage incurs a mismatch.
m.add_quadratic(x[0][2],x[1][0],6)
run(m,'Chemical process / Process-train configuration',penalty=10,details=lambda b:{'stage_1':opts[next(j for j in range(3) if b[j])],'stage_2':opts[next(j for j in range(3) if b[3+j])]})
