"""Select a two-marker panel from synthetic biomarker scores; not a diagnostic model."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import qubitor
from _common import run
markers=['Marker-A','Marker-B','Marker-C','Marker-D']; score=[0.7,0.9,0.85,0.6]
m=qubitor.Model('biomarker_panel'); x=m.binary_vars('marker',4)
for i,s in enumerate(score): m.add_linear(x[i],-s)
m.add_constraint(sum(x)==2,name='panel_size')
m.add_quadratic(x[1],x[2],0.5)
run(m,'Precision oncology / Biomarker panel selection (synthetic)',penalty=10,details=lambda b:{'selected_markers':[markers[i] for i,v in enumerate(b) if v],'warning':'Synthetic example only; not validated for diagnosis or patient care.'})
