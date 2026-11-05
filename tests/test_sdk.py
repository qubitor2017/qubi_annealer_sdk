import unittest
import qubitor

class SDKTests(unittest.TestCase):
    def test_direct_qubo_and_exact_backend(self):
        q = qubitor.from_qubo([[-1, -1], [-1, -1]])
        r = qubitor.solve(q, backend='mock_exact')
        self.assertEqual(r.solution, [1, 1])
        self.assertEqual(r.objective, -4.0)

    def test_builder_one_hot_compiles_symmetric(self):
        m = qubitor.Model('onehot')
        x = m.binary_vars('x', 3)
        m.minimize(0)
        for i, v in enumerate(x): m.add_linear(v, [3, 1, 2][i])
        m.one_hot(x, name='choose_one')
        q = qubitor.compile(m, penalty=10)
        q.validate(require_symmetric=True)
        r = qubitor.solve(q, backend='mock_exact')
        self.assertEqual(sum(r.solution), 1)
        self.assertEqual(r.solution, [0, 1, 0])

    def test_expression_constraint(self):
        m = qubitor.Model()
        a = m.binary_var('a'); b = m.binary_var('b')
        m.minimize(3*a + 1*b)
        m.add_constraint(a + b == 1)
        q = qubitor.compile(m, penalty=10)
        r = qubitor.solve(q, backend='mock_exact')
        self.assertEqual(sum(r.solution), 1)
        self.assertEqual(r.solution, [0, 1])

    def test_ising_roundtrip_energy_order(self):
        i = qubitor.from_ising(h={0:-1,1:0.3}, J={(0,1):-0.5}, n=2)
        q = qubitor.compile(i)
        self.assertTrue(q.validate(require_symmetric=True))

if __name__ == '__main__': unittest.main()
