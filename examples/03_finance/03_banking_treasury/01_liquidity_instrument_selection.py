"""Select treasury instruments to meet a target liquidity amount at minimum cost."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import qubitor
from _common import run
liquidity=[2,3,4]; cost=[1,3,5]; target=5
m=qubitor.Model('liquidity_instrument_selection'); x=m.binary_vars('instrument',3)
for i,c in enumerate(cost): m.add_linear(x[i],c)
m.add_constraint(sum(liquidity[i]*x[i] for i in range(3))==target,name='liquidity_target')
run(m,'Finance / Banking & treasury liquidity selection',penalty=20,details=lambda b:{'selected_instruments':[i for i,v in enumerate(b) if v],'liquidity':sum(liquidity[i]*b[i] for i in range(3)),'warning':'Synthetic operational example; not financial advice.'})
