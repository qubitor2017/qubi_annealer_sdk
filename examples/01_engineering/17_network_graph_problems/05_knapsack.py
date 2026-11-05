"""0/1 knapsack with binary slack variables for an exact capacity equality."""
import qubitor
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import run
weights=[2,3,4]; values=[3,4,5]; capacity=5
m=qubitor.Model('knapsack')
x=m.binary_vars('item',len(weights)); slack=m.binary_vars('slack',3)
m.maximize(sum(v*x[i] for i,v in enumerate(values)))
# 1,2,2 represent every integer slack from 0 through 5.
m.add_constraint(sum(weights[i]*x[i] for i in range(3))+slack[0]+2*slack[1]+2*slack[2]==capacity,name='capacity')
run(m,'Computational complexity / 0-1 Knapsack',penalty=20,details=lambda b:{'selected_items':[i for i in range(3) if b[i]],'total_weight':sum(weights[i]*b[i] for i in range(3)),'total_value':sum(values[i]*b[i] for i in range(3))})
