"""Preprocessing correction, missingness, and independent-discovery checks."""
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer,KNNImputer,IterativeImputer
from sklearn.preprocessing import RobustScaler,StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score,silhouette_score
from scipy.stats import chi2_contingency
from .preprocessing import CognitivePreprocessor,compute_domain_scores,FEATURES,DOMAINS


def run(s,root,out):
    tr,te=s['train'],s['test'];base=KMeans(3,n_init=20,random_state=20261015).fit(s['D'][tr]).predict(s['D'][te])
    rows=[];labels={}
    for name,imputer in [('mean',SimpleImputer()),('knn',KNNImputer(n_neighbors=5,weights='distance')),
                         ('iterative',s['imp'])]:
        if name=='iterative': A=s['completed'][tr];B=s['completed'][te]
        else:A=imputer.fit_transform(s['X'][tr]);B=imputer.transform(s['X'][te])
        scaler=RobustScaler().fit(s['pp'].aggregate(A));X=scaler.transform(s['pp'].aggregate(A));Y=scaler.transform(s['pp'].aggregate(B))
        m=KMeans(3,n_init=20,random_state=20261015).fit(X);p=m.predict(Y);labels[name]=p
        rows.append(dict(experiment=name,n_train=len(tr),n_validation=len(te),ari_vs_reference=adjusted_rand_score(base,p),
            validation_silhouette=silhouette_score(s['D'][te],p)))
    eligible=s['index'].observed_tests.to_numpy()>=7
    subset_tr=tr[eligible[tr]];subset_te=te[eligible[te]]
    for name,clip in [('at_least_7_observed',(.01,.99)),('no_clipping',(0.,1.)),('iterative_50_iterations',(.01,.99))]:
        ids=subset_tr if name=='at_least_7_observed' else tr
        testids=subset_te if name=='at_least_7_observed' else te
        pp=CognitivePreprocessor(clip=clip).fit(s['index'].iloc[ids][FEATURES])
        imp=IterativeImputer(max_iter=50 if name=='iterative_50_iterations' else 15,
            random_state=20261015,min_value=pp.min_,max_value=pp.max_)
        A=imp.fit_transform(pp.transform_tests(s['index'].iloc[ids][FEATURES]));B=imp.transform(pp.transform_tests(s['index'].iloc[testids][FEATURES]))
        scaler=RobustScaler().fit(pp.aggregate(A));X=scaler.transform(pp.aggregate(A));Y=scaler.transform(pp.aggregate(B))
        p=KMeans(3,n_init=20,random_state=20261015).fit(X).predict(Y)
        base_compare=base[eligible[te]] if name=='at_least_7_observed' else base
        rows.append(dict(experiment=name,n_train=len(ids),n_validation=len(testids),ari_vs_reference=adjusted_rand_score(base_compare,p),
            validation_silhouette=silhouette_score(s['D'][testids],p),imputation_iterations=imp.n_iter_))
    independent=KMeans(3,n_init=20,random_state=20261015).fit_predict(s['D'][te])
    rows.append(dict(experiment='independent_validation_discovery_fixed_training_transform',n_train=len(te),n_validation=len(te),
        ari_vs_reference=adjusted_rand_score(base,independent),validation_silhouette=silhouette_score(s['D'][te],independent)))
    pd.DataFrame(rows).to_csv(out/'missingness_sensitivity.csv',index=False)
    missing=[]
    for col in FEATURES:
        flag=s['index'].iloc[te][col].isna().to_numpy()
        tab=pd.crosstab(base,flag)
        v=np.sqrt(chi2_contingency(tab,correction=False)[0]/len(te)) if tab.shape[1]>1 else 0.
        for cluster in range(3):
            missing.append(dict(variable=col,cluster=cluster,missing_fraction=float(flag[base==cluster].mean()),cramers_v=v))
    pd.DataFrame(missing).to_csv(out/'cluster_missingness_association.csv',index=False)
    # Isolate the old NB14 aggregation mismatch using identical existing values.
    full=pd.read_csv(root/'data/imputed_csv/Imputed_MICE.csv',index_col=0)
    raw=s['df'];assert full.index.equals(raw.index)
    corrected=compute_domain_scores(full[FEATURES],DOMAINS,weights=(1-raw[FEATURES].isna().mean()).to_dict()).to_numpy()
    raw_matrix=full[FEATURES].to_numpy()
    W=CognitivePreprocessor().fit(raw[FEATURES]).matrix_
    naive=raw_matrix@W
    checks=[]
    for cohort,ids in [('all_assessments',np.arange(len(full))),('complete_cases',np.flatnonzero(raw[FEATURES].notna().all(axis=1)))]:
        # Corrected transforms are refitted within each descriptive cohort,
        # reproducing the intended legacy branch (no held-out claim).
        good=compute_domain_scores(full.iloc[ids][FEATURES],DOMAINS,weights=(1-raw[FEATURES].isna().mean()).to_dict()).to_numpy()
        A=StandardScaler().fit_transform(naive[ids]);B=StandardScaler().fit_transform(good)
        pa=KMeans(3,n_init=20,random_state=42).fit_predict(A);pb=KMeans(3,n_init=20,random_state=42).fit_predict(B)
        checks.append(dict(cohort=cohort,n=len(ids),ari_naive_vs_corrected=adjusted_rand_score(pa,pb),
            naive_silhouette=silhouette_score(A,pa,sample_size=2000,random_state=42),
            corrected_silhouette=silhouette_score(B,pb,sample_size=2000,random_state=42),
            attention_score_correlation=float(np.corrcoef(A[:,1],B[:,1])[0,1])))
    pd.DataFrame(checks).to_csv(out/'preprocessing_correction_impact.csv',index=False)
