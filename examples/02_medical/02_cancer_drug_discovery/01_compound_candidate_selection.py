"""Select candidate compounds from synthetic scores; research toy, not a drug recommendation."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import qubitor
from _common import run
compounds=['C-01','C-02','C-03','C-04']; score=[0.8,0.7,0.95,0.6]
m=qubitor.Model('compound_candidate_selection'); x=m.binary_vars('compound',4)
for i,s in enumerate(score): m.add_linear(x[i],-s)
m.add_constraint(sum(x)==2,name='select_two_candidates')
m.add_quadratic(x[0],x[2],0.4)
run(m,'Cancer drug discovery / Compound candidate selection (synthetic)',penalty=10,details=lambda b:{'selected_candidates':[compounds[i] for i,v in enumerate(b) if v],'warning':'Synthetic scores only; not biomedical evidence or a clinical recommendation.'})
