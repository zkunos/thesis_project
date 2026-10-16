import unittest
import numpy as np
import pandas as pd
from scipy.stats import multivariate_normal, multivariate_t
from sklearn.mixture import GaussianMixture
from sklearn.metrics import adjusted_rand_score
from threadpoolctl import threadpool_limits
from .mixtures import MissingMixture
from .medoids import SampledPAM
from .preprocessing import CognitivePreprocessor, compute_domain_scores


class ResearchTests(unittest.TestCase):
    def test_marginal_likelihoods(self):
        X=np.array([[1.,np.nan],[np.nan,-.5],[1.,-.5],[np.nan,np.nan]])
        mean=np.array([.2,.3]);cov=np.array([[1.2,.4],[.4,.8]])
        for family in ['normal','t','contaminated']:
            model=MissingMixture(k=1,family=family,df=5)
            model.means_=mean[None];model.covariances_=cov[None];model.weights_=np.ones(1)
            expected=[]
            for row in X:
                observed=~np.isnan(row)
                if not observed.any(): expected.append(0.);continue
                m=mean[observed];S=cov[np.ix_(observed,observed)];v=row[observed]
                if family=='normal': val=multivariate_normal.logpdf(v,mean=m,cov=S)
                elif family=='t': val=multivariate_t.logpdf(v,loc=m,shape=S,df=5)
                else: val=np.logaddexp(np.log(.9)+multivariate_normal.logpdf(v,mean=m,cov=S),
                    np.log(.1)+multivariate_normal.logpdf(v,mean=m,cov=S*10))
                expected.append(val)
            np.testing.assert_allclose(model.score_samples(X),expected,rtol=1e-10,atol=1e-10)

    def test_complete_gaussian_reference(self):
        rng=np.random.default_rng(7)
        X=np.r_[rng.normal(-3,.7,(250,3)),rng.normal(3,.8,(250,3))]
        ours=MissingMixture(2,reg=1e-6,n_init=1,tol=1e-7).fit(X)
        reference=GaussianMixture(2,reg_covar=1e-6,n_init=3,random_state=42).fit(X)
        self.assertAlmostEqual(ours.score_samples(X).mean(),reference.score(X),places=5)
        self.assertGreater(adjusted_rand_score(ours.predict(X),reference.predict(X)),.99)

    def test_missing_recovery_and_monotonicity(self):
        rng=np.random.default_rng(9)
        X=np.r_[rng.normal(-3,.5,(200,3)),rng.normal(3,.5,(200,3))]
        truth=np.repeat([0,1],200)
        missing=rng.random(X.shape)<.25;missing[:,0]=False
        X[missing]=np.nan
        for family in ['normal','t','contaminated']:
            fit=MissingMixture(2,family=family,reg=1e-6,n_init=1,max_iter=150).fit(X)
            self.assertGreater(adjusted_rand_score(truth,fit.predict(X)),.95)
            self.assertTrue(np.all(np.diff(fit.history_)>=-1e-6))
            np.testing.assert_allclose(fit.predict_proba(X).sum(axis=1),1)

    def test_preprocessing_direction_and_no_leakage(self):
        frame=pd.DataFrame({'ATMTA':[10.,20.,30.,40.],'ASPAN':[1.,2.,3.,4.]})
        pp=CognitivePreprocessor({'Attention':['ATMTA','ASPAN']}).fit(frame)
        before=pp.mean_.copy()
        transformed=pp.transform_tests(pd.DataFrame({'ATMTA':[10000.],'ASPAN':[4.]}))
        self.assertLess(transformed[0,0],0)
        np.testing.assert_array_equal(pp.mean_,before)
        legacy=compute_domain_scores(frame,{'Attention':['ATMTA','ASPAN']})
        np.testing.assert_allclose(legacy.to_numpy(),0,atol=1e-10)

    def test_pam_recovers_separated_groups(self):
        rng=np.random.default_rng(3)
        X=np.r_[rng.normal(-4,.3,(40,2)),rng.normal(4,.3,(40,2))]
        model=SampledPAM(2,sample_size=80,n_samples=1).fit(X)
        self.assertEqual(adjusted_rand_score(np.repeat([0,1],40),model.labels_),1.)
        np.testing.assert_array_equal(model.cluster_centers_,X[model.medoid_indices_])

    def test_trajectory_integrated_likelihood(self):
        from .trajectory import TrajectoryMixture,sufficient
        t=np.array([0.,.4,1.2]);y=np.array([.2,.5,.1]);beta=np.array([[.1,.3]])
        D=np.array([[.3,.02],[.02,.1]]);noise=.2;Z=np.column_stack([np.ones(3),t])
        lp,_,_=TrajectoryMixture().terms(sufficient([(t,y)]),beta,D,noise)
        expected=multivariate_normal.logpdf(y,mean=Z@beta[0],cov=Z@D@Z.T+noise*np.eye(3))
        self.assertAlmostEqual(lp[0,0],expected,places=10)

    def test_trajectory_em_monotonic(self):
        from .trajectory import TrajectoryMixture
        rng=np.random.default_rng(99);records=[]
        for j in range(160):
            t=np.array([0.,.3,.7,1.2]);group=j//80
            beta=np.array([-2+4*group,-1+2*group])+rng.normal(0,.15,2)
            records.append((t,beta[0]+beta[1]*t+rng.normal(0,.15,4)))
        m=TrajectoryMixture(2,n_init=1,max_iter=300).fit(records)
        self.assertTrue(np.all(np.diff(m.history_)>=-1e-6))
        self.assertGreater(adjusted_rand_score(np.repeat([0,1],80),m.predict_proba(records).argmax(axis=1)),.95)

    def test_greedy_nmi_objective_and_label_invariance(self):
        from .ensembles import greedy_nmi
        from sklearn.metrics import normalized_mutual_info_score
        truth=np.repeat([0,1,2],20);rng=np.random.default_rng(11)
        partitions=[]
        for j in range(8):
            labels=truth.copy();ids=rng.choice(60,5,replace=False);labels[ids]=rng.integers(3,size=5)
            partitions.append((labels+j)%3)
        consensus,objective=greedy_nmi(partitions,3)
        self.assertAlmostEqual(objective,np.mean([normalized_mutual_info_score(consensus,p) for p in partitions]),places=10)
        best=max(np.mean([normalized_mutual_info_score(a,b) for b in partitions]) for a in partitions)
        self.assertGreaterEqual(objective,best-1e-10)
        self.assertGreater(adjusted_rand_score(consensus,truth),.9)


if __name__=='__main__':
    with threadpool_limits(1):
        unittest.main()
