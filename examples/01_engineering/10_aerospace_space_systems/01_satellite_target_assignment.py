"""Assign three observation targets to three satellites."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import qubitor
from _common import run
sats=['SAT-A','SAT-B','SAT-C']; targets=['T1','T2','T3']; cost=[[2,4,5],[3,2,4],[4,3,1]]
m=qubitor.Model('satellite_target_assignment'); x=m.binary_vars('sat_target',(3,3))
for i in range(3): m.one_hot(x[i],name=f'satellite_{i}_target')
for j in range(3): m.one_hot([x[i][j] for i in range(3)],name=f'target_{j}_satellite')
for i in range(3):
    for j in range(3): m.add_linear(x[i][j],cost[i][j])
run(m,'Aerospace / Satellite-to-target assignment',penalty=10,details=lambda b:{sats[i]:targets[next(j for j in range(3) if b[i*3+j])] for i in range(3)})
