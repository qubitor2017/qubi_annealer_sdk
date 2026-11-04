from abc import ABC, abstractmethod
from ..qubo import QuboModel
from ..result import SolveResult

class Backend(ABC):
    name = 'abstract'
    max_variables = None
    supports_sparse = True

    @abstractmethod
    def solve(self, model: QuboModel, **kwargs) -> SolveResult:
        raise NotImplementedError
