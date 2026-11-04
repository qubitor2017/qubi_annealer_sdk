from dataclasses import dataclass, field
from typing import Any

@dataclass
class SolveResult:
    solution: list[int]
    objective: float
    status: str = 'unknown'
    backend: str = 'unknown'
    raw_objective: int | float | None = None
    temperature: int | None = None
    iterations: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def as_dict(self):
        return {'solution': self.solution, 'objective': self.objective, 'status': self.status,
                'backend': self.backend, 'raw_objective': self.raw_objective,
                'temperature': self.temperature, 'iterations': self.iterations,
                'metadata': self.metadata}
