import itertools
import unittest
import qubitor


class ModelInputOptionTests(unittest.TestCase):
    def test_option_a_compiles_symmetric_and_enforces_equality(self):
        m = qubitor.Model("option_a")
        x = m.binary_vars("x", 3)
        m.minimize(3*x[0] + x[1] + 2*x[2])
        m.add_quadratic(x[0], x[2], 0.5)
        m.add_constraint(x[0] + x[1] + x[2] == 1, name="one_hot")
        q = qubitor.compile(m, penalty=10)
        self.assertTrue(q.validate(require_symmetric=True))
        r = qubitor.solve(q, backend="mock_exact")
        self.assertEqual(sum(r.solution), 1)
        self.assertEqual(r.solution, [0, 1, 0])

    def test_option_a_affine_equality_rhs(self):
        m = qubitor.Model("affine_equality")
        x = m.binary_vars("x", 3)
        m.minimize(1*x[0] + 2*x[1] + 3*x[2])
        m.add_constraint(x[0] + x[1] == x[2], name="balance")
        q = qubitor.compile(m, penalty=20)
        q.validate(require_symmetric=True)
        result = qubitor.solve(q)
        self.assertEqual(result.solution, [0, 0, 0])

    def test_option_b_dense_and_sparse_qubo(self):
        dense = qubitor.from_qubo([[-2.0, 0.5], [0.5, -1.0]])
        sparse = qubitor.from_qubo({(0,0):-2.0, (0,1):0.5, (1,0):0.5, (1,1):-1.0}, n=2)
        self.assertEqual(dense.energy([1, 1]), sparse.energy([1, 1]))
        self.assertEqual(qubitor.solve(dense).solution, qubitor.solve(sparse).solution)

    def test_option_b_rejects_asymmetric_qubo(self):
        with self.assertRaisesRegex(ValueError, "symmetric"):
            qubitor.from_qubo([[0, 1], [0, 0]])

    def test_option_b_ising_to_qubo_preserves_energy(self):
        ising = qubitor.from_ising(h={0:-1.0, 1:0.25}, J={(0,1):-0.75}, n=2, offset=0.3)
        qubo = qubitor.compile(ising)
        for bits in itertools.product((0, 1), repeat=2):
            spins = [2*b - 1 for b in bits]
            e_i = ising.offset + sum(ising.h.get(i, 0)*spins[i] for i in range(2))
            e_i += sum(v*spins[i]*spins[j] for (i,j),v in ising.J.items())
            self.assertAlmostEqual(e_i, qubo.energy(bits), places=9)

    def test_ising_rejects_bad_indices_and_nonfinite_values(self):
        with self.assertRaises(ValueError):
            qubitor.from_ising(h={2: 1.0}, J={}, n=2)
        with self.assertRaises(ValueError):
            qubitor.from_ising(h={0: float('nan')}, J={}, n=1)

    def test_builder_rejects_foreign_variable(self):
        a = qubitor.Model(); xa = a.binary_var("a")
        b = qubitor.Model(); xb = b.binary_var("b")
        with self.assertRaises(ValueError):
            a.add_linear(xb, 1)


if __name__ == "__main__":
    unittest.main()
