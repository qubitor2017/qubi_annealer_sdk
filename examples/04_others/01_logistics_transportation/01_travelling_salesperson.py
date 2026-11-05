"""Four-city TSP with one city per tour position and one position per city."""
import qubitor
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import run
from _common import one_hot_decode
names=['Depot','A','B','C']; d=[[0,4,6,7],[4,0,5,3],[6,5,0,4],[7,3,4,0]]; n=4; p=20
m=qubitor.Model('tsp'); x=m.binary_vars('visit',(n,n))
for city in range(n): m.one_hot(x[city],name=f'city_{city}_once')
for pos in range(n): m.one_hot([x[city][pos] for city in range(n)],name=f'position_{pos}_once')
for pos in range(n):
    nxt=(pos+1)%n
    for i in range(n):
        for j in range(n):
            if i!=j: m.add_quadratic(x[i][pos],x[j][nxt],d[i][j])
m.minimize(0*x[0][0])
run(m,'Logistics / Travelling Salesperson (4-city toy)',penalty=p,details=lambda b:{'tour':[names[i] for i in one_hot_decode(b,n)],'tour_cost':sum(d[one_hot_decode(b,n)[t]][one_hot_decode(b,n)[(t+1)%n]] for t in range(n))})
