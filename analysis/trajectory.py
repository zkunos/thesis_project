"""Patient likelihood mixture of linear trajectories with shared random effects.

Integrates Gaussian random intercept/slope uncertainty; does not cluster noisy
individual slope estimates. Linear elapsed-time trajectories are exploratory.
"""
import time
import numpy as np
import pandas as pd
from scipy.special import logsumexp
from sklearn.cluster import KMeans
from .mixtures import positive_definite


def sufficient(records):
    A=[];b=[];yy=[];ns=[]
    for t,y in records:
        Z=np.column_stack([np.ones(len(t)),t])
        A.append(Z.T@Z);b.append(Z.T@y);yy.append(y@y);ns.append(len(t))
    return np.array(A),np.array(b),np.array(yy),np.array(ns)


class TrajectoryMixture:
    def __init__(self,k=1,n_init=3,max_iter=200,seed=42):
        self.k,self.n_init,self.max_iter,self.seed=k,n_init,max_iter,seed

    def terms(self,stat,beta,D,noise):
        A,b,yy,ns=stat
        C=np.linalg.inv(np.linalg.inv(D)[None]+A/noise)
        residual_b=b[:,None,:]-np.einsum('nij,kj->nki',A,beta)
        rss=yy[:,None]-2*b@beta.T+np.einsum('ki,nij,kj->nk',beta,A,beta)
        mahal=rss/noise-np.einsum('nki,nij,nkj->nk',residual_b,C,residual_b)/noise**2
        logdet=ns*np.log(noise)+np.linalg.slogdet(D)[1]-np.linalg.slogdet(C)[1]
        lp=-.5*(ns[:,None]*np.log(2*np.pi)+logdet[:,None]+mahal)
        random_means=np.einsum('nij,nkj->nki',C,residual_b)/noise
        return lp,C,random_means

    def fit(self,records):
        stat=sufficient(records);A,b,yy,ns=stat;n=len(ns);best=None
        slopes=np.linalg.solve(A+np.eye(2)[None]*.01,b[...,None])[...,0]
        for start in range(self.n_init):
            labs=KMeans(self.k,n_init=5,random_state=self.seed+start).fit_predict(slopes)
            beta=np.array([slopes[labs==g].mean(axis=0) for g in range(self.k)])
            D=np.diag([.3,.1]);noise=.3;weights=np.bincount(labs,minlength=self.k)/n;history=[]
            for iteration in range(self.max_iter):
                lp,C,random_mean=self.terms(stat,beta,D,noise)
                joint=lp+np.log(weights);den=logsumexp(joint,axis=1);ll=float(den.sum());history.append(ll)
                if iteration and abs(ll-history[-2])/n<1e-5:break
                R=np.exp(joint-den[:,None]);weights=np.maximum(R.mean(axis=0),1e-8);weights/=weights.sum()
                for g in range(self.k):
                    beta[g]=np.linalg.solve(np.einsum('n,nij->ij',R[:,g],A)+np.eye(2)*1e-8,
                        np.einsum('n,ni->i',R[:,g],b-np.einsum('nij,nj->ni',A,random_mean[:,g])))
                D=np.mean(C,axis=0)+np.einsum('nk,nki,nkj->ij',R,random_mean,random_mean)/n
                D=positive_definite(D,1e-5)
                fitted=beta[None]+random_mean
                residual=yy[:,None]-2*np.einsum('ni,nki->nk',b,fitted)+np.einsum('nki,nij,nkj->nk',fitted,A,fitted)
                noise=max(float((np.sum(R*residual)+np.einsum('nij,nji->',A,C))/ns.sum()),1e-5)
            lp,_,_=self.terms(stat,beta,D,noise)
            ll=float(logsumexp(lp+np.log(weights),axis=1).sum())
            if best is None or ll>best[0]:best=(ll,beta.copy(),D.copy(),noise,weights.copy(),history)
        self.loglik_,self.beta_,self.D_,self.noise_,self.weights_,self.history_=best
        self.converged_=len(self.history_)<self.max_iter
        self.n_parameters_=2*self.k+3+1+self.k-1
        return self

    def predict_proba(self,records):
        lp,_,_=self.terms(sufficient(records),self.beta_,self.D_,self.noise_)
        joint=lp+np.log(self.weights_)
        return np.exp(joint-logsumexp(joint,axis=1)[:,None])

    def score_samples(self,records):
        lp,_,_=self.terms(sufficient(records),self.beta_,self.D_,self.noise_)
        return logsumexp(lp+np.log(self.weights_),axis=1)


def run(state,out):
    import joblib
    from sklearn.metrics import adjusted_rand_score
    df=state['df'].copy();pp=state['pp']
    completed=state['imp'].transform(pp.transform_tests(df[pp.columns_]))
    D=state['scaler'].transform(pp.aggregate(completed))
    pc=state['pca'].transform(D)[:,0]
    pc*=1 if state['pca'].components_[0].sum()>0 else -1
    df['severity']=pc/np.std(state['severity'][state['train']])
    training_ids=set(state['index'].iloc[state['train']].ID)
    records=[];meta=[]
    for patient,g in df.groupby('ID',sort=True):
        g=g[g.observed_tests>=7].sort_values('TSI_TO_ASSESSMENT_DAYS')
        if len(g)<3 or g.AGE_INJURY.nunique()!=1:continue
        time_years=(g.TSI_TO_ASSESSMENT_DAYS.to_numpy()-g.TSI_TO_ASSESSMENT_DAYS.min())/365.25
        if time_years[-1]<.25 or time_years[-1]>5 or len(np.unique(time_years))<3:continue
        records.append((time_years,g.severity.to_numpy()))
        meta.append(dict(patient_key=g.patient_key.iloc[0],train=patient in training_ids,n_visits=len(g),span_years=time_years[-1]))
    meta=pd.DataFrame(meta);meta.to_csv(out/'trajectory_included_patients.csv',index=False)
    train=np.flatnonzero(meta.train.to_numpy());test=np.flatnonzero(~meta.train.to_numpy())
    A=[records[i] for i in train];B=[records[i] for i in test]
    rows=[];models={}
    for k in range(1,5):
        start=time.time();m=TrajectoryMixture(k,n_init=3,max_iter=300,seed=20261015).fit(A)
        P=m.predict_proba(A);V=m.predict_proba(B);n=len(A)
        rows.append(dict(k=k,n_train=n,n_validation=len(B),converged=m.converged_,iterations=len(m.history_),
            bic=-2*m.loglik_+m.n_parameters_*np.log(n),
            validation_loglik=m.score_samples(B).mean(),minimum_train_class_fraction=P.mean(axis=0).min(),
            validation_mean_max_probability=V.max(axis=1).mean(),seconds=time.time()-start))
        models[k]=m
        print(f'Trajectory k={k}: {rows[-1]}',flush=True)
    table=pd.DataFrame(rows);table.to_csv(out/'trajectory_model_comparison.csv',index=False)
    eligible=table[table.converged & (table.minimum_train_class_fraction>=.05)]
    selected=int(eligible.loc[eligible.bic.idxmin(),'k']) if len(eligible) else 1
    model=models[selected];P=model.predict_proba(B)
    result=meta.iloc[test].copy();result['cluster']=P.argmax(axis=1);result['maximum_probability']=P.max(axis=1)
    result.to_csv(out/'trajectory_membership_uncertainty.csv',index=False)
    coefficients=pd.DataFrame(model.beta_,columns=['intercept','slope_per_year']);coefficients['weight']=model.weights_
    coefficients.to_csv(out/'trajectory_coefficients.csv',index=False)
    joblib.dump(dict(models=models,records=records,meta=meta,selected=selected),out/'trajectory_models.joblib')
    # Patient resampling for selected k, retaining full within-patient records.
    rng=np.random.default_rng(20261015);stability=[]
    if selected>1:
        for repeat in range(20):
            ids=rng.choice(len(A),int(.8*len(A)),replace=False)
            fit=TrajectoryMixture(selected,n_init=2,max_iter=200,seed=repeat).fit([A[i] for i in ids])
            stability.append(dict(repeat=repeat,converged=fit.converged_,ari=adjusted_rand_score(P.argmax(axis=1),fit.predict_proba(B).argmax(axis=1))))
    pd.DataFrame(stability,columns=['repeat','converged','ari']).to_csv(out/'trajectory_stability.csv',index=False)
