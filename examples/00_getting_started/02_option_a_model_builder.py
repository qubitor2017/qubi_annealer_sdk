"""Option A: binary variables, objective and equality constraints."""
import qubitor
m=qubitor.Model('option_a_demo'); x=m.binary_vars('x',4)
m.minimize(3*x[0]+1*x[1]+2*x[2]+4*x[3])
m.add_quadratic(x[0],x[3],-0.5)
m.add_constraint(x[0]+x[1]+x[2]+x[3]==2,name='choose_two')
r=qubitor.solve(m,backend='mock_exact',penalty=10)
print('Option A result:',r.solution,'energy:',r.objective)
