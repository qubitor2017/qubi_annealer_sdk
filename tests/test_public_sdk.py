import unittest
import qubitor
from qubitor.pubo import PuboModel

class PublicSDKTests(unittest.TestCase):
    def test_version_and_surface(self):
        self.assertEqual(qubitor.__version__, "1.1.0")
        self.assertTrue(hasattr(qubitor, "solve"))
        self.assertFalse(hasattr(qubitor, "Euler"))

    def test_qubo_exact(self):
        q = qubitor.from_qubo([[-1, -1], [-1, -1]])
        r = qubitor.solve(q)
        self.assertEqual(r.solution, [1, 1])
        self.assertEqual(r.objective, -4.0)

    def test_maxcut(self):
        edges = [(0,1),(1,2),(2,3),(3,0),(0,2)]
        q = qubitor.build_maxcut(edges, n_nodes=4)
        r = qubitor.solve(q)
        self.assertEqual(qubitor.decode_maxcut(r.solution, edges), 4)

    def test_pubo_quadratization(self):
        p = PuboModel(3, {(0,1,2):-5.0})
        r = qubitor.solve(p)
        self.assertEqual(r.objective, -5.0)
        self.assertEqual(len(r.solution), 3)

    def test_ising(self):
        i = qubitor.from_ising(h={0:-1,1:0.3}, J={(0,1):-0.5}, n=2)
        q = qubitor.compile(i)
        self.assertTrue(q.validate(require_symmetric=True))

    def test_model_builder(self):
        m = qubitor.Model("onehot")
        x = m.binary_vars("x", 3)
        for v,c in zip(x,[3,1,2]): m.add_linear(v,c)
        m.one_hot(x)
        r = qubitor.solve(m, penalty=10)
        self.assertEqual(r.solution,[0,1,0])

    def test_legacy_import(self):
        from qubif_sdk import build_maxcut, decode_maxcut, AnnealerClient
        J,h = build_maxcut([(0,1),(1,2),(2,0)],3)
        self.assertEqual(len(J),3)
        self.assertEqual(len(h),3)
        self.assertTrue(callable(decode_maxcut))
        self.assertTrue(callable(AnnealerClient))

if __name__ == "__main__":
    unittest.main()
