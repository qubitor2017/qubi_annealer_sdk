"""Allocate one crop to each field and each crop to at most one field (one-to-one toy)."""
import qubitor
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import run
fields=['Field-1','Field-2','Field-3']; crops=['Rice','Maize','Soy']; profit=[[8,6,7],[5,9,6],[7,5,8]]
m=qubitor.Model('crop_field_allocation'); x=m.binary_vars('crop_field',(3,3))
for i in range(3): m.one_hot(x[i],name=f'field_{i}_crop')
for j in range(3): m.one_hot([x[i][j] for i in range(3)],name=f'crop_{j}_field')
for i in range(3):
    for j in range(3): m.add_linear(x[i][j],-profit[i][j])
run(m,'Agriculture / Crop-to-field allocation (synthetic profit)',penalty=10,details=lambda b:{fields[i]:crops[next(j for j in range(3) if b[i*3+j])] for i in range(3)})
