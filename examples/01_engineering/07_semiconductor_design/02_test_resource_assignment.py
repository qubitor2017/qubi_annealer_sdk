"""Assign devices to test stations with station exclusivity."""
import qubitor
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import run
devices=['D1','D2','D3']; stations=['ATE-1','ATE-2','ATE-3']; cost=[[2,5,4],[4,2,5],[5,4,1]]
m=qubitor.Model('wafer_test_assignment'); x=m.binary_vars('device_station',(3,3))
for i in range(3): m.one_hot(x[i],name=f'device_{i}_station')
for j in range(3): m.one_hot([x[i][j] for i in range(3)],name=f'station_{j}_device')
for i in range(3):
    for j in range(3): m.add_linear(x[i][j],cost[i][j])
run(m,'Semiconductor manufacturing / Test-station assignment',penalty=10,details=lambda b:{devices[i]:stations[next(j for j in range(3) if b[i*3+j])] for i in range(3)})
