"""Select one option per research case; purely illustrative combinatorial selection, not treatment advice."""
import qubitor
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import run
cases=['Case-A','Case-B']; options=['Option-1','Option-2','Option-3']; score=[[8,6,9],[7,9,5]]
m=qubitor.Model('research_option_selection'); x=m.binary_vars('option',(2,3))
for i in range(2): m.one_hot(x[i],name=f'case_{i}_one_option')
for i in range(2):
    for j in range(3): m.add_linear(x[i][j],-score[i][j])
run(m,'Biomedical research / Option selection (synthetic scores)',penalty=10,details=lambda b:{cases[i]:options[next(j for j in range(3) if b[i*3+j])] for i in range(2)})
