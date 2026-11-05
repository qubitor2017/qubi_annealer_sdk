"""Allocate three orders to three execution venues with synthetic transaction costs."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import qubitor
from _common import run
orders=['Order-A','Order-B','Order-C']; venues=['Venue-1','Venue-2','Venue-3']; cost=[[3,2,5],[4,1,3],[2,4,1]]
m=qubitor.Model('execution_venue_allocation'); x=m.binary_vars('order_venue',(3,3))
for i in range(3): m.one_hot(x[i],name=f'order_{i}_venue')
for i in range(3):
    for j in range(3): m.add_linear(x[i][j],cost[i][j])
# Penalise concentrating all flow on the same venue via pairwise interactions.
for i in range(3):
    for j in range(i+1,3): m.add_quadratic(x[i][0],x[j][0],1.0)
run(m,'Finance / Trading & execution venue allocation',penalty=10,details=lambda b:{orders[i]:venues[next(j for j in range(3) if b[i*3+j])] for i in range(3)})
