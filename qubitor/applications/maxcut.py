"""Max-Cut model conversion: minimize -cut as a symmetric QUBO."""
from ..qubo import QuboModel

def build_maxcut(edges,n_nodes=None,weights=None):
    edges=list(edges)
    if n_nodes is None: n_nodes=1+max((max(u,v) for u,v in edges),default=-1)
    if n_nodes<1: raise ValueError('n_nodes must be positive')
    Q={}; weights=list(weights) if weights is not None else [1.0]*len(edges)
    if len(weights)!=len(edges): raise ValueError('weights length mismatch')
    for (u,v),w in zip(edges,weights):
        if u==v or not (0<=u<n_nodes and 0<=v<n_nodes): raise ValueError(f'Invalid edge {(u,v)}')
        w=float(w)
        # E=-cut: -w*x_u -w*x_v +2w*x_u*x_v.
        Q[(u,u)]=Q.get((u,u),0.0)-w; Q[(v,v)]=Q.get((v,v),0.0)-w
        Q[(u,v)]=Q.get((u,v),0.0)+w; Q[(v,u)]=Q.get((v,u),0.0)+w
    return QuboModel(Q,n_nodes,source='maxcut').validate(require_symmetric=True)

def decode_maxcut(solution,edges,weights=None):
    weights=list(weights) if weights is not None else [1.0]*len(edges)
    return sum(w for (u,v),w in zip(edges,weights) if int(solution[u])!=int(solution[v]))
