"""Select a small basket of assets to approximate target index weights (binary selection toy)."""
import qubitor
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import run
assets=['A','B','C','D']; target=[0.40,0.30,0.20,0.10]; k=2
# With equal selected weights, minimise squared distance to target; add diversity preference.
m=qubitor.Model('index_tracking_selection'); x=m.binary_vars('asset',4)
# Expand sum_i (0.5*x_i - target_i)^2; x_i^2=x_i.
for i,t in enumerate(target): m.add_linear(x[i],0.25-t)
m.add_constraint(sum(x)==k,name='select_two')
m.minimize(0*x[0])
run(m,'Finance / Index-tracking asset selection (toy)',penalty=10,details=lambda b:{'selected_assets':[assets[i] for i,v in enumerate(b) if v],'target_weights':target,'warning':'Binary equal-weight proxy only; not continuous index tracking.'})
