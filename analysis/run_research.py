"""Run with python -m analysis.run_research --stage prepare|benchmark|robust|ensemble|calibration|trajectory|report."""
from __future__ import annotations
import os
os.environ.setdefault('OMP_NUM_THREADS','1')
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('MKL_NUM_THREADS','1')
os.environ.setdefault('NUMBA_NUM_THREADS','1')
from pathlib import Path
import argparse, json, time, warnings, importlib.metadata, platform
import numpy as np
import pandas as pd
import joblib
from scipy.optimize import linear_sum_assignment
from scipy.spatial.distance import cdist, squareform
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.stats import norm, rankdata
from sklearn.experimental import enable_iterative_imputer  # noqa
from sklearn.impute import IterativeImputer
from sklearn.preprocessing import RobustScaler, StandardScaler
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score, silhouette_score
from sklearn.model_selection import train_test_split
from threadpoolctl import threadpool_limits
from .preprocessing import CognitivePreprocessor, compute_domain_scores, FEATURES, DOMAINS
from .data_contract import load_verified, sha256
from .mixtures import MissingMixture, positive_definite
from .medoids import SampledPAM

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results/research_2026'
OUT.mkdir(exist_ok=True,parents=True)
SEED=20261015

def log(s): print(time.strftime('%H:%M:%S'),s,flush=True)
def save_json(name,data): (OUT/name).write_text(json.dumps(data,indent=2,default=str),encoding='utf-8')
def cache(): return joblib.load(OUT/'prepared.joblib')
def metrics(X,labels,seed=SEED):
    labels=np.asarray(labels); good=labels>=0; k=len(np.unique(labels[good]))
    sizes=np.bincount(labels[good]) if good.any() else np.array([])
    sizes=sizes[sizes>0]
    sil=np.nan
    if k>1 and good.sum()>k:
        sil=float(silhouette_score(X[good],labels[good],sample_size=min(2000,good.sum()),random_state=seed))
    return dict(k_observed=k,coverage=float(good.mean()),silhouette=sil,
        minimum_cluster_fraction=float(sizes.min()/len(X)) if len(sizes) else 0.)


def prepare():
    df,index,audit=load_verified(ROOT,OUT)
    train,test=train_test_split(np.arange(len(index)),test_size=.2,random_state=SEED)
    train=np.sort(train);test=np.sort(test)
    pp=CognitivePreprocessor().fit(index.iloc[train][FEATURES])
    X=pp.transform_tests(index[FEATURES])
    imp=IterativeImputer(max_iter=15,random_state=SEED,min_value=pp.min_,max_value=pp.max_)
    imp.fit(X[train]); completed=imp.transform(X)
    domains=pp.aggregate(completed)
    scaler=RobustScaler().fit(domains[train]);D=scaler.transform(domains)
    pca=PCA().fit(D[train]); PCs=pca.transform(D)
    # Orient PC1 so larger values consistently mean better cognitive scores.
    sign=1. if pca.components_[0].sum()>0 else -1.
    severity=PCs[:,0]*sign
    state=dict(df=df,index=index,train=train,test=test,pp=pp,X=X,completed=completed,
        domains=domains,D=D,pca=pca,residual=PCs[:,1:],severity=severity,imp=imp,scaler=scaler)
    joblib.dump(state,OUT/'prepared.joblib')
    manifest=index[['assessment_key','patient_key','source_row','observed_tests']].copy()
    manifest['split']='discovery';manifest.iloc[test,manifest.columns.get_loc('split')]='validation'
    manifest.to_csv(OUT/'index_patient_manifest.csv',index=False)
    profile=[]
    for j,col in enumerate(FEATURES):
        v=index[col].dropna()
        profile.append(dict(variable=col,missing_fraction=float(index[col].isna().mean()),
            unique_values=int(v.nunique()),minimum=float(v.min()),maximum=float(v.max()),
            maximum_mass=float((v==v.max()).mean()),minimum_mass=float((v==v.min()).mean()),
            training_clip_low=float(pp.lo_[j]),training_clip_high=float(pp.hi_[j])))
    pd.DataFrame(profile).to_csv(OUT/'feature_audit.csv',index=False)
    versions={m:importlib.metadata.version(m) for m in ['numpy','pandas','scipy','scikit-learn','umap-learn','hdbscan','diptest','statsmodels','matplotlib']}
    save_json('run_manifest.json',dict(seed=SEED,python=platform.python_version(),versions=versions,
        train_patients=len(train),validation_patients=len(test),
        input_hashes={str(p.relative_to(ROOT)):sha256(p) for p in [ROOT/'data/0_tests2.xlsx',ROOT/'results/eligible_data_matrix.csv']},
        pc_explained_variance=pca.explained_variance_ratio_.tolist(),
        design='Earliest eligible assessment per patient; frozen 80/20 split; no clinical outcome used for selection',
        caveats=['Source has no natural assessment key','Time is relative to injury field, not verified episode ID',
                 'All legacy eligible records retained; at least 7 observed tests tested separately',
                 'Selection of the retained 14 variables inherited from the full historical cohort'] ))
    log(f'Prepared {len(index)} patients: {len(train)} discovery, {len(test)} validation; PC1 {pca.explained_variance_ratio_[0]:.3f}')


def benchmark():
    s=cache();tr,te=s['train'],s['test'];rows=[];assign={};models={}
    import diptest
    tendency=[]
    for name,X in [('domains',s['D']),('residual',s['residual']),
                   ('without_orientation',s['D'][:,1:]),('tests',s['completed'])]:
        pc=PCA(n_components=1).fit(X[tr]).transform(X[tr]).ravel()
        dip,p=diptest.diptest(pc)
        tendency.append(dict(representation=name,n=len(tr),dip=dip,p_value=p,
            interpretation='Exploratory; discrete score limits may induce modes'))
        methods=['kmeans','pam','gmm_full','gmm_tied'] if name in ['domains','residual'] else ['kmeans']
        for method in methods:
            for k in range(1 if method.startswith('gmm') else 2,9):
                t=time.time()
                if method=='kmeans': m=KMeans(n_clusters=k,n_init=15,random_state=SEED)
                elif method=='pam':m=SampledPAM(k,sample_size=400,n_samples=3,seed=SEED)
                else:m=GaussianMixture(k,covariance_type=method.split('_')[1],n_init=5,max_iter=300,reg_covar=.01,random_state=SEED)
                m.fit(X[tr]);a=m.predict(X[tr]);b=m.predict(X[te]);label=f'{name}:{method}:{k}'
                row=dict(model=label,representation=name,method=method,k_requested=k,seconds=time.time()-t,
                    converged=bool(getattr(m,'converged_',True)),**{'train_'+q:v for q,v in metrics(X[tr],a).items()},
                    **{'validation_'+q:v for q,v in metrics(X[te],b).items()})
                if method.startswith('gmm'):
                    P=m.predict_proba(X[tr]);row.update(bic=m.bic(X[tr]),icl=m.bic(X[tr])-2*np.sum(P*np.log(P+1e-15)),
                        validation_loglik=m.score(X[te]))
                rows.append(row);assign[label]=m.predict(X);models[label]=m
            log(f'{name} {method} finished')
    pd.DataFrame(tendency).to_csv(OUT/'clusterability.csv',index=False)
    import hdbscan
    for neighbors in [None,15,50]:
        if neighbors is None: Xtr=s['D'][tr];Xte=s['D'][te]; reducer=None
        else:
            import umap
            reducer=umap.UMAP(n_components=3,n_neighbors=neighbors,min_dist=0.,random_state=SEED,n_jobs=1)
            Xtr=reducer.fit_transform(s['D'][tr]);Xte=reducer.transform(s['D'][te])
        for size in [100,300]:
            t=time.time();m=hdbscan.HDBSCAN(min_cluster_size=size,min_samples=20,prediction_data=True).fit(Xtr)
            labels=m.labels_; val=hdbscan.approximate_predict(m,Xte)[0] if np.any(labels>=0) else np.full(len(te),-1)
            name=f'hdbscan:{neighbors}:{size}'
            rows.append(dict(model=name,representation='domains',method='hdbscan' if neighbors is None else 'umap_hdbscan',
                k_requested=-1,seconds=time.time()-t,converged=True,
                **{'train_'+q:v for q,v in metrics(s['D'][tr],labels).items()},
                **{'validation_'+q:v for q,v in metrics(s['D'][te],val).items()},
                embedding_silhouette=metrics(Xtr,labels)['silhouette']))
            all_labels=np.empty(len(s['index']),int);all_labels[tr]=labels;all_labels[te]=val
            assign[name]=all_labels;models[name]=(reducer,m)
        log(f'HDBSCAN neighbors={neighbors} finished')
    table=pd.DataFrame(rows);table['selected_by_training']=False
    for (_,method),g in table.groupby(['representation','method']):
        viable=g[(g.converged)&(g.train_minimum_cluster_fraction>=.02)]
        if not method.startswith('gmm'):viable=viable[viable.train_silhouette.notna()]
        if len(viable):
            winner=viable.bic.idxmin() if method.startswith('gmm') else viable.train_silhouette.idxmax()
            if pd.notna(winner):table.loc[winner,'selected_by_training']=True
    table.to_csv(OUT/'model_comparison.csv',index=False)
    joblib.dump(dict(assign=assign,models=models),OUT/'benchmarks.joblib')
    profile_rows=[]
    for label in table.loc[table.selected_by_training,'model']:
        for cluster in np.unique(assign[label][te]):
            mask=assign[label][te]==cluster
            for j,domain in enumerate(DOMAINS):
                profile_rows.append(dict(model=label,cluster=int(cluster),domain=domain,n=int(mask.sum()),
                    validation_mean=float(s['domains'][te][mask,j].mean())))
    pd.DataFrame(profile_rows).to_csv(OUT/'validation_profiles.csv',index=False)
    log('Benchmark complete')


def robust(family_name=None,resume=False):
    s=cache();tr,te=s['train'],s['test']
    for name,kwargs in [('normal',{}),('t4',{'family':'t','df':4}),('t10',{'family':'t','df':10}),
                        ('contaminated',{'family':'contaminated'})]:
        if family_name is not None and name!=family_name:continue
        csv_path=OUT/f'incomplete_mixture_comparison_{name}.csv'
        model_path=OUT/f'incomplete_models_{name}.joblib'
        rows=pd.read_csv(csv_path).to_dict('records') if resume and csv_path.exists() else []
        models=joblib.load(model_path) if resume and model_path.exists() else {}
        if resume and not rows and (OUT/'incomplete_mixture_comparison.csv').exists():
            old=pd.read_csv(OUT/'incomplete_mixture_comparison.csv')
            rows=old[old.family==name].to_dict('records')
            old_models=joblib.load(OUT/'incomplete_models.joblib')
            models={key:value for key,value in old_models.items() if key.startswith(name+':')}
        for k in range(1,9):
            if any(row['k']==k for row in rows):continue
            t=time.time();m=MissingMixture(k,**kwargs,n_init=2,max_iter=120,reg=.02,seed=SEED).fit(s['X'][tr])
            a=m.predict(s['X'][tr]);b=m.predict(s['X'][te]);P=m.predict_proba(s['X'][te])
            row=dict(family=name,k=k,converged=m.converged_,iterations=m.n_iter_,seconds=time.time()-t,
                bic=m.bic(s['X'][tr]),icl=m.icl(s['X'][tr]),validation_loglik=m.score_samples(s['X'][te]).mean(),
                validation_mean_entropy=float(-np.sum(P*np.log(P+1e-15),axis=1).mean()),
                min_covariance_eigenvalue=float(min(np.linalg.eigvalsh(C).min() for C in m.covariances_)),
                **{'train_'+q:v for q,v in metrics(s['D'][tr],a).items()},
                **{'validation_'+q:v for q,v in metrics(s['D'][te],b).items()})
            rows.append(row);models[f'{name}:{k}']=m
            pd.DataFrame(rows).to_csv(csv_path,index=False)
            joblib.dump(models,model_path)
            log(f'Missing mixture {name} k={k} BIC={row["bic"]:.1f}, converged={m.converged_}, {time.time()-t:.1f}s')


def align(reference,labels):
    ref=np.unique(reference);new=np.unique(labels)
    overlap=np.array([[np.sum((reference==a)&(labels==b)) for b in new] for a in ref])
    a,b=linear_sum_assignment(-overlap)
    mapping={new[j]:ref[i] for i,j in zip(a,b)}
    return np.array([mapping.get(v,-1) for v in labels])


def ensemble():
    s=cache();tr,te=s['train'],s['test'];rng=np.random.default_rng(SEED)
    rows=[];all_predictions={};counter=[]
    completed_draws=[]
    for draw in range(20):
        imp=IterativeImputer(max_iter=10,sample_posterior=True,random_state=SEED+draw,
            min_value=s['pp'].min_,max_value=s['pp'].max_)
        Xi=imp.fit_transform(s['X'][tr]);Xv=imp.transform(s['X'][te])
        scaler=RobustScaler().fit(s['pp'].aggregate(Xi))
        completed_draws.append((scaler.transform(s['pp'].aggregate(Xi)),scaler.transform(s['pp'].aggregate(Xv))))
    joblib.dump(completed_draws,OUT/'multiple_imputation_domains.joblib')
    for method in ['kmeans','pam']:
        for k in [2,3,4]:
            pred=[]
            for draw in range(20):
                A,B=completed_draws[draw]
                m=(KMeans(n_clusters=k,n_init=10,random_state=SEED) if method=='kmeans'
                   else SampledPAM(k,sample_size=300,n_samples=2,seed=SEED))
                m.fit(A);pred.append(m.predict(B))
            pred=np.array(pred);label=f'{method}:{k}';all_predictions[label]=pred
            aris=[adjusted_rand_score(pred[a],pred[b]) for a in range(20) for b in range(a)]
            rows.append(dict(source='imputation_draw',method=method,k=k,n_repeats=20,mean_ari=np.mean(aris),
                median_ari=np.median(aris),ari_p05=np.quantile(aris,.05),ari_p95=np.quantile(aris,.95)))
            # Aggregate in held-out space only to summarize independent training fits.
            # This consensus is descriptive, not a trainable validation predictor.
            C=np.zeros((len(te),len(te)),np.float32)
            for p in pred:C+=(p[:,None]==p[None,:])/len(pred)
            distance=np.maximum(0,1-C);np.fill_diagonal(distance,0)
            cons=fcluster(linkage(squareform(distance,checks=False),method='average'),k,criterion='maxclust')-1
            aligned=np.array([align(cons,p) for p in pred])
            confidence=np.mean(aligned==cons,axis=0)
            pd.DataFrame(dict(patient_key=s['index'].iloc[te].patient_key,consensus=cons,
                agreement=confidence,observed_tests=s['index'].iloc[te].observed_tests)).to_csv(OUT/f'assignment_uncertainty_{method}_{k}.csv',index=False)
            counter.append(dict(method=method,k=k,mean_agreement=confidence.mean(),fraction_at_least_80=float((confidence>=.8).mean()),
                                minimum_consensus_fraction=np.bincount(cons).min()/len(te)))
            log(f'MI {method} k={k}: mean ARI {np.mean(aris):.3f}')
    # Separate preprocessing/imputation/subsampling changes from algorithm seeds.
    baseline=KMeans(n_clusters=3,n_init=20,random_state=SEED).fit(s['D'][tr]).predict(s['D'][te])
    stability=[];J=[]
    for source in ['patient_subsample','initialization']:
        predictions=[]
        for repeat in range(50):
            if source=='patient_subsample':
                ids=rng.choice(tr,int(.8*len(tr)),replace=False)
                pp=CognitivePreprocessor().fit(s['index'].iloc[ids][FEATURES])
                imp=IterativeImputer(max_iter=10,random_state=SEED,min_value=pp.min_,max_value=pp.max_)
                Xi=imp.fit_transform(pp.transform_tests(s['index'].iloc[ids][FEATURES]))
                Xv=imp.transform(pp.transform_tests(s['index'].iloc[te][FEATURES]))
                scaler=RobustScaler().fit(pp.aggregate(Xi));A=scaler.transform(pp.aggregate(Xi));B=scaler.transform(pp.aggregate(Xv))
            else:A=s['D'][tr];B=s['D'][te]
            model=KMeans(n_clusters=3,n_init=10,random_state=SEED+repeat).fit(A)
            p=model.predict(B);predictions.append(p);mapped=align(baseline,p)
            stability.append(dict(source=source,repeat=repeat,ari_vs_reference=adjusted_rand_score(baseline,p)))
            for c in range(3):
                union=(baseline==c)|(mapped==c);inter=(baseline==c)&(mapped==c)
                J.append(dict(source=source,repeat=repeat,cluster=c,jaccard=inter.sum()/union.sum()))
        aris=[adjusted_rand_score(predictions[a],predictions[b]) for a in range(50) for b in range(a)]
        rows.append(dict(source=source,method='kmeans',k=3,n_repeats=50,mean_ari=np.mean(aris),median_ari=np.median(aris),ari_p05=np.quantile(aris,.05),ari_p95=np.quantile(aris,.95)))
        log(f'{source} mean ARI {np.mean(aris):.3f}')
    pd.DataFrame(rows).to_csv(OUT/'refit_agreement.csv',index=False)
    pd.DataFrame(counter).to_csv(OUT/'consensus_summary.csv',index=False)
    pd.DataFrame(stability).to_csv(OUT/'patient_stability.csv',index=False)
    pd.DataFrame(J).to_csv(OUT/'per_cluster_stability.csv',index=False)
    joblib.dump(all_predictions,OUT/'imputation_predictions.joblib')


def calibration():
    import diptest
    s=cache();rng=np.random.default_rng(SEED);n=1000;tr=s['train'];raw=s['index'].iloc[tr][FEATURES]
    ids=rng.choice(len(raw),n,replace=False);obs=raw.iloc[ids]
    def screen(frame):
        pp=CognitivePreprocessor().fit(frame)
        imp=IterativeImputer(max_iter=7,random_state=SEED,min_value=pp.min_,max_value=pp.max_)
        Z=imp.fit_transform(pp.transform_tests(frame));D=RobustScaler().fit_transform(pp.aggregate(Z))
        pc=PCA(n_components=1).fit_transform(D).ravel()
        scores=[]
        for k in range(2,9):
            labels=KMeans(n_clusters=k,n_init=5,random_state=SEED).fit_predict(D)
            scores.append(silhouette_score(D,labels))
        return float(max(scores)),int(np.argmax(scores)+2),float(diptest.diptest(pc)[0])
    observed=screen(obs)
    gaussian=np.empty(raw.shape)
    for j,col in enumerate(FEATURES):
        v=raw[col].to_numpy(float);mask=np.isfinite(v);gaussian[:,j]=np.nan
        gaussian[mask,j]=norm.ppf((rankdata(v[mask])-.5)/mask.sum())
    corr=positive_definite(pd.DataFrame(gaussian).corr().to_numpy(),.01)
    corr=corr/np.sqrt(np.outer(np.diag(corr),np.diag(corr)))
    margins=[np.sort(raw[c].dropna().to_numpy()) for c in FEATURES]
    records=[]
    for repeat in range(100):
        Z=rng.multivariate_normal(np.zeros(len(FEATURES)),corr,n);U=norm.cdf(Z)
        Y=np.column_stack([np.quantile(margins[j],U[:,j],method='nearest') for j in range(len(FEATURES))])
        mask=raw.isna().to_numpy()[rng.integers(len(raw),size=n)]
        Y[mask]=np.nan
        sil,k,dip=screen(pd.DataFrame(Y,columns=FEATURES))
        records.append(dict(repeat=repeat,maximum_silhouette=sil,selected_k=k,dip=dip))
        if repeat%10==0:log(f'Continuous copula reference {repeat}/100')
    table=pd.DataFrame(records);table.to_csv(OUT/'continuous_null_simulations.csv',index=False)
    result=dict(n=n,B=100,observed_maximum_silhouette=observed[0],observed_best_k=observed[1],observed_dip=observed[2],
        silhouette_reference_p=(1+int((table.maximum_silhouette>=observed[0]).sum()))/101,
        dip_reference_p=(1+int((table.dip>=observed[2]).sum()))/101,
        null='Single Gaussian copula with empirical discrete margins and resampled joint missing masks; unconditional mask resampling does not model MAR/MNAR dependence',
        scope='Descriptive fitted-reference calibration of k-means k=2..8 on 1000 patients; not a globally calibrated test across all candidate methods')
    # Positive control: known separated groups, identical full search.
    Y=np.r_[rng.normal(-3,.5,(500,14)),rng.normal(3,.5,(500,14))]
    Y[:,[FEATURES.index('ATMTA')]]*=-1
    score=screen(pd.DataFrame(Y,columns=FEATURES));result['positive_control_maximum_silhouette']=score[0];result['positive_control_selected_k']=score[1]
    save_json('calibration_summary.json',result)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stage',required=True);parser.add_argument('--family')
    parser.add_argument('--resume',action='store_true',help='Resume an interrupted robust grid only if inputs and configuration are unchanged')
    args=parser.parse_args()
    with threadpool_limits(1):
        if args.stage=='robust':robust(args.family,args.resume)
        elif args.stage=='trajectory':
            from .trajectory import run
            run(cache(),OUT)
        elif args.stage=='report':
            from .research_report import run
            run(ROOT,OUT)
        elif args.stage=='sensitivity':
            from .sensitivity import run
            run(cache(),ROOT,OUT)
        elif args.stage=='aggregate':
            from .ensemble_comparison import run
            run(cache(),OUT)
        elif args.stage=='scaling':
            from .scaling_analysis import run
            run(cache(),OUT)
        else:globals()[args.stage]()

if __name__=='__main__':main()
