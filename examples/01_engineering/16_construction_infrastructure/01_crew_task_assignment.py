"""Assign three crews to three tasks at minimum synthetic cost."""
import qubitor
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import run
crews=['Crew-A','Crew-B','Crew-C']; tasks=['Electrical','Piping','Civil']; cost=[[4,7,5],[6,3,8],[5,6,4]]
m=qubitor.Model('crew_task_assignment'); x=m.binary_vars('crew_task',(3,3))
for i in range(3): m.one_hot(x[i],name=f'crew_{i}_task')
for j in range(3): m.one_hot([x[i][j] for i in range(3)],name=f'task_{j}_crew')
for i in range(3):
    for j in range(3): m.add_linear(x[i][j],cost[i][j])
run(m,'Construction / Crew-to-task assignment',penalty=10,details=lambda b:{crews[i]:tasks[next(j for j in range(3) if b[i*3+j])] for i in range(3)})
