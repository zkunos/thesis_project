# Data-Driven Cognitive Phenotyping in Acquired Brain Injury

MSc Thesis — Fundamental Principles of Data Science, Universitat de Barcelona

**Author:** Zoltan Kunos
**Supervisor:** Alejandro García-Rudolph

## Overview

This project investigates whether unsupervised clustering of neuropsychological assessment data can identify stable cognitive structure in acquired brain injury (ABI), while assessing sensitivity to different missing-data imputation strategies. The principal result is a broad cognitive-severity gradient rather than sharply discrete phenotypes. The selected UMAP+HDBSCAN solution divides this gradient into three interpretable severity bands.

The source extract contains 22,075 assessments from 8,739 patients. Following Tier-1 filtering, the analysis retains 17,406 assessments from 7,285 patients, using 14 neuropsychological variables across 6 cognitive domains. The pipeline compares 10 imputation methods and evaluates 4 pre-specified hypotheses.

The primary unit of analysis is the assessment. Repeated follow-up assessments are retained as separate rows in most clustering and bootstrap analyses rather than grouped within patients. Consequently, within-patient dependence may inflate apparent stability and narrow assessment-level uncertainty intervals. The H3 multinomial sensitivity analysis is patient-grouped.

The executed [2026 clustering extension](report/research/clustering_results_2026.md) adds patient-level discovery and validation, incomplete-data mixtures, independently refitted imputation ensembles, and longitudinal models. It finds reproducible partitions but substantial sensitivity to scaling and test availability. The historical results below remain separate from this extension.

## Project Structure

```
├── notebooks/           # Historical pipeline 0-14b and new research entry points 15-17
├── analysis/            # Shared preprocessing, clustering experiments, tests and reporting
├── dashboard/           # CogDash application, saved-model inference, and functional tests
├── data/                # Input data and imputed CSV outputs
├── results/             # Generated tables, assignments, and serialized results
├── report/              # LaTeX thesis, figures, references, and final PDF
├── presentation/        # Defence deck, PDF export, and CogDash manual
└── outputs/             # Generated presentation artifacts
```

## CogDash

The local Streamlit dashboard presents the saved assessment-level findings alongside the patient-level clustering results. It includes independent-imputation repeatability, model comparisons, scaling sensitivity, trajectories, and exploratory assignment with the saved discovery-fitted model.

From the repository root, run `./dashboard/run.ps1`, then open [CogDash locally](http://127.0.0.1:8501). See [dashboard setup](dashboard/README.md) for dependencies and required local results. The updated [user manual](presentation/cogdash_manual.pdf) includes fresh screenshots of the recreated interface. Research group assignments have no established diagnostic or treatment-planning validity.

## Notebook Execution Order

```
NB0 → NB1 + NB2 (parallel) → NB3 → NB4 → NB5 → NB6,7,8,9 (parallel) → NB10 → NB11,12,13 (parallel) → NB14 → NB14b
```

| Notebook | Description |
|----------|-------------|
| 0 | EDA and Missingness Analysis |
| 1 | Missingness Strategy (8 conventional imputation methods) |
| 2 | Deep Learning Imputation (DAE, VAE) |
| 3 | Clustering Analysis (K-Means, GMM baselines) |
| 4 | Paper Clustering Comparison |
| 5 | Improved Clustering Infrastructure (UMAP + HDBSCAN sweep, shared pipeline) |
| 6 | H1 — Per-method bootstrap stability + per-cluster Hennig Jaccard |
| 7 | H2 — Imputation Robustness |
| 8 | H3 — Clinical Unit Association |
| 9 | H4 — Domain vs Variable Level |
| 10 | Cluster Clinical Naming |
| 11 | Feature Importance Analysis |
| 12 | Seed and Resampling Stability |
| 13 | Sensitivity Analysis |
| 14 | Additional Robustness Checks — assessment bootstrap (A-3), Holm correction (A-2), across-imputation sensitivity (A-4), listwise baseline (A-5), outcome-adjacent validation (D-1) |
| 14b | Fix A-2 — replaces empirical bootstrap p-values with parametric one-sided p-values, regenerates `Backlog_H2_Holm.csv` |
| 15 | Patient-level original-space benchmarks, incomplete-data mixtures and sensitivity checks |
| 16 | Independent imputation ensembles, consensus and scaling sensitivity |
| 17 | Patient trajectory models and consolidated research results |

NB15 → NB16 → NB17 form a separate extension. Use the [research runner and setup instructions](analysis/README.md) to reproduce it. NB5 and NB14 now share direction-aligned, standardized domain construction; their stale cell outputs were cleared. Historical saved NB14 results predate this correction and require rerunning before replacement in the thesis.

## Imputation Methods

| Category | Methods |
|----------|---------|
| Conventional Statistical | Mean, EM, MICE |
| Machine Learning | KNN, MissForest |
| Hybrid | Predictive Mean Matching |
| Matrix Completion | SoftImpute, NMF |
| Deep Learning | Denoising Autoencoder, Variational Autoencoder |

## Hypotheses

- **H1: Stability and discreteness** — *Partially supported*. All 10 methods met the pre-specified silhouette and noise thresholds, but core Jaccard values were moderate (overall 0.509-0.630), recovered cluster count varied from 3 to 5, and original six-domain-space silhouette was only 0.079. Stable severity bands were recovered; discreteness was not established.
- **H2: Robustness across imputation techniques** — *Supported within a fixed-reference design*. A StandardScaler, UMAP model, and k-means partition (`k=3`) were fitted on MICE and applied unchanged to the other imputations. Mean pairwise ARI was 0.710 and median ARI was 0.739. This tests assignment robustness under a fixed structure, not whether independently refitted UMAP+HDBSCAN pipelines recover identical clusters.
- **H3: Clinical-unit association** — *Supported as an association hypothesis*. The association was statistically significant (`chi2=911.3`, Cramer's `V=0.162`) but small. Patient-grouped multinomial validation found no clear added out-of-sample predictive value from tier beyond the broad diagnostic grouping.
- **H4: Domain-level versus variable-level features** — *Supported primarily through conditioning and interpretability*. Silhouette changed only marginally (0.481 vs. 0.473), while mean VIF decreased from 2.77 to 1.88 and condition number from 61.7 to 11.8. The main benefit is reduced redundancy and improved interpretability, not stronger clustering.

## Robustness Suite (NB14 / NB14b)

Five reviewer-facing checks that supplement the headline H1–H4 results:

| Item | Method | Output |
|------|--------|--------|
| A-3 | Assessment-level bootstrap intervals on H1-H4 metrics; repeated assessments are not grouped by patient | `Backlog_Bootstrap_CIs.csv` |
| A-2 | Holm-Bonferroni + BH correction over the 45 H2 ARI pairs (parametric one-sided p-values, B=1000) | `Backlog_H2_Holm.csv` |
| A-4 | Across-imputation sensitivity summaries from 5 independent MICE runs | `Backlog_Rubin_Pooled.csv` |
| A-5 | Complete-case (listwise) baseline + ARI/NMI vs the imputed labels | `Backlog_Listwise_Comparison.csv` |
| D-1 | TSI by phenotype (Mann–Whitney U) + within-patient phenotype stability | `Backlog_TSI_Phenotype.csv`, `Backlog_Within_Patient_Transitions.csv` |

A consolidated `results/backlog_results.pkl` stores these outputs. For A-4, the reported values are across-imputation means with descriptive intervals based on between-imputation variance only. Because within-imputation variances were not estimated and the statistics are nonlinear, these intervals are not treated as Rubin-rule confidence intervals.

The Gaussian-mixture baseline tested `k=2` through `k=6`. BIC decreased through `k=6`, showing that no optimum was identified within the tested range. This result does not by itself prove a continuum or exclude solutions with more components.

## Report

```bash
cd report
pdflatex -interaction=nonstopmode -halt-on-error main_short.tex
bibtex main_short
pdflatex -interaction=nonstopmode -halt-on-error main_short.tex
pdflatex -interaction=nonstopmode -halt-on-error main_short.tex
```

This sequence updates the bibliography and resolves cross-references after structural edits. The compiled thesis is available at `report/main_short.pdf`. The added vector figures can be reproduced from the saved experiment with `.venv-research/Scripts/python.exe report/research/render_thesis_figures.py` from the repository root.

## Defence Materials

The rebuilt [defence deck](presentation/defense_2026/thesis_defense.pptx) and [PDF export](presentation/defense_2026/thesis_defense.pdf) contain 17 main slides for a 15-minute presentation and 10 backup slides for examiner questions. The PowerPoint includes timed speaker notes, sources, and editable charts and tables. The main presentation covers the historical analysis, patient-level validation, scaling and missingness sensitivity, and the limits of the clinical interpretation. The earlier deck and the CogDash manual remain in `presentation/`.

## Recent Clustering Research

The [15 October 2026 research assessment](report/research/clustering_research_2026.md) evaluates seven articles published within the preceding year. The [original experiment protocol](report/research/clustering_experiment_protocol_2026.md), [executed results and limitations](report/research/clustering_results_2026.md), and [BibTeX references](report/research/clustering_recent_references.bib) accompany it.

The extension uses 5,828 discovery and 1,457 validation patients. Across 20 stochastic imputations, k-means selects two groups in every training-silhouette screen; fixed three-group assignments have mean pairwise validation ARI 0.935. However, switching from robust to equal-domain scaling changes three-group assignments substantially (ARI 0.243), and test availability differs between groups. These results do not establish a unique set of discrete phenotypes.

The thesis source now integrates the extension into the abstract, Chapter 3 methodology, Chapter 4 results, discussion, limitations and conclusions. The added source sections are `ClusteringExtensionMethods.tex` and `ClusteringExtensionResults.tex`, included from the existing chapters. Earlier supplementary outputs are explicitly identified as predating the preprocessing correction.

The historical eligible matrix retains rows with **at least one observed retained test**. Its 50% missingness threshold applies to variable selection. The new analysis reports a separate sensitivity restricted to at least seven observed tests. Generated research outputs are in `results/research_2026/`; eight numerical validation tests pass.

## Requirements

- Python 3.12 for the patient-level analysis and CogDash, with the pinned dependencies in `analysis/requirements-research.lock.txt` and `dashboard/requirements.txt`. Historical analyses were produced in a separate Python 3.13 environment.
- Key packages: pandas, numpy, scikit-learn, umap-learn, hdbscan, matplotlib, seaborn, plotly, streamlit, torch, statsmodels, openpyxl

## License

This project was developed as part of the MSc in Fundamental Principles of Data Science at the Universitat de Barcelona.
