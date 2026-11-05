"""Assign each production job to exactly one machine; machine costs are illustrative."""
import qubitor
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import run
jobs=['Housing','Shaft','Bracket']; machines=['Mill-A','Mill-B']; cost=[[5,7],[4,3],[6,5]]
m=qubitor.Model('job_machine_assignment'); x=m.binary_vars('job_machine',(3,2))
for i in range(3): m.one_hot(x[i],name=f'job_{i}_machine')
for i in range(3):
    for j in range(2): m.add_linear(x[i][j],cost[i][j])
run(m,'Manufacturing / Job-to-machine assignment',penalty=10,details=lambda b:{'assignments':{jobs[i]:machines[next(j for j in range(2) if b[i*2+j])] for i in range(3)}})
