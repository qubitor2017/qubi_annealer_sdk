"""Map three tasks to three compute nodes with communication affinity rewards."""
import qubitor
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import run
tasks=['Preprocess','Solve','Visualise']; nodes=['Node-1','Node-2','Node-3']; cost=[[1,3,4],[3,1,2],[4,2,1]]
m=qubitor.Model('hpc_task_mapping'); x=m.binary_vars('task_node',(3,3))
for i in range(3): m.one_hot(x[i],name=f'task_{i}_node')
for i in range(3):
    for j in range(3): m.add_linear(x[i][j],cost[i][j])
# Reward co-location of communicating task pairs.
m.add_quadratic(x[0][0],x[1][0],-1.5); m.add_quadratic(x[0][1],x[1][1],-1.5)
run(m,'Science & HPC / Task-to-node mapping',penalty=10,details=lambda b:{tasks[i]:nodes[next(j for j in range(3) if b[i*3+j])] for i in range(3)})
