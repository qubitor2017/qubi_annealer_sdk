"""QUBO/Ising representations, validation and model-builder compiler."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping
import math


def _finite(value, label):
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{label} must be finite; received {value!r}.")
    return value


@dataclass
class QuboModel:
    """QUBO matrix Q with energy ``offset + x.T @ Q @ x``.

    The public SDK accepts symmetric Q matrices. Off-diagonal polynomial
    coefficients are therefore represented equally in Q[i,j] and Q[j,i].
    """
    Q: dict[tuple[int, int], float]
    n: int
    offset: float = 0.0
    labels: list[str] | None = None
    source: str = 'direct_qubo'

    def validate(self, max_variables=None, require_symmetric=True, tolerance=1e-8):
        if not isinstance(self.n, int) or isinstance(self.n, bool) or self.n < 1:
            raise ValueError('QUBO dimension n must be a positive integer.')
        if max_variables is not None and self.n > max_variables:
            raise ValueError(f'Model has {self.n} variables; backend limit is {max_variables}.')
        _finite(self.offset, 'QUBO offset')
        if self.labels is not None and len(self.labels) != self.n:
            raise ValueError('QUBO labels length must equal the matrix dimension.')
        for key, value in self.Q.items():
            if not (isinstance(key, tuple) and len(key) == 2):
                raise ValueError(f'Invalid QUBO key {key!r}; expected (i, j).')
            i, j = key
            if not isinstance(i, int) or not isinstance(j, int) or not (0 <= i < self.n and 0 <= j < self.n):
                raise ValueError(f'Q index {key} outside 0..{self.n-1}.')
            _finite(value, f'Q[{i},{j}]')
        if require_symmetric:
            for (i, j), value in self.Q.items():
                other = self.Q.get((j, i), 0.0)
                if abs(float(value) - float(other)) > tolerance:
                    raise ValueError(f'Q must be symmetric: Q[{i},{j}]={value}, Q[{j},{i}]={other}.')
        return self

    @property
    def nnz(self):
        return sum(1 for v in self.Q.values() if v != 0)

    def energy(self, x):
        if len(x) != self.n:
            raise ValueError('Solution length does not match QUBO dimension.')
        if any(int(v) not in (0, 1) for v in x):
            raise ValueError('QUBO solution must contain only binary values 0 or 1.')
        return float(self.offset) + sum(float(v) * int(x[i]) * int(x[j]) for (i, j), v in self.Q.items())

    @classmethod
    def from_dense(cls, matrix, offset=0.0, labels=None, require_symmetric=True):
        try:
            n = len(matrix)
            if any(len(row) != n for row in matrix):
                raise ValueError('QUBO matrix must be square.')
            q = {(i, j): _finite(matrix[i][j], f'Q[{i},{j}]')
                 for i in range(n) for j in range(n) if float(matrix[i][j]) != 0.0}
        except TypeError as exc:
            raise ValueError('QUBO matrix must be a two-dimensional square sequence.') from exc
        return cls(q, n, _finite(offset, 'QUBO offset'), labels, 'direct_qubo').validate(require_symmetric=require_symmetric)

    @classmethod
    def from_sparse(cls, n, coefficients: Mapping, offset=0.0, labels=None, require_symmetric=True):
        q = {}
        for key, value in coefficients.items():
            if not (isinstance(key, tuple) and len(key) == 2):
                raise ValueError(f'Invalid sparse QUBO key {key!r}; expected (i, j).')
            i, j = key
            if int(i) != i or int(j) != j:
                raise ValueError(f'Sparse QUBO indices must be integers: {key!r}.')
            v = _finite(value, f'Q[{i},{j}]')
            if v != 0.0:
                q[(int(i), int(j))] = v
        return cls(q, int(n), _finite(offset, 'QUBO offset'), labels, 'direct_qubo').validate(require_symmetric=require_symmetric)


@dataclass
class IsingModel:
    """Ising energy ``offset + sum(h[i]*s[i]) + sum(J[i,j]*s[i]*s[j])``; s in {-1,+1}."""
    h: dict[int, float]
    J: dict[tuple[int, int], float]
    n: int
    offset: float = 0.0

    def validate(self, max_variables=None):
        if not isinstance(self.n, int) or isinstance(self.n, bool) or self.n < 1:
            raise ValueError('Ising dimension n must be a positive integer.')
        if max_variables is not None and self.n > max_variables:
            raise ValueError(f'Model has {self.n} spins; backend limit is {max_variables}.')
        _finite(self.offset, 'Ising offset')
        for i, value in self.h.items():
            if not isinstance(i, int) or not 0 <= i < self.n:
                raise ValueError(f'Ising field index {i!r} outside 0..{self.n-1}.')
            _finite(value, f'h[{i}]')
        for pair, value in self.J.items():
            if not (isinstance(pair, tuple) and len(pair) == 2):
                raise ValueError(f'Invalid Ising coupler key {pair!r}; expected (i, j).')
            i, j = pair
            if not isinstance(i, int) or not isinstance(j, int) or not (0 <= i < self.n and 0 <= j < self.n):
                raise ValueError(f'Ising coupler {pair!r} outside 0..{self.n-1}.')
            if i == j:
                raise ValueError('Ising couplers must connect distinct variables.')
            _finite(value, f'J[{i},{j}]')
        return self

    def to_qubo(self) -> QuboModel:
        self.validate()
        # s=2x-1. Symmetric Q represents the same energy exactly, including offset.
        linear = {i: 2.0 * float(v) for i, v in self.h.items()}
        const = float(self.offset) - sum(float(v) for v in self.h.values())
        pair = {}
        for (i, j), val in self.J.items():
            a, b = sorted((i, j))
            pair[(a, b)] = pair.get((a, b), 0.0) + 4.0 * float(val)
            linear[a] = linear.get(a, 0.0) - 2.0 * float(val)
            linear[b] = linear.get(b, 0.0) - 2.0 * float(val)
            const += float(val)
        q = {(i, i): v for i, v in linear.items() if v}
        for (i, j), v in pair.items():
            q[(i, j)] = q.get((i, j), 0.0) + v / 2.0
            q[(j, i)] = q.get((j, i), 0.0) + v / 2.0
        return QuboModel(q, self.n, const, source='ising_conversion').validate(require_symmetric=True)

    @classmethod
    def from_qubo(cls, model: QuboModel):
        model.validate(require_symmetric=True)
        h, J = {}, {}
        offset = model.offset
        for i in range(model.n):
            d = float(model.Q.get((i, i), 0.0))
            offset += d / 2.0
            h[i] = h.get(i, 0.0) + d / 2.0
        for i in range(model.n):
            for j in range(i + 1, model.n):
                c = float(model.Q.get((i, j), 0.0)) + float(model.Q.get((j, i), 0.0))
                if c:
                    J[(i, j)] = c / 4.0
                    h[i] = h.get(i, 0.0) + c / 4.0
                    h[j] = h.get(j, 0.0) + c / 4.0
                    offset += c / 4.0
        return cls({i: v for i, v in h.items() if v}, J, model.n, offset).validate()


def compile_model(model, penalty=1000.0) -> QuboModel:
    """Compile binary linear/quadratic objective + equality constraints to symmetric QUBO.

    Equality constraints are penalised as penalty*(lhs-rhs)^2. The penalty is
    positive and finite. The constant offset is preserved separately.
    """
    penalty = _finite(penalty, 'Constraint penalty')
    if penalty <= 0:
        raise ValueError('Constraint penalty must be greater than zero.')
    n = len(model.variables)
    if n == 0:
        raise ValueError('Model has no variables.')
    if model.sense not in ('min', 'max'):
        raise ValueError(f'Unsupported objective sense {model.sense!r}.')
    lin = dict(model.linear)
    quad = dict(model.quadratic)
    offset = _finite(model.constant, 'Objective constant')
    factor = 1.0 if model.sense == 'min' else -1.0
    lin = {i: factor * _finite(v, f'linear[{i}]') for i, v in lin.items()}
    quad = {k: factor * _finite(v, f'quadratic[{k}]') for k, v in quad.items()}
    offset *= factor

    for con in model.constraints:
        if con.sense != '==':
            raise NotImplementedError('Only equality constraints are supported in this SDK release.')
        terms = con.terms
        r = _finite(con.rhs, f'constraint {con.name} RHS')
        if any(not isinstance(i, int) or not 0 <= i < n for i in terms):
            raise ValueError(f'Constraint {con.name!r} references an unknown variable.')
        offset += penalty * r * r
        for i, a in terms.items():
            a = _finite(a, f'constraint {con.name} coefficient[{i}]')
            lin[i] = lin.get(i, 0.0) + penalty * (a * a - 2.0 * r * a)
        ids = sorted(terms)
        for p, i in enumerate(ids):
            for j in ids[p + 1:]:
                quad[(i, j)] = quad.get((i, j), 0.0) + 2.0 * penalty * terms[i] * terms[j]

    Q = {}
    for i, c in lin.items():
        if c:
            Q[(i, i)] = c
    for (i, j), c in quad.items():
        if not (0 <= i < n and 0 <= j < n):
            raise ValueError(f'Objective quadratic index {(i, j)} outside model variables.')
        if c:
            Q[(i, j)] = Q.get((i, j), 0.0) + c / 2.0
            Q[(j, i)] = Q.get((j, i), 0.0) + c / 2.0
    labels = [v.name for v in model.variables]
    return QuboModel(Q, n, offset, labels, 'model_builder').validate(require_symmetric=True)
