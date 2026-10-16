"""Create an auditable results report and static scientific figures."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import joblib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .data_contract import sha256


def markdown_table(df,columns):
    def fmt(x):
        if isinstance(x,(float,np.floating)):return '—' if not np.isfinite(x) else f'{x:.3f}'
        return str(x)
    return '\n'.join(['| '+' | '.join(columns)+' |','| '+' | '.join(['---']*len(columns))+' |']+
                     ['| '+' | '.join(fmt(value) for value in row)+' |' for row in df[columns].itertuples(index=False,name=None)])


def run(root,out):
    destination=root/'report/research';figs=destination/'figures';figs.mkdir(parents=True,exist_ok=True)
    required=['model_comparison.csv','refit_agreement.csv','ensemble_comparison.csv','cluster_count_distribution.csv',
              'scaling_sensitivity.csv','trajectory_model_comparison.csv','calibration_summary.json','missingness_sensitivity.csv',
              'incomplete_mixture_comparison_normal.csv','incomplete_mixture_comparison_t4.csv',
              'incomplete_mixture_comparison_t10.csv','incomplete_mixture_comparison_contaminated.csv']
    for name in required:
        if not (out/name).exists():raise FileNotFoundError(f'Results incomplete: {name}')
    read=lambda name:pd.read_csv(out/name)
    audit=json.loads((out/'data_audit.json').read_text());manifest=json.loads((out/'run_manifest.json').read_text())
    null=json.loads((out/'calibration_summary.json').read_text());bench=read('model_comparison.csv')
    robust=pd.concat([read(f'incomplete_mixture_comparison_{family}.csv') for family in ['normal','t4','t10','contaminated']],ignore_index=True)
    assert all(robust.groupby('family').k.nunique()>=8),'Incomplete robust model grid'
    robust.to_csv(out/'incomplete_mixture_comparison.csv',index=False)
    stability=read('refit_agreement.csv');scaling=read('scaling_sensitivity.csv');common=read('common_geometry_comparison.csv').iloc[0]
    scaleaudit=read('scaling_audit.csv');correct=read('preprocessing_correction_impact.csv');sens=read('missingness_sensitivity.csv')
    trajectory=read('trajectory_model_comparison.csv');ensemble=read('ensemble_comparison.csv');counts=read('cluster_count_distribution.csv')
    selected=bench[bench.selected_by_training]
    rb=[]
    for family,g in robust.groupby('family'):
        usable=g[g.converged & (g.train_minimum_cluster_fraction>=.02)]
        if len(usable):
            best=usable.loc[usable.bic.idxmin()]
            rb.append(dict(family=family,selected_k=int(best.k),bic=best.bic,validation_loglik=best.validation_loglik,
                validation_silhouette=best.validation_silhouette,converged_fits=int(g.converged.sum()),
                fits=len(g),lowest_bic_any_fit_k=int(g.loc[g.bic.idxmin(),'k']),
                selected_by_icl_k=int(usable.loc[usable.icl.idxmin(),'k'])))
    rb=pd.DataFrame(rb);rb.to_csv(out/'robust_selected_models.csv',index=False)
    state=joblib.load(out/'prepared.joblib');bank=joblib.load(out/'benchmarks.joblib')
    assignments=[]
    for label in selected.model:
        part=state['index'][['assessment_key','patient_key']].copy()
        part['model']=label;part['cluster']=bank['assign'][label]
        part['split']='discovery';part.iloc[state['test'],part.columns.get_loc('split')]='validation'
        assignments.append(part)
    pd.concat(assignments,ignore_index=True).to_csv(out/'selected_assignments.csv',index=False)
    incomplete_assignments=[]
    for _,row in rb.iterrows():
        model=joblib.load(out/f'incomplete_models_{row.family}.joblib')[f'{row.family}:{row.selected_k}']
        P=model.predict_proba(state['X'])
        part=state['index'][['assessment_key','patient_key']].copy()
        part['model']=f'incomplete:{row.family}:{row.selected_k}'
        part['cluster']=P.argmax(axis=1);part['maximum_probability']=P.max(axis=1)
        part['entropy']=-np.sum(P*np.log(P+1e-15),axis=1)
        part['split']='discovery';part.iloc[state['test'],part.columns.get_loc('split')]='validation'
        incomplete_assignments.append(part)
    pd.concat(incomplete_assignments,ignore_index=True).to_csv(out/'incomplete_assignments.csv',index=False)
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':160})
    colors=['#176B87','#E9803C','#668B49','#9A5A92']
    # Same partitions scored in both geometries: no cross-space winner claim.
    fig,axes=plt.subplots(1,2,figsize=(11,4.3))
    x=np.arange(6);axes[0].bar(x,scaleaudit.robust_scaled_variance,color=colors[0],label='Robust-scaled variance')
    axes[0].axhline(1,color=colors[1],ls='--',label='Equal-domain variance')
    axes[0].set_xticks(x,scaleaudit.domain,rotation=35,ha='right');axes[0].set_ylabel('Training variance');axes[0].legend(fontsize=8)
    vals=np.array([[common.robust_k3_silhouette_robust,common.robust_k3_silhouette_equal_domain],
                   [common.equal_k3_silhouette_robust,common.equal_k3_silhouette_equal_domain]])
    xx=np.arange(2)
    axes[1].bar(xx-.18,vals[:,0],.36,label='Scored in robust space',color=colors[0]);axes[1].bar(xx+.18,vals[:,1],.36,label='Scored in equal-domain space',color=colors[1])
    axes[1].set_xticks(xx,['Robust k=3 labels','Equal-domain k=3 labels']);axes[1].set_ylabel('Validation silhouette');axes[1].legend(fontsize=8)
    fig.suptitle('Scaling changes both geometry and the recovered groups');fig.tight_layout();fig.savefig(figs/'scaling_sensitivity.png');plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,4))
    imp=stability[stability.source=='imputation_draw']
    x=np.arange(len(imp));ax.bar(x,imp.mean_ari,color=[colors[0] if m=='kmeans' else colors[1] for m in imp.method])
    ax.set_xticks(x,[f'{m}, k={k}' for m,k in zip(imp.method,imp.k)]);ax.set_ylim(0,1.05);ax.set_ylabel('Mean pairwise validation ARI')
    for i,v in enumerate(imp.mean_ari):ax.text(i,v+.015,f'{v:.3f}',ha='center',fontsize=9)
    ax.set_title('Independent clustering fits across 20 stochastic imputations');fig.tight_layout();fig.savefig(figs/'imputation_stability.png');plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(11,4.2))
    for color,(family,g) in zip(colors,robust.groupby('family')):
        g=g.sort_values('k');axes[0].plot(g.k,g.bic,marker='o',label=family,color=color)
        failed=g[~g.converged];axes[0].scatter(failed.k,failed.bic,marker='x',s=80,color='black')
        axes[1].plot(g.k,g.validation_loglik,marker='o',label=family,color=color)
    axes[0].set(xlabel='Mixture components',ylabel='Training BIC (lower is better)')
    axes[1].set(xlabel='Mixture components',ylabel='Mean observed-data validation log likelihood')
    axes[0].legend(fontsize=8);axes[1].legend(fontsize=8)
    fig.suptitle('Incomplete-data mixtures: fit quality is not proof of discrete phenotypes\nBlack crosses indicate fits that did not meet the convergence tolerance',fontsize=11)
    fig.tight_layout();fig.savefig(figs/'incomplete_mixtures.png');plt.close(fig)
    scprofiles=read('scaling_profiles.csv')
    fig,axes=plt.subplots(1,2,figsize=(11,4.1),sharey=True)
    # Original robust k=3 is explicitly a fixed comparison, not selected by silhouette.
    from sklearn.cluster import KMeans
    labs=KMeans(3,n_init=20,random_state=20261015).fit(state['D'][state['train']]).predict(state['D'][state['test']])
    domains=list(scaleaudit.domain)
    for c in range(3):
        mask=labs==c;axes[0].plot(domains,state['domains'][state['test']][mask].mean(axis=0),marker='o',label=f'Group {c+1} (n={mask.sum()})')
    for c,g in scprofiles[scprofiles.model=='equal_domain:kmeans:3'].groupby('cluster'):
        g=g.set_index('domain').loc[domains];axes[1].plot(domains,g['mean'],marker='o',label=f'Group {c+1} (n={g.n.iloc[0]})')
    for ax,title in zip(axes,['Robust-scaled k-means, k=3','Equal-domain k-means, k=3']):
        ax.set_title(title);ax.tick_params(axis='x',rotation=35);ax.legend(fontsize=8);ax.axhline(0,color='grey',lw=.5)
        for label in ax.get_xticklabels():label.set_ha('right')
    axes[0].set_ylabel('Mean domain composite (aligned test z scores)')
    fig.tight_layout();fig.savefig(figs/'validation_profiles.png');plt.close(fig)
    hypotheses=(
        '**Main conclusion:** reproducible partitions exist, but their interpretation is strongly dependent on scaling, imputation and model family. '
        'The new analysis does not establish a unique set of discrete cognitive phenotypes. '
        'It adds evidence for stable score groupings and identifies measurement effects that must be addressed before stronger clinical claims.\n\n')
    text='# Implemented clustering extension: results\n\nAnalysis date: 15 October 2026.\n\n'+hypotheses
    text+=f"Verified {audit['eligible_rows']:,} assessments from {audit['eligible_patients']:,} patients. The new cross-sectional experiment uses the earliest eligible assessment per patient, with **{manifest['train_patients']:,} discovery and {manifest['validation_patients']:,} validation patients**. The saved eligible matrix exactly matches the current spreadsheet. Source hashes and row mappings are recorded locally. No raw data were uploaded.\n\n"
    text+=f"The audit recovered an eligibility discrepancy: the saved matrix and NB0 retain rows with at least one observed retained test, not a maximum 50% missingness rule. There are {audit['at_least_half_observed']:,} assessments and {audit['index_at_least_half_observed']:,} index patients with at least seven observed tests. The primary experiment preserves the historical eligible cohort and assesses that stricter rule separately.\n\n"
    text+='**Implemented changes and checks**\n\n'
    text+='Shared clipping, test-direction alignment, variable standardization and domain aggregation now replace the duplicated NB5/NB14 logic. New preprocessing is fitted on discovery patients only. NB15–NB17 call reproducible Python stages. Historical result files remain untouched; new outputs are under `results/research_2026/`.\n\n'
    text+=f"The corrected aggregation materially changes the old descriptive comparison: three-group k-means ARI between old and corrected preprocessing is **{correct.iloc[0].ari_naive_vs_corrected:.3f}** over all assessments and **{correct.iloc[1].ari_naive_vs_corrected:.3f}** over complete cases. Attention composites correlate **{correct.iloc[0].attention_score_correlation:.3f}**, consistent with the importance of reversing the timed test. These are controlled aggregation checks, not a rerun of every legacy H1–H4 statistic.\n\n"
    text+='The code implements and tests observed-data Gaussian, fixed-df t (4 and 10), and fixed-contamination (90% core, 10% tenfold covariance) mixtures. Missing coordinates are integrated out. It also implements sampled PAM, independently refitted imputation ensembles, and a linear trajectory mixture with integrated patient random effects. These are native implementations, not exact reproductions of the published R packages.\n\n'
    text+='**Original-space comparisons**\n\n'+markdown_table(selected,['model','train_silhouette','validation_silhouette','validation_coverage','train_minimum_cluster_fraction'])+'\n\n'
    text+='The table selects partition/density models by discovery silhouette and GMMs by discovery BIC among converged solutions with at least 2% in each cluster. Silhouettes are measured in the indicated feature representation, not the UMAP embedding. Noise is excluded from silhouette and coverage is reported separately. Different representations define different geometries; their silhouettes are not a common performance scale.\n\n'
    text+='Direct HDBSCAN assigned every patient to noise at both tested minimum cluster sizes (100 and 300, min_samples=20). UMAP+HDBSCAN recovered groups, but changing neighborhood size from 15 to 50 changed the recovered count and reduced separation in measured domain space. This is evidence of parameter and representation sensitivity, not a comprehensive rejection of density clustering.\n\n'
    text+='**Scaling is a major source of sensitivity**\n\n'
    text+=f"Robust scaling gives language and orientation variances {scaleaudit.loc[scaleaudit.domain=='Language','robust_scaled_variance'].iloc[0]:.2f} and {scaleaudit.iloc[0].robust_scaled_variance:.2f}, compared with {scaleaudit.loc[scaleaudit.domain=='Memory','robust_scaled_variance'].iloc[0]:.2f} for memory. Tight central score ranges amplify the tails of ceiling-heavy tests. The robust-space first component explains {manifest['pc_explained_variance'][0]:.1%}, but is dominated by language/orientation; it should not automatically be equated with a balanced general-cognition factor. Equal-domain scaling yields PC1 variance {common.equal_domain_pc1_variance:.1%}.\n\n"
    text+=f"At k=3, robust and equal-domain assignments agree at only **ARI {common.ari_robust_vs_equal:.3f}**. The robust labels have validation silhouette {common.robust_k3_silhouette_robust:.3f} in their own geometry and {common.robust_k3_silhouette_equal_domain:.3f} in equal-domain geometry. Equal-domain labels have corresponding values {common.equal_k3_silhouette_robust:.3f} and {common.equal_k3_silhouette_equal_domain:.3f}. The geometry sensitivity was added after inspecting training-set variances and is explicitly exploratory. Neither scaling is established as clinically correct.\n\n"
    text+='![Scaling sensitivity](figures/scaling_sensitivity.png)\n\n![Validation profiles](figures/validation_profiles.png)\n\nGroup numbers in the profile figure are local to each model; matching numbers/colors across panels do not identify the same patients.\n\n'
    text+='**Refitting and imputation uncertainty**\n\n'+markdown_table(stability,['source','method','k','n_repeats','mean_ari','ari_p05','ari_p95'])+'\n\n'
    text+='These ARIs compare labels for the same held-out patients after independent discovery fits. The 5th–95th percentiles describe pairwise agreement variation; they are not confidence intervals, because pairs share fitted partitions. Patient subsampling refits preprocessing, imputation and k-means; initialization checks vary clustering seeds with the input fixed. Stochastic imputations use a bounded Bayesian chained-equations model, so their stability is conditional on that model.\n\n'
    text+='The new cohort, representation and validation design differ from the historical assessment-level analysis. A numerically higher ARI is not evidence that the new model outperforms the original one. `selected_assignments.csv` links the selected reference labels to verified assessment and patient keys.\n\n'
    cluster_stability=read('per_cluster_stability.csv')
    cluster_stability=cluster_stability[cluster_stability.source=='patient_subsample'].groupby('cluster').jaccard.agg(['mean','min','max']).reset_index()
    text+='Per-cluster held-out Jaccard across patient subsamples (fixed three-group k-means):\n\n'+markdown_table(cluster_stability,['cluster','mean','min','max'])+'\n\n'
    text+='![Imputation stability](figures/imputation_stability.png)\n\n'
    text+='Equal-domain k-means imputation stability:\n\n'+markdown_table(read('equal_domain_imputation_stability.csv'),['k','mean_ari','ari_p05','ari_p95'])+'\n\n'
    text+='Other sensitivity comparisons (fixed k=3):\n\n'+markdown_table(sens,['experiment','n_train','n_validation','ari_vs_reference','validation_silhouette'])+'\n\n'
    text+='These sensitivity silhouettes use the fixed reference domain geometry, including for the KNN and no-clipping assignments. Independent validation discovery fits clusters on validation patients under the frozen training transform; that row is an agreement diagnostic, not another held-out prediction score.\n\n'
    missingness=read('cluster_missingness_association.csv')
    top_missingness=missingness.groupby('variable').agg(cramers_v=('cramers_v','first'),
        minimum_missing_fraction=('missing_fraction','min'),maximum_missing_fraction=('missing_fraction','max'))
    top_missingness=top_missingness.sort_values('cramers_v',ascending=False).head(5).reset_index()
    text+='Test availability is associated with fixed three-group assignments on validation patients:\n\n'+markdown_table(top_missingness,list(top_missingness.columns))+'\n\n'
    text+='These are descriptive associations, not evidence that missingness causes the groups. They show that administration patterns and impairment remain entangled. The smallest robust-space group has particularly high missingness in memory and executive tests. Stability under the same imputation assumptions does not remove this concern.\n\n'
    text+=f"Across the 20 imputation draws, the k-means training-silhouette screen selected counts {counts.k_selected.value_counts().sort_index().to_dict()}. This compares two through eight clusters and does not test the existence of groups against a one-population null.\n\n"
    text+='Average-linkage and greedy mean-NMI consensus gave similar agreement for k-means k=2 and k=3. Generic NMF aggregation was unreliable here: the requested two-group k-means ensemble collapsed to one assigned group and hit the iteration limit; its three-group version produced only two assigned groups. Full results are saved in `ensemble_comparison.csv`. Consensus was calculated over held-out assignment vectors to summarize agreement; it is not an independently validated predictive model. A one-group silhouette is undefined.\n\n'
    text+='**Incomplete-data models**\n\n'+markdown_table(rb,list(rb.columns))+'\n\n'
    text+=f"The grid contains {len(robust)} fits, of which {int(robust.converged.sum())} meet the requested numerical convergence criterion. Selected models must converge and assign at least 2% of discovery patients to every component. A dispersion-matrix eigenvalue floor of 0.02 (the scale matrix for t models) regularizes singular fits to bounded/discrete scores; BIC is an exploratory comparison of these approximations, not a test of biological classes. More components can fit skewness, ceiling masses and other distributional features. A best fit at the search boundary does not establish an optimum. These likelihoods may be compared within this 14-test data representation, not with GMM likelihoods in six-domain space.\n\n"
    text+='The t family with four degrees of freedom has the best BIC and validation likelihood among the selected restricted families. Both t families still select eight components, the upper search boundary. Their low six-domain silhouettes and unresolved component count argue for treating them as density models with uncertain memberships, not adopting eight clinical phenotypes. Gaussian and contaminated-normal selection also differs, and ICL selects six rather than seven components for the contaminated model.\n\n'
    text+='The reported silhouette for these models evaluates their assignments in the completed six-domain robust-scaled representation; their likelihood fits integrate missing values directly in the 14-test representation. Selected assignments and model-conditional membership probabilities are saved with verified keys in `incomplete_assignments.csv`. Probabilities do not capture uncertainty about the model family, component count or missingness mechanism.\n\n'
    text+='![Incomplete-data mixture results](figures/incomplete_mixtures.png)\n\n'
    text+='**Continuous-reference check**\n\n'
    text+=f"A matched-size 1,000-patient screen compared k-means k=2–8 with 100 single-Gaussian-copula reference datasets, preserving empirical discrete margins and resampling joint missingness masks. The observed maximum silhouette was {null['observed_maximum_silhouette']:.3f}; its fitted-reference tail fraction was {null['silhouette_reference_p']:.4f}. The PC1 dip-statistic tail fraction was {null['dip_reference_p']:.4f}. The positive control recovered {null['positive_control_selected_k']} groups with silhouette {null['positive_control_maximum_silhouette']:.3f}.\n\n"
    text+='The criteria disagree. The silhouette result suggests structure beyond this particular fitted reference, while the dip statistic does not show excess multimodality relative to it. This is a descriptive calibration: the null is estimated from these data, missingness is resampled independently of simulated values, and the screen does not reproduce selection across every model family. It does not establish an omnibus p-value for clinical phenotypes or exclude other continuous explanations.\n\n'
    text+='**Longitudinal analysis**\n\n'+markdown_table(trajectory,['k','n_train','n_validation','converged','bic','validation_loglik','minimum_train_class_fraction'])+'\n\n'
    admissible=trajectory[trajectory.converged & (trajectory.minimum_train_class_fraction>=.05)]
    trajectory_k=int(admissible.loc[admissible.bic.idxmin(),'k'])
    text+=f"The included cohort contains {int(trajectory.iloc[0].n_train+trajectory.iloc[0].n_validation):,} patients. The convergence and 5% minimum-class rule selects **{trajectory_k} trajectory class**. The two-, three- and four-class fits improve likelihood but each introduces a class below the size threshold. This does not establish that recovery is homogeneous; it leaves nonlinear continuous variation and small genuine subgroups unresolved.\n\n"
    text+='The trajectory experiment requires at least three sufficiently observed visits, a 0.25–5 year observed span, distinct times and a constant recorded injury age. It models the cognitive score over elapsed time from the first eligible assessment, integrating random intercept/slope uncertainty. This is a selected follow-up cohort and an exploratory course model, not a causal recovery model. More complex solutions improve likelihood but require inspecting small classes and departure from a linear Gaussian trajectory. The supplied selection rule requires at least 5% expected membership in every class. Repeated cognition is not an independent functional endpoint.\n\n'
    text+='**Implications for the thesis**\n\n'
    text+='Retain the interpretation of broad cognitive score/severity structure, while acknowledging that the dominant direction is sensitive to domain weighting. Qualify categorical phenotype claims. Report both robust and equal-domain geometries, since they produce different groups. Treat the independent-imputation result as an extension of H2, distinct from the earlier fixed-reference ARI. Recalculate legacy sensitivity statistics with the corrected preprocessing before replacing their thesis tables. Do not translate improved fit or stable assignments into treatment recommendations without external outcomes or cohort replication.\n\n'
    text+='**Remaining limits and deviations from the proposed protocol**\n\n'
    text+='The supplied data lack a verified episode-level assessment identifier and independent rehabilitation outcome. Variable selection was inherited from the historical full cohort. Imputation assumes an ignorable mechanism; bounded posterior draws do not solve MNAR. Some iterative imputers hit their iteration limit; extending deterministic imputation to 50 iterations converged after 37 and left the three-group labels unchanged. The skew-t and the published contaminated multivariate longitudinal model were not ported; the implemented restricted families make their assumptions explicit. PCA/dip diagnostics and fitted-reference simulations were run; a calibrated Silverman test was not implemented. The null simulation is narrower than the proposed full-procedure calibration and the positive control is an easy separated-group check, not a power study. The code uses native ensemble methods, not an exact reproduction of the paper authors\' software. No superiority claim is made for an unimplemented method.\n\n'
    text+='The recent evidence motivating this work is documented in the [research review](clustering_research_2026.md): [incomplete-data mixtures](https://doi.org/10.18637/jss.v115.i03), [multiple-imputation ensembles](https://doi.org/10.1186/s12874-026-02869-2), [clusterability](https://doi.org/10.5334/jors.389), and [longitudinal comparisons](https://doi.org/10.1186/s12874-026-02882-5). All cited articles are within the requested one-year publication window.\n\n'
    text+='Reproduce with `analysis/run_research.ps1` using the project research environment. Source versions, dependency versions, input hashes and output hashes accompany the results. Numerical unit tests cover reference likelihoods, complete-data agreement, missing-data recovery, EM monotonicity, preprocessing direction, medoids, integrated trajectory likelihood and ensemble objective calculations.\n'
    (destination/'clustering_results_2026.md').write_text(text,encoding='utf-8')
    hashes={str(p.relative_to(root)):sha256(p) for p in sorted((root/'analysis').glob('*.py'))}
    hashes.update({str(p.relative_to(root)):sha256(p) for p in (root/'analysis').glob('requirements-research*.txt')})
    hashes.update({str(p.relative_to(root)):sha256(p) for p in [root/'analysis/run_research.ps1',destination/'clustering_results_2026.md',*figs.glob('*.png')]})
    hashes.update({str(p.relative_to(root)):sha256(p) for p in sorted(out.glob('*.csv'))})
    (out/'artifact_hashes.json').write_text(json.dumps(hashes,indent=2),encoding='utf-8')
    print('Wrote report/research/clustering_results_2026.md and four figures',flush=True)
