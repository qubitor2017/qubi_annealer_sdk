"""Choose antenna configurations for two links with interference penalty."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import qubitor
from _common import run
configs=['Low-band','Mid-band','High-band']; m=qubitor.Model('antenna_configuration'); x=m.binary_vars('link_config',(2,3))
for i in range(2): m.one_hot(x[i],name=f'link_{i}_config')
for i in range(2):
    for j,c in enumerate([[2,3,5],[3,2,4]][i]): m.add_linear(x[i][j],c)
# Both links on the same band may interfere.
for c in range(3): m.add_quadratic(x[0][c],x[1][c],8)
run(m,'RF / Microwave / Photonics / Antenna-band configuration',penalty=10,details=lambda b:{'link_1':configs[next(j for j in range(3) if b[j])],'link_2':configs[next(j for j in range(3) if b[3+j])]})
