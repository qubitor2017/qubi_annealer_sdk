"""Select one component from each of three circuit positions."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import qubitor
from _common import run
parts=[['R-low','R-precision'],['C-small','C-stable'],['L-compact','L-highQ']]; costs=[2,4,3,5,3,6]
m=qubitor.Model('circuit_component_selection'); x=m.binary_vars('part',6)
for g in range(3): m.one_hot(x[2*g:2*g+2],name=f'position_{g}')
for i,c in enumerate(costs): m.add_linear(x[i],c)
m.add_quadratic(x[1],x[3],-0.5)
run(m,'Electrical & electronics / Circuit component selection',penalty=10,details=lambda b:{f'position_{g+1}':parts[g][next(j for j in range(2) if b[g*2+j])] for g in range(3)})
