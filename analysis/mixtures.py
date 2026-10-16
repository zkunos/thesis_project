"""Observed-data EM for Gaussian and fixed-tail robust elliptical mixtures.

Missing coordinates are integrated out, not mean-filled for likelihood fitting.
Mean filling is used only for initialization. The t degrees of freedom and the
contamination fraction/inflation are fixed hyperparameters, not estimated.
This is an independently tested Python implementation, not MixtureMissing.
"""
from __future__ import annotations
import numpy as np
from scipy.special import gammaln, logsumexp
from scipy.linalg import solve_triangular
from sklearn.cluster import KMeans


def positive_definite(S, floor):
    values, vectors = np.linalg.eigh((S + S.T) / 2)
    return (vectors * np.maximum(values, floor)) @ vectors.T


class MissingMixture:
    def __init__(self, k=2, family='normal', df=5., alpha=.9, inflation=10.,
                 reg=.01, n_init=2, max_iter=120, tol=1e-5, seed=42):
        self.k, self.family, self.df = k, family, df
        self.alpha, self.inflation, self.reg = alpha, inflation, reg
        self.n_init, self.max_iter, self.tol, self.seed = n_init, max_iter, tol, seed

    def _patterns(self, X):
        masks, codes = np.unique(~np.isnan(X), axis=0, return_inverse=True)
        return [(np.flatnonzero(codes == j), np.flatnonzero(m), np.flatnonzero(~m))
                for j, m in enumerate(masks)]

    def _component(self, X, mean, cov, patterns, moments=False):
        n, p = X.shape
        logp = np.empty(n)
        tau = np.empty(n)
        conditional = np.empty_like(X) if moments else None
        conditional_covs = []
        for ids, obs, mis in patterns:
            q = len(obs)
            if q:
                Soo = cov[np.ix_(obs, obs)]
                L = np.linalg.cholesky(Soo)
                deltaX = X[np.ix_(ids, obs)] - mean[obs]
                whitened = solve_triangular(L, deltaX.T, lower=True, check_finite=False)
                delta = np.sum(whitened**2, axis=0)
                logdet = 2 * np.log(np.diag(L)).sum()
            else:
                delta = np.zeros(len(ids)); logdet = 0.
            normal = -.5 * (q * np.log(2*np.pi) + logdet + delta)
            if self.family == 'normal':
                logp[ids], tau[ids] = normal, 1.
            elif self.family == 't':
                nu = self.df
                logp[ids] = (gammaln((nu+q)/2)-gammaln(nu/2)
                    -.5*(q*np.log(nu*np.pi)+logdet) -(nu+q)/2*np.log1p(delta/nu))
                tau[ids] = (nu+q)/(nu+delta)
            elif self.family == 'contaminated':
                bad = -.5*(q*np.log(2*np.pi*self.inflation)+logdet+delta/self.inflation)
                density = np.logaddexp(np.log(self.alpha)+normal, np.log1p(-self.alpha)+bad)
                good_prob = np.exp(np.log(self.alpha)+normal-density)
                logp[ids] = density
                tau[ids] = good_prob + (1-good_prob)/self.inflation
            else:
                raise ValueError(self.family)
            if moments:
                conditional[ids] = X[ids]
                if len(mis):
                    if q:
                        gain = np.linalg.solve(Soo, cov[np.ix_(obs, mis)])
                        conditional[np.ix_(ids, mis)] = mean[mis] + deltaX @ gain
                        C = cov[np.ix_(mis, mis)] - cov[np.ix_(mis, obs)] @ gain
                    else:
                        conditional[ids] = mean
                        C = cov.copy()
                    conditional_covs.append((ids, mis, C))
        return logp, tau, conditional, conditional_covs

    def _log_prob(self, X):
        patterns = self._patterns(X)
        return np.column_stack([self._component(X, m, S, patterns)[0]
                                for m,S in zip(self.means_, self.covariances_)])

    def fit(self, X):
        X = np.asarray(X, float)
        n, p = X.shape
        patterns = self._patterns(X)
        filled = np.where(np.isnan(X), np.nanmean(X,axis=0), X)
        best = None
        for start in range(self.n_init):
            labels = KMeans(n_clusters=self.k, n_init=3, random_state=self.seed+start).fit_predict(filled)
            means = np.array([filled[labels==g].mean(axis=0) for g in range(self.k)])
            base = positive_definite(np.cov(filled,rowvar=False),self.reg)
            covs = np.array([positive_definite(np.cov(filled[labels==g],rowvar=False),self.reg)
                             if np.sum(labels==g)>p+2 else base.copy() for g in range(self.k)])
            weights = np.bincount(labels,minlength=self.k)/n
            history=[]
            converged=False
            for iteration in range(self.max_iter):
                values=[self._component(X,m,S,patterns,True) for m,S in zip(means,covs)]
                logjoint=np.column_stack([v[0] for v in values])+np.log(np.maximum(weights,1e-15))
                logden=logsumexp(logjoint,axis=1)
                ll=float(logden.sum()); history.append(ll)
                if iteration and abs(ll-history[-2])/n < self.tol:
                    converged=True; break
                resp=np.exp(logjoint-logden[:,None])
                Nk=resp.sum(axis=0)
                for g,(_,tau,C,conditional_covs) in enumerate(values):
                    w=resp[:,g]*tau
                    total=w.sum()
                    S1=w @ C
                    S2=(C.T*w) @ C
                    for ids,mis,S in conditional_covs:
                        S2[np.ix_(mis,mis)] += resp[ids,g].sum()*S
                    means[g]=S1/max(total,1e-12)
                    covs[g]=positive_definite((S2-np.outer(means[g],S1)-np.outer(S1,means[g])
                        +total*np.outer(means[g],means[g]))/max(Nk[g],1e-12),self.reg)
                weights=np.maximum(Nk,1e-10); weights/=weights.sum()
            self.means_,self.covariances_,self.weights_=means,covs,weights
            ll=float(self.score_samples(X).sum())
            if best is None or ll>best[0]:
                best=(ll,means.copy(),covs.copy(),weights.copy(),converged,history)
        self.loglik_,self.means_,self.covariances_,self.weights_,self.converged_,self.history_=best
        self.n_iter_=len(self.history_)
        self.n_parameters_=self.k*(p+p*(p+1)//2)+self.k-1
        return self

    def score_samples(self,X):
        return logsumexp(self._log_prob(np.asarray(X,float))+np.log(self.weights_),axis=1)

    def predict_proba(self,X):
        logjoint=self._log_prob(np.asarray(X,float))+np.log(self.weights_)
        return np.exp(logjoint-logsumexp(logjoint,axis=1)[:,None])

    def predict(self,X):
        return self.predict_proba(X).argmax(axis=1)

    def bic(self,X):
        return -2*self.score_samples(X).sum()+self.n_parameters_*np.log(len(X))

    def icl(self,X):
        P=self.predict_proba(X)
        return self.bic(X)-2*np.sum(P*np.log(np.maximum(P,1e-15)))
