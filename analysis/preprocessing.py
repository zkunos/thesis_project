"""Training-only cognitive preprocessing shared by legacy and new analyses."""
from __future__ import annotations

import numpy as np
import pandas as pd

HIGHER_WORSE = frozenset({'ATMTA'})
DOMAINS = {
    'Orientation': ['OPERSONA', 'OESPAI', 'OTEMPS'],
    'Attention': ['ASPAN', 'ATMTA'],
    'Visuoperception': ['VPIMATGES'],
    'Language': ['LREPETICIOTB', 'LDENOMINACIOTB', 'LCOMPRENSIOTB'],
    'Memory': ['MDIGITS', 'MRAVLT075', 'MRAVLT015', 'MRAVLT015R'],
    'Executive Function': ['FEPMR'],
}
FEATURES = [v for values in DOMAINS.values() for v in values]


class CognitivePreprocessor:
    """Fit observed training quantiles/scales; never learn from validation rows.

    Missing entries remain missing in transform_tests. aggregate requires a
    completed matrix so each domain has an invariant definition.
    """
    def __init__(self, domains=None, weights=None, clip=(0.01, 0.99)):
        self.domains = domains or DOMAINS
        self.weights = weights
        self.clip = clip

    def fit(self, frame):
        self.columns_ = list(frame.columns)
        if set(self.columns_) != {v for vs in self.domains.values() for v in vs}:
            raise ValueError('Domain map must cover exactly the supplied cognitive features')
        X = frame.to_numpy(dtype=float)
        if np.any(np.all(np.isnan(X), axis=0)):
            raise ValueError('A training variable has no observations')
        self.lo_, self.hi_ = np.nanquantile(X, self.clip, axis=0)
        self.direction_ = np.array([-1.0 if c in HIGHER_WORSE else 1.0 for c in self.columns_])
        Y = np.clip(X, self.lo_, self.hi_) * self.direction_
        self.mean_ = np.nanmean(Y, axis=0)
        self.scale_ = np.nanstd(Y, axis=0)
        self.scale_[self.scale_ < 1e-10] = 1.0
        w = (1 - np.isnan(X).mean(axis=0)) if self.weights is None else np.array(
            [self.weights.get(c, 1.0) for c in self.columns_])
        self.matrix_ = np.zeros((len(self.columns_), len(self.domains)))
        for j, cols in enumerate(self.domains.values()):
            idx = [self.columns_.index(c) for c in cols]
            self.matrix_[idx, j] = w[idx] / w[idx].sum()
        limits = np.array([self.lo_, self.hi_]) * self.direction_
        self.min_ = (limits.min(axis=0) - self.mean_) / self.scale_
        self.max_ = (limits.max(axis=0) - self.mean_) / self.scale_
        return self

    def transform_tests(self, frame):
        X = frame.loc[:, self.columns_].to_numpy(dtype=float)
        return (np.clip(X, self.lo_, self.hi_) * self.direction_ - self.mean_) / self.scale_

    def aggregate(self, completed):
        X = np.asarray(completed, dtype=float)
        if X.shape[1] != len(self.columns_) or not np.isfinite(X).all():
            raise ValueError('Aggregate requires a finite, aligned completed test matrix')
        return X @ self.matrix_


def compute_domain_scores(X_df, domains, weights=None):
    """Compatibility wrapper reproducing NB5's complete-data preprocessing.

    This fits on all supplied rows for legacy descriptive analyses. New held-out
    analyses must instead fit CognitivePreprocessor on discovery rows only.
    """
    fitted = CognitivePreprocessor(domains=domains, weights=weights).fit(X_df)
    return pd.DataFrame(fitted.aggregate(fitted.transform_tests(X_df)),
                        index=X_df.index, columns=list(domains))
