"""Assign one of three channels to each transmitter; adjacent transmitters cannot share a channel."""
import qubitor
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import run
edges=[(0,1),(1,2),(2,3),(0,3)]; n=4; k=3; p=8
m=qubitor.Model('frequency_assignment'); x=m.binary_vars('channel',(n,k))
for i in range(n): m.one_hot(x[i],name=f'tx_{i}_channel')
for u,v in edges:
    for c in range(k): m.add_quadratic(x[u][c],x[v][c],p)
m.minimize(0*x[0][0])
run(m,'Telecommunications / Frequency assignment',penalty=p,details=lambda b:{'channel_by_transmitter':[next((c for c in range(k) if b[i*k+c]),None) for i in range(n)]})
