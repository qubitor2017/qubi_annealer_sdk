"""Select exactly two features, rewarding predictive score and penalising redundancy."""
import qubitor
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import run
features=['age','signal_A','signal_B','marker_C','marker_D']; score=[0.7,0.9,0.8,0.6,0.85]
redundancy={(1,2):0.8,(2,4):0.3,(1,4):0.2}
m=qubitor.Model('feature_selection'); x=m.binary_vars('feature',5)
for i,s in enumerate(score): m.add_linear(x[i],-s)
for (i,j),v in redundancy.items(): m.add_quadratic(x[i],x[j],v)
m.add_constraint(sum(x)==2,name='select_two_features')
run(m,'AI / Feature selection (synthetic scores)',penalty=10,details=lambda b:{'selected_features':[features[i] for i,v in enumerate(b) if v]})
