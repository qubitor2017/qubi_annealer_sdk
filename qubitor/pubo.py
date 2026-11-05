"""PUBO representation and exact Rosenberg quadratization to QUBO."""
from dataclasses import dataclass, field
from itertools import combinations
from math import isfinite
from .qubo import QuboModel

@dataclass
class PuboModel:
    """Minimize offset + sum(c_S * product(x_i for i in S)); binary variables."""
    n: int
    terms: dict[tuple[int, ...], float] = field(default_factory=dict)
    offset: float = 0.0
    labels: list[str] | None = None
    def __post_init__(self):
        cleaned={}
        for key,val in self.terms.items():
            ids=tuple(sorted(set(int(i) for i in key)))
            if any(i<0 or i>=self.n for i in ids): raise ValueError(f'PUBO index outside 0..{self.n-1}: {ids}')
            v=float(val)
            if not isfinite(v): raise ValueError('PUBO coefficients must be finite')
            if v: cleaned[ids]=cleaned.get(ids,0.0)+v
        self.terms={k:v for k,v in cleaned.items() if v}
        if self.n<1: raise ValueError('PUBO must contain at least one variable')
    def energy(self,x):
        if len(x)!=self.n: raise ValueError('Solution length mismatch')
        return self.offset+sum(c*all(int(x[i]) for i in ids) for ids,c in self.terms.items())
    def quadratize(self, penalty=None):
        """Return (QUBO, decoder metadata). Penalty must dominate objective variation."""
        bound=sum(abs(c) for c in self.terms.values())
        M=float(penalty if penalty is not None else max(1.0,bound+1.0))
        if M<=bound: raise ValueError(f'Quadratization penalty must exceed sum(abs(coefficients))={bound:g}; got {M:g}')
        linear={}; quadratic={}; next_id=self.n; ancillas=[]
        def add_lin(i,c): linear[i]=linear.get(i,0.0)+c
        def add_pair(i,j,c):
            if i==j: add_lin(i,c)
            else:
                a,b=sorted((i,j)); quadratic[(a,b)]=quadratic.get((a,b),0.0)+c
        def product_ancilla(a,b):
            nonlocal next_id
            y=next_id; next_id+=1; ancillas.append((y,a,b))
            # M*(a*b - 2*a*y - 2*b*y + 3*y), zero iff y=a*b.
            add_pair(a,b,M); add_pair(a,y,-2*M); add_pair(b,y,-2*M); add_lin(y,3*M)
            return y
        for ids,c in self.terms.items():
            if len(ids)==0: continue
            if len(ids)==1: add_lin(ids[0],c); continue
            factors=list(ids)
            while len(factors)>2:
                y=product_ancilla(factors[0],factors[1])
                factors=[y]+factors[2:]
            add_pair(factors[0],factors[1],c)
        Q={}
        for i,c in linear.items():
            if c: Q[(i,i)]=c
        for (i,j),c in quadratic.items():
            if c: Q[(i,j)]=Q.get((i,j),0.0)+c/2; Q[(j,i)]=Q.get((j,i),0.0)+c/2
        labels=(self.labels or [f'x{i}' for i in range(self.n)])+[f'__ancilla_{k}' for k in range(len(ancillas))]
        model=QuboModel(Q,next_id,self.offset,labels,'pubo_quadratization').validate(require_symmetric=True)
        return model, {'original_n':self.n,'ancillas':ancillas,'penalty':M,'objective_abs_bound':bound}
    def decode(self,qubo_solution,metadata):
        return list(qubo_solution[:metadata['original_n']])
