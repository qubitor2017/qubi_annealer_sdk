"""Assign three delivery jobs to three vehicles, one job per vehicle."""
import qubitor
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import run
jobs=['North','East','West']; vehicles=['Van-1','Van-2','Van-3']; cost=[[4,7,5],[6,3,8],[5,6,4]]
m=qubitor.Model('delivery_assignment'); x=m.binary_vars('assign',(3,3))
for i in range(3): m.one_hot(x[i],name=f'job_{i}_assigned')
for j in range(3): m.one_hot([x[i][j] for i in range(3)],name=f'vehicle_{j}_used_once')
for i in range(3):
    for j in range(3): m.add_linear(x[i][j],cost[i][j])
run(m,'Logistics / Delivery-job to vehicle assignment',penalty=10,details=lambda b:{'assignments':{jobs[i]:vehicles[next(j for j in range(3) if b[i*3+j])] for i in range(3)}})
