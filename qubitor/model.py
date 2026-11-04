"""Small binary model builder for Qubitor's initial QUBO SDK.

MVP scope: binary variables, linear/quadratic objective terms, and equality
constraints. Inequalities, general integer/continuous variables, and arbitrary
MILP/MIQP ingestion are intentionally not silently approximated in this release.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Iterable, Mapping, Sequence, Union

Number = Union[int, float]

@dataclass(frozen=True)
class Var:
    index: int
    name: str

    def __hash__(self):
        return hash(self.index)

    def _expr(self): return Expr({self.index: 1.0})
    def __add__(self, other): return self._expr() + other
    def __radd__(self, other): return self._expr() + other
    def __sub__(self, other): return self._expr() - other
    def __rsub__(self, other): return as_expr(other) - self._expr()
    def __mul__(self, scalar): return self._expr() * scalar
    def __rmul__(self, scalar): return self._expr() * scalar
    def __neg__(self): return -self._expr()
    def __le__(self, rhs): return self._expr() <= rhs
    def __ge__(self, rhs): return self._expr() >= rhs
    def __eq__(self, rhs): return self._expr() == rhs

@dataclass
class Constraint:
    terms: Dict[int, float]
    sense: str
    rhs: float
    name: str

class Expr:
    """Affine expression. Products of variables are added with Model.add_quadratic."""
    def __init__(self, terms=None, constant=0.0):
        self.terms: Dict[int, float] = dict(terms or {})
        self.constant = float(constant)

    def _coerce(self, other):
        if isinstance(other, Expr): return other
        if isinstance(other, Var): return Expr({other.index: 1.0})
        if isinstance(other, (int, float)): return Expr(constant=float(other))
        return NotImplemented

    def __add__(self, other):
        other = self._coerce(other)
        if other is NotImplemented: return NotImplemented
        t = dict(self.terms)
        for i, c in other.terms.items(): t[i] = t.get(i, 0.0) + c
        return Expr({i:c for i,c in t.items() if abs(c)>1e-15}, self.constant + other.constant)
    __radd__ = __add__

    def __sub__(self, other): return self + (-1 * self._coerce(other))
    def __rsub__(self, other): return self._coerce(other) - self
    def __mul__(self, scalar):
        if not isinstance(scalar, (int, float)): raise TypeError('Expressions can only be scaled by a number; use add_quadratic for variable products.')
        return Expr({i: c*scalar for i,c in self.terms.items()}, self.constant*scalar)
    __rmul__ = __mul__
    def __neg__(self): return self * -1
    def __le__(self, rhs): return (self, '<=', float(rhs))
    def __ge__(self, rhs): return (self, '>=', float(rhs))
    def __eq__(self, rhs):
        # Constraint-building convenience; equality between two Expr objects is not model identity.
        if isinstance(rhs, (int, float, Expr, Var)):
            return (self, '==', rhs)
        return False

class Model:
    def __init__(self, name='qubitor_model'):
        self.name = name
        self.variables: list[Var] = []
        self.linear: Dict[int, float] = {}
        self.quadratic: Dict[tuple[int,int], float] = {}
        self.constraints: list[Constraint] = []
        self.constant = 0.0
        self.sense = 'min'

    def binary_var(self, name=None) -> Var:
        idx = len(self.variables)
        var = Var(idx, name or f'x{idx}')
        self.variables.append(var)
        return var

    def binary_vars(self, name, shape):
        if isinstance(shape, int): shape = (shape,)
        if len(shape) == 1:
            return [self.binary_var(f'{name}[{i}]') for i in range(shape[0])]
        if len(shape) == 2:
            return [[self.binary_var(f'{name}[{i},{j}]') for j in range(shape[1])] for i in range(shape[0])]
        raise ValueError('MVP binary_vars supports 1-D or 2-D shapes.')

    def minimize(self, expr):
        self._set_objective(expr, 'min')

    def maximize(self, expr):
        self._set_objective(expr, 'max')

    def _set_objective(self, expr, sense):
        if not isinstance(expr, Expr): expr = as_expr(expr)
        self.linear = dict(expr.terms)
        self.constant = expr.constant
        self.sense = sense

    def add_linear(self, var: Var, coefficient: Number):
        self.linear[var.index] = self.linear.get(var.index, 0.0) + float(coefficient)

    def add_quadratic(self, var_a: Var, var_b: Var, coefficient: Number):
        i, j = sorted((var_a.index, var_b.index))
        if i == j:
            # For binary variables x_i^2 == x_i.
            self.add_linear(var_a, coefficient)
        else:
            self.quadratic[(i,j)] = self.quadratic.get((i,j), 0.0) + float(coefficient)

    def add_constraint(self, relation, name=None):
        if not (isinstance(relation, tuple) and len(relation) == 3):
            raise TypeError('Use model.add_constraint(expr == rhs, name=...) for equality constraints.')
        expr, sense, rhs = relation
        if not isinstance(expr, Expr): expr = as_expr(expr)
        if sense != '==':
            raise NotImplementedError('Initial SDK supports equality constraints only. Inequalities require explicit slack-variable modelling in a future release.')
        # Move expression constant to the right-hand side.
        self.constraints.append(Constraint(dict(expr.terms), sense, float(rhs) - expr.constant, name or f'c{len(self.constraints)}'))
        return self.constraints[-1]

    def one_hot(self, variables: Sequence[Var], name=None):
        return self.add_constraint(sum_expr(variables) == 1, name=name or 'one_hot')


def as_expr(value):
    if isinstance(value, Expr): return value
    if isinstance(value, Var): return Expr({value.index: 1.0})
    if isinstance(value, (int, float)): return Expr(constant=float(value))
    raise TypeError(f'Cannot convert {type(value).__name__} to an expression.')

def sum_expr(items: Iterable):
    result = Expr()
    for item in items: result = result + as_expr(item)
    return result
