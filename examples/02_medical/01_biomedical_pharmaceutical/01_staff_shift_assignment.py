"""Assign staff to shifts; this is an operational scheduling toy, not a clinical model."""
import qubitor
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import run
staff=['Staff-A','Staff-B','Staff-C']; shifts=['Morning','Afternoon','Night']; cost=[[1,4,5],[3,1,4],[4,3,1]]
m=qubitor.Model('staff_shift_assignment'); x=m.binary_vars('staff_shift',(3,3))
for i in range(3): m.one_hot(x[i],name=f'staff_{i}_one_shift')
for j in range(3): m.one_hot([x[i][j] for i in range(3)],name=f'shift_{j}_covered')
for i in range(3):
    for j in range(3): m.add_linear(x[i][j],cost[i][j])
run(m,'Healthcare operations / Staff-to-shift assignment',penalty=10,details=lambda b:{staff[i]:shifts[next(j for j in range(3) if b[i*3+j])] for i in range(3)})
