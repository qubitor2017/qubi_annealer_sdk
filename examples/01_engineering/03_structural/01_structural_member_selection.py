"""Select one member option for each of three structural locations (illustrative cost/stiffness trade-off)."""
import qubitor
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import run
locations=['Beam-A','Beam-B','Column-C']; options=['Light','Heavy']; cost=[[4,7],[3,6],[5,8]]
m=qubitor.Model('structural_member_selection'); x=m.binary_vars('member',(3,2))
for i in range(3): m.one_hot(x[i],name=f'one_member_{i}')
for i in range(3):
    for j in range(2): m.add_linear(x[i][j],cost[i][j])
# A simple compatibility preference between selected heavy members.
for i in range(3):
    for j in range(i+1,3): m.add_quadratic(x[i][1],x[j][1],-0.5)
run(m,'Engineering / Structural member option selection',penalty=10,details=lambda b:{locations[i]:options[next(j for j in range(2) if b[i*2+j])] for i in range(3)})
