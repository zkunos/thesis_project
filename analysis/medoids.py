"""CLARA-style sampling with exact PAM swap optimization inside each sample."""
import numpy as np
from scipy.spatial.distance import cdist


class SampledPAM:
    def __init__(self,k=3,sample_size=400,n_samples=3,max_iter=15,seed=42):
        self.k,self.sample_size,self.n_samples,self.max_iter,self.seed=k,sample_size,n_samples,max_iter,seed

    def fit(self,X):
        X=np.asarray(X,float); rng=np.random.default_rng(self.seed); best=np.inf
        for repeat in range(self.n_samples):
            ids=rng.choice(len(X),min(len(X),self.sample_size),replace=False)
            S=X[ids]; D=cdist(S,S)
            med=[int(np.argmin(D.sum(axis=0)))]
            while len(med)<self.k:
                cost=np.minimum(D[:,med].min(axis=1)[:,None],D).sum(axis=0)
                cost[med]=np.inf; med.append(int(np.argmin(cost)))
            for iteration in range(self.max_iter):
                current=D[:,med].min(axis=1).sum()
                swap=None; best_swap=current
                for j in range(self.k):
                    other=[m for i,m in enumerate(med) if i!=j]
                    remain=D[:,other].min(axis=1) if other else np.full(len(S),np.inf)
                    costs=np.minimum(remain[:,None],D).sum(axis=0)
                    costs[med]=np.inf; candidate=int(np.argmin(costs))
                    if costs[candidate]<best_swap-1e-9:
                        best_swap=costs[candidate];swap=(j,candidate)
                if swap is None: break
                med[swap[0]]=swap[1]
            candidate=S[med]
            cost=cdist(X,candidate).min(axis=1).sum()
            if cost<best:
                best=cost;self.cluster_centers_=candidate.copy();self.medoid_indices_=ids[med]
        self.inertia_=best;self.labels_=self.predict(X)
        return self

    def predict(self,X):
        return cdist(X,self.cluster_centers_).argmin(axis=1)
