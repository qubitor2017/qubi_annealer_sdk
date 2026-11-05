"""Select a fixed-size ensemble from candidate models with pairwise diversity rewards."""
import qubitor
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import run
models=['M1','M2','M3','M4']; loss=[0.30,0.25,0.28,0.22]
m=qubitor.Model('ensemble_selection'); x=m.binary_vars('model',4)
for i,v in enumerate(loss): m.add_linear(x[i],v)
# Small negative couplings reward diverse pairs in this toy objective.
m.add_quadratic(x[0],x[2],-0.05); m.add_quadratic(x[1],x[3],-0.04)
m.add_constraint(sum(x)==2,name='ensemble_size')
run(m,'AI / Model ensemble selection',penalty=5,details=lambda b:{'selected_models':[models[i] for i,v in enumerate(b) if v]})
