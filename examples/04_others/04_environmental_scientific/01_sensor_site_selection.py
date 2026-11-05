"""Choose exactly two sensor sites with site value and pairwise coverage synergy."""
import qubitor
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import run
sites=['Hill','River','Road','Factory']; value=[4,5,3,4]
m=qubitor.Model('sensor_site_selection'); x=m.binary_vars('sensor',4)
for i,v in enumerate(value): m.add_linear(x[i],-v)
# Pairwise complementarity: these pairs jointly cover a monitoring corridor.
m.add_quadratic(x[0],x[1],-2.0); m.add_quadratic(x[1],x[3],-1.0)
m.add_constraint(sum(x)==2,name='two_sensors')
run(m,'Environment / Sensor-site selection (coverage proxy)',penalty=10,details=lambda b:{'selected_sites':[sites[i] for i,v in enumerate(b) if v]})
