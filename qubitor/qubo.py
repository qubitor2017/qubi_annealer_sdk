"""QUBO/Ising representations and model compiler."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping
import math

@dataclass
class QuboModel:
    """Symmetric matrix Q, interpreted by the hardware as x.T @ Q @ x.

    Coefficients are stored as Python numbers at SDK level. The serial backend
    quantizes to signed int32 using a caller-selected scale.
    """
    Q: dict[tuple[int,int], float]
    n: int
    offset: float = 0.0
    labels: list[str] | None = None
    source: str = 'direct_qubo'

    def validate(self, max_variables=None, require_symmetric=True, tolerance=1e-8):
        if self.n < 1: raise ValueError('QUBO must contain at least one variable.')
        if max_variables is not None and self.n > max_variables:
            raise ValueError(f'Model has {self.n} variables; backend limit is {max_variables}.')
        for (i,j), value in self.Q.items():
            if not (0 <= i < self.n and 0 <= j < self.n): raise ValueError(f'Q index {(i,j)} outside 0..{self.n-1}.')
            if not math.isfinite(float(value)): raise ValueError(f'Non-finite coefficient at {(i,j)}.')
        if require_symmetric:
            for (i,j), value in self.Q.items():
                other = self.Q.get((j,i), 0.0)
                if abs(float(value)-float(other)) > tolerance:
                    raise ValueError(f'Q must be symmetric for this backend: Q[{i},{j}]={value}, Q[{j},{i}]={other}.')
        return self

    @property
    def nnz(self): return sum(1 for v in self.Q.values() if v != 0)

    def energy(self, x):
        if len(x) != self.n: raise ValueError('Solution length does not match QUBO dimension.')
        return self.offset + sum(float(v)*int(x[i])*int(x[j]) for (i,j),v in self.Q.items())

    @classmethod
    def from_dense(cls, matrix, offset=0.0, labels=None, require_symmetric=True):
        n = len(matrix)
        if any(len(row) != n for row in matrix): raise ValueError('Q must be square.')
        q = {(i,j): float(matrix[i][j]) for i in range(n) for j in range(n) if float(matrix[i][j]) != 0}
        return cls(q, n, float(offset), labels, 'direct_qubo').validate(require_symmetric=require_symmetric)

    @classmethod
    def from_sparse(cls, n, coefficients: Mapping, offset=0.0, labels=None, require_symmetric=True):
        q = {(int(i),int(j)):float(v) for (i,j),v in coefficients.items() if float(v) != 0}
        return cls(q, int(n), float(offset), labels, 'direct_qubo').validate(require_symmetric=require_symmetric)

@dataclass
class IsingModel:
    h: dict[int, float]
    J: dict[tuple[int,int], float]
    n: int
    offset: float = 0.0

    def to_qubo(self) -> QuboModel:
        # E(s)=offset + sum h_i s_i + sum J_ij s_i s_j, s=2x-1.
        # Returns symmetric Q for x.T Q x, preserving the energy up to constants.
        linear = {i: 2.0*float(v) for i,v in self.h.items()}
        const = float(self.offset) - sum(float(v) for v in self.h.values())
        pair = {}
        for (i,j), val in self.J.items():
            if i == j: raise ValueError('Ising couplers must connect distinct variables.')
            a,b = sorted((int(i),int(j)))
            pair[(a,b)] = pair.get((a,b),0.0) + 4.0*float(val)
            linear[a] = linear.get(a,0.0) - 2.0*float(val)
            linear[b] = linear.get(b,0.0) - 2.0*float(val)
            const += float(val)
        q = {(i,i):v for i,v in linear.items() if v}
        for (i,j), v in pair.items():
            # Split the polynomial coefficient evenly across symmetric matrix entries.
            q[(i,j)] = q.get((i,j),0.0) + v/2.0
            q[(j,i)] = q.get((j,i),0.0) + v/2.0
        return QuboModel(q, self.n, const, source='ising_conversion').validate(require_symmetric=True)

    @classmethod
    def from_qubo(cls, model: QuboModel):
        model.validate(require_symmetric=True)
        # E(x)=x.T Q x; convert with x=(s+1)/2.
        h = {}
        J = {}
        offset = model.offset
        for i in range(model.n):
            offset += float(model.Q.get((i,i),0.0))/2.0
            h[i] = h.get(i,0.0) + float(model.Q.get((i,i),0.0))/2.0
        for i in range(model.n):
            for j in range(i+1,model.n):
                # Symmetric Q contributes Qij+Qji to x_i*x_j.
                c = float(model.Q.get((i,j),0.0)) + float(model.Q.get((j,i),0.0))
                if c:
                    J[(i,j)] = c/4.0
                    h[i] = h.get(i,0.0) + c/4.0
                    h[j] = h.get(j,0.0) + c/4.0
                    offset += c/4.0
        return cls({i:v for i,v in h.items() if v}, J, model.n, offset)


def compile_model(model, penalty=1000.0) -> QuboModel:
    """Compile the supported model builder subset to symmetric QUBO.

    Each equality constraint receives penalty * (lhs-rhs)^2. The generated
    symmetric matrix represents twice the resulting polynomial (same argmin),
    avoiding half-integer coefficients for quadratic terms. The constant offset
    is retained separately for reporting.
    """
    n = len(model.variables)
    if n == 0: raise ValueError('Model has no variables.')
    lin = dict(model.linear)
    quad = dict(model.quadratic)
    offset = float(model.constant)
    sense_factor = 1.0 if model.sense == 'min' else -1.0
    lin = {i: sense_factor*v for i,v in lin.items()}
    quad = {k: sense_factor*v for k,v in quad.items()}
    offset *= sense_factor

    for con in model.constraints:
        # penalty*(sum a_i*x_i - rhs)^2; x_i^2 = x_i for binary variables.
        terms = con.terms
        r = float(con.rhs)
        offset += penalty*r*r
        for i,a in terms.items():
            lin[i] = lin.get(i,0.0) + penalty*(a*a - 2.0*r*a)
        ids = sorted(terms)
        for p,i in enumerate(ids):
            for j in ids[p+1:]:
                key=(i,j)
                quad[key] = quad.get(key,0.0) + 2.0*penalty*terms[i]*terms[j]

    # Q is symmetric and hardware energy is x^T Q x. Diagonal entries carry
    # linear terms; each quadratic polynomial coefficient is split evenly over
    # Q[i,j] and Q[j,i], so the represented energy equals the compiled polynomial.
    Q = {}
    for i,c in lin.items():
        if c: Q[(i,i)] = c
    for (i,j),c in quad.items():
        if c:
            Q[(i,j)] = Q.get((i,j),0.0) + c/2.0
            Q[(j,i)] = Q.get((j,i),0.0) + c/2.0
    labels = [v.name for v in model.variables]
    return QuboModel(Q, n, offset, labels, 'model_builder').validate(require_symmetric=True)
