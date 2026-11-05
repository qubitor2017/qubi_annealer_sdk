"""Allocate three robots to three tasks, one task per robot and one robot per task."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import qubitor
from _common import run
robots=['R1','R2','R3']; tasks=['Inspect','Carry','Assemble']; cost=[[2,5,4],[4,2,3],[3,4,1]]
m=qubitor.Model('robot_task_allocation'); x=m.binary_vars('robot_task',(3,3))
for i in range(3): m.one_hot(x[i],name=f'robot_{i}_task')
for j in range(3): m.one_hot([x[i][j] for i in range(3)],name=f'task_{j}_robot')
for i in range(3):
    for j in range(3): m.add_linear(x[i][j],cost[i][j])
run(m,'Robotics / Robot-task allocation',penalty=10,details=lambda b:{robots[i]:tasks[next(j for j in range(3) if b[i*3+j])] for i in range(3)})
