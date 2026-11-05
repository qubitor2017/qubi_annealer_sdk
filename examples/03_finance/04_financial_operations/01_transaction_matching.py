"""Match three incoming and outgoing transactions one-to-one at minimum synthetic mismatch cost."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import qubitor
from _common import run
incoming=['IN-1','IN-2','IN-3']; outgoing=['OUT-A','OUT-B','OUT-C']; mismatch=[[1,4,3],[3,1,5],[4,2,1]]
m=qubitor.Model('transaction_matching'); x=m.binary_vars('match',(3,3))
for i in range(3): m.one_hot(x[i],name=f'incoming_{i}_match')
for j in range(3): m.one_hot([x[i][j] for i in range(3)],name=f'outgoing_{j}_match')
for i in range(3):
    for j in range(3): m.add_linear(x[i][j],mismatch[i][j])
run(m,'Finance / Financial operations transaction matching',penalty=10,details=lambda b:{incoming[i]:outgoing[next(j for j in range(3) if b[i*3+j])] for i in range(3)})
