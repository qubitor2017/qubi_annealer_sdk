"""Tiny unit-commitment-style on/off selection with an exact demand equality."""
import qubitor
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import run
capacity=[2,3,4]; cost=[3,4,7]; demand=5
m=qubitor.Model('generator_commitment'); x=m.binary_vars('generator_on',3)
for i in range(3): m.add_linear(x[i],cost[i])
m.add_constraint(sum(capacity[i]*x[i] for i in range(3))==demand,name='meet_demand')
run(m,'Energy / Generator commitment (binary toy)',penalty=20,details=lambda b:{'online_generators':[i for i,v in enumerate(b) if v],'delivered_capacity':sum(capacity[i]*b[i] for i in range(3))})
