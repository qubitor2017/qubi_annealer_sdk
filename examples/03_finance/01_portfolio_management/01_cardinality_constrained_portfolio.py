"""Illustrative equal-weight portfolio selection with return, covariance risk and cardinality."""
import qubitor
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import run
names=['ALPHA','BETA','GAMMA','DELTA']; mu=[0.12,0.10,0.08,0.14]
cov=[[0.040,0.010,0.008,0.015],[0.010,0.030,0.009,0.012],[0.008,0.009,0.025,0.010],[0.015,0.012,0.010,0.050]]
lam=2.0; k=2
m=qubitor.Model('portfolio_selection'); x=m.binary_vars('asset',len(names))
for i in range(len(names)): m.add_linear(x[i],-mu[i]+lam*cov[i][i])
for i in range(len(names)):
    for j in range(i+1,len(names)): m.add_quadratic(x[i],x[j],2*lam*cov[i][j])
m.add_constraint(sum(x)==k,name='cardinality')
m.minimize(0*x[0])
run(m,'Finance / Cardinality-constrained portfolio (toy data)',penalty=10,details=lambda b:{'selected_assets':[names[i] for i,v in enumerate(b) if v],'expected_return_score':sum(mu[i]*b[i] for i in range(4)),'risk_proxy':sum(cov[i][j]*b[i]*b[j] for i in range(4) for j in range(4)),'warning':'Illustrative synthetic inputs; not investment advice or a production portfolio model.'})
