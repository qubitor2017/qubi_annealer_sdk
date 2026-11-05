"""Deterministic brute-force backend for small tests/examples only."""
from itertools import product
from .base import Backend
from ..result import SolveResult

class MockExactBackend(Backend):
    name = 'mock_exact'
    max_variables = 24
    supports_sparse = True

    def solve(self, model, **kwargs):
        model.validate(max_variables=self.max_variables, require_symmetric=True)
        best_x, best_e = None, float('inf')
        for x in product((0,1), repeat=model.n):
            e = model.energy(x)
            if e < best_e:
                best_x, best_e = list(x), e
        return SolveResult(best_x, best_e, 'optimal_for_test', self.name,
                           raw_objective=best_e, metadata={'warning':'Brute-force test backend; not an FPGA performance solver.'})
