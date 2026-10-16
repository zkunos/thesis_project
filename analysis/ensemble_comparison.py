import numpy as np
import pandas as pd
import joblib
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import linkage,fcluster
from sklearn.decomposition import NMF
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score,normalized_mutual_info_score,silhouette_score
from .ensembles import greedy_nmi


def run(s,out):
    predictions=joblib.load(out/'imputation_predictions.joblib');rows=[]
    for label,parts in predictions.items():
        method,ktext=label.split(':');k=int(ktext);n=parts.shape[1]
        C=np.zeros((n,n),np.float64)
        for p in parts:C+=(p[:,None]==p[None,:])/len(parts)
        distance=np.maximum(0,1-C);np.fill_diagonal(distance,0)
        agg=fcluster(linkage(squareform(distance,checks=False),method='average'),k,criterion='maxclust')-1
        greedy,obj=greedy_nmi(parts,k,seed=20261015)
        factor=NMF(n_components=k,init='nndsvda',max_iter=300,random_state=20261015)
        nmf=factor.fit_transform(C).argmax(axis=1)
        for name,cons in [('average_linkage',agg),('greedy_mean_nmi',greedy),('nmf',nmf)]:
            rows.append(dict(method=method,k=k,ensemble=name,k_observed=len(np.unique(cons)),
                mean_nmi_to_partitions=np.mean([normalized_mutual_info_score(cons,p) for p in parts]),
                mean_ari_to_partitions=np.mean([adjusted_rand_score(cons,p) for p in parts]),
                original_space_silhouette=silhouette_score(s['D'][s['test']],cons) if len(np.unique(cons))>1 else np.nan,
                minimum_fraction=np.unique(cons,return_counts=True)[1].min()/n,
                nmf_iterations=factor.n_iter_ if name=='nmf' else np.nan))
        print(f'Ensemble comparisons {label}',flush=True)
    pd.DataFrame(rows).to_csv(out/'ensemble_comparison.csv',index=False)
    draws=joblib.load(out/'multiple_imputation_domains.joblib');counts=[]
    for draw,(A,B) in enumerate(draws):
        candidates=[]
        for k in range(2,9):
            m=KMeans(k,n_init=10,random_state=20261015).fit(A)
            score=silhouette_score(A,m.labels_,sample_size=1000,random_state=20261015)
            candidates.append((score,k))
        score,k=max(candidates)
        counts.append(dict(draw=draw,k_selected=k,training_silhouette=score,method='kmeans',selection='maximum training silhouette, k=2..8'))
    pd.DataFrame(counts).to_csv(out/'cluster_count_distribution.csv',index=False)
