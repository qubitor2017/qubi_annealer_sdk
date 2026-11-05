"""Single-machine scheduling: assign each job to one time slot with slot-dependent cost."""
import qubitor
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import run
jobs=['J1','J2','J3']; slots=['t0','t1','t2']; cost=[[2,4,7],[3,2,5],[5,3,2]]
m=qubitor.Model('single_machine_schedule'); x=m.binary_vars('job_slot',(3,3))
for i in range(3): m.one_hot(x[i],name=f'job_{i}_slot')
for t in range(3): m.one_hot([x[i][t] for i in range(3)],name=f'slot_{t}_occupied')
for i in range(3):
    for t in range(3): m.add_linear(x[i][t],cost[i][t])
run(m,'Manufacturing / Single-machine slot scheduling',penalty=10,details=lambda b:{'schedule':{slots[next(t for t in range(3) if b[i*3+t])]:jobs[i] for i in range(3)}})
