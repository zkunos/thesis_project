"""Post hoc scaling sensitivity prompted by training-set ceiling concentrations."""
import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score,silhouette_score
from .preprocessing import DOMAINS
from .medoids import SampledPAM


def run(s,out):
    tr,te=s['train'],s['test'];standard=StandardScaler().fit(s['domains'][tr]);Z=standard.transform(s['domains'])
    pca=PCA().fit(Z[tr]);rows=[];assign={};models={};profiles=[]
    base=KMeans(3,n_init=20,random_state=20261015).fit(s['D'][tr]).predict(s['D'][te])
    for representation,X in [('equal_domain',Z),('equal_domain_residual',pca.transform(Z)[:,1:])]:
        for method in ['kmeans','pam']:
            for k in range(2,9):
                m=KMeans(k,n_init=15,random_state=20261015) if method=='kmeans' else SampledPAM(k,seed=20261015)
                m.fit(X[tr]);a=m.predict(X[tr]);b=m.predict(X[te]);label=f'{representation}:{method}:{k}'
                rows.append(dict(model=label,representation=representation,method=method,k=k,
                    train_silhouette=silhouette_score(X[tr],a,sample_size=2000,random_state=20261015),
                    validation_silhouette=silhouette_score(X[te],b),
                    validation_silhouette_common_equal_domain=silhouette_score(Z[te],b),
                    minimum_fraction=np.bincount(a).min()/len(tr),ari_vs_robust_k3=adjusted_rand_score(base,b)))
                assign[label]=m.predict(X);models[label]=m
                if k==3:
                    for c in range(3):
                        for j,d in enumerate(DOMAINS):profiles.append(dict(model=label,cluster=c,domain=d,n=int((b==c).sum()),mean=float(s['domains'][te][b==c,j].mean())))
    pd.DataFrame(rows).to_csv(out/'scaling_sensitivity.csv',index=False)
    pd.DataFrame(profiles).to_csv(out/'scaling_profiles.csv',index=False)
    pd.DataFrame(dict(domain=list(DOMAINS),robust_scaled_variance=s['D'][tr].var(axis=0),
        equal_domain_variance=Z[tr].var(axis=0),robust_pc1_loading=s['pca'].components_[0],
        equal_domain_pc1_loading=pca.components_[0])).to_csv(out/'scaling_audit.csv',index=False)
    fit=KMeans(3,n_init=20,random_state=20261015).fit(Z[tr]);pred=fit.predict(Z[te])
    pd.DataFrame([dict(robust_k3_silhouette_robust=silhouette_score(s['D'][te],base),
        robust_k3_silhouette_equal_domain=silhouette_score(Z[te],base),
        equal_k3_silhouette_equal_domain=silhouette_score(Z[te],pred),
        equal_k3_silhouette_robust=silhouette_score(s['D'][te],pred),
        ari_robust_vs_equal=adjusted_rand_score(base,pred),
        equal_domain_pc1_variance=pca.explained_variance_ratio_[0])]).to_csv(out/'common_geometry_comparison.csv',index=False)
    mirows=[];draws=joblib.load(out/'multiple_imputation_domains.joblib')
    for k in [2,3,4]:
        predictions=[]
        for A,B in draws:
            sc=StandardScaler().fit(A);m=KMeans(k,n_init=10,random_state=20261015).fit(sc.transform(A))
            predictions.append(m.predict(sc.transform(B)))
        aris=[adjusted_rand_score(predictions[a],predictions[b]) for a in range(len(draws)) for b in range(a)]
        mirows.append(dict(k=k,mean_ari=np.mean(aris),median_ari=np.median(aris),ari_p05=np.quantile(aris,.05),ari_p95=np.quantile(aris,.95)))
    pd.DataFrame(mirows).to_csv(out/'equal_domain_imputation_stability.csv',index=False)
    joblib.dump(dict(assign=assign,models=models,Z=Z,pca=pca),out/'equal_domain_models.joblib')
