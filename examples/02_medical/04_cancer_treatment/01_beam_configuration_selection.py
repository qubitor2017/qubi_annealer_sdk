"""Select candidate beam configurations from synthetic scores; not a radiotherapy plan."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import qubitor
from _common import run
beams=['B1','B2','B3','B4']; benefit=[0.8,0.9,0.7,0.85]
m=qubitor.Model('beam_configuration_research'); x=m.binary_vars('beam',4)
for i,v in enumerate(benefit): m.add_linear(x[i],-v)
m.add_constraint(sum(x)==2,name='select_two_beam_options')
m.add_quadratic(x[0],x[1],0.6)
run(m,'Cancer treatment research / Beam-option selection (synthetic)',penalty=10,details=lambda b:{'selected_options':[beams[i] for i,v in enumerate(b) if v],'warning':'Not a dose model, treatment plan, or clinical recommendation.'})
