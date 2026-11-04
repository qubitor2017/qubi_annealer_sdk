"""Compatibility layer for the historical qubif_sdk Max-Cut demo.

Legacy convention: build_maxcut returns Ising couplers J and fields h.
"""
from .. import from_ising, solve as solve_model

def build_maxcut(edges,n_nodes=None,weights=None):
    edges=list(edges)
    if n_nodes is None: n_nodes=1+max((max(u,v) for u,v in edges),default=-1)
    weights=list(weights) if weights is not None else [1.0]*len(edges)
    if len(weights)!=len(edges): raise ValueError('weights length mismatch')
    J={}
    for (u,v),w in zip(edges,weights):
        if u==v or not (0<=u<n_nodes and 0<=v<n_nodes): raise ValueError(f'Invalid edge {(u,v)}')
        a,b=sorted((int(u),int(v))); J[(a,b)]=J.get((a,b),0.0)+float(w)
    h={i:0.0 for i in range(n_nodes)}
    return J,h

def decode_maxcut(spins,edges,weights=None):
    weights=list(weights) if weights is not None else [1.0]*len(edges)
    return sum(w for (u,v),w in zip(edges,weights) if int(spins[u])!=int(spins[v]))

class AnnealerClient:
    def __init__(self,port='/dev/ttyUSB0',backend='n512',**kwargs):
        self.port,self.backend,self.kwargs=port,backend,kwargs
    def solve(self,J,h,n,problem_type=0,num_sweeps=4000):
        if problem_type!=0: raise NotImplementedError('Only the legacy Ising/Max-Cut problem type is supported')
        ising=from_ising(h=h,J=J,n=int(n))
        result=solve_model(ising,backend=self.backend,port=self.port,**self.kwargs)
        spins=[1 if int(bit) else -1 for bit in result.solution]
        return spins,result.objective
    def close(self): pass
