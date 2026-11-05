"""Select intervention targets from a synthetic interaction network; research toy only."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import qubitor
from _common import run
targets=['T1','T2','T3','T4']; benefit=[0.8,0.9,0.7,0.85]; interactions=[(0,1),(1,2)]
m=qubitor.Model('target_selection'); x=m.binary_vars('target',4)
for i,v in enumerate(benefit): m.add_linear(x[i],-v)
for i,j in interactions: m.add_quadratic(x[i],x[j],0.7)
m.add_constraint(sum(x)==2,name='select_two_targets')
run(m,'Cancer systems biology / Target selection (synthetic network)',penalty=10,details=lambda b:{'selected_targets':[targets[i] for i,v in enumerate(b) if v],'warning':'Synthetic network only; not biological or clinical evidence.'})
