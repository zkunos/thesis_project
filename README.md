# Data-Driven Cognitive Phenotyping in Acquired Brain Injury

MSc Thesis — Fundamental Principles of Data Science, Universitat de Barcelona

**Author:** Zoltan Kunos
**Supervisor:** Alejandro García-Rudolph

## Overview

This project investigates whether unsupervised clustering of neuropsychological assessment data can identify stable cognitive structure in acquired brain injury (ABI), while assessing sensitivity to different missing-data imputation strategies. The principal result is a broad cognitive-severity gradient rather than sharply discrete phenotypes. The selected UMAP+HDBSCAN solution divides this gradient into three interpretable severity bands.

The source extract contains 22,075 assessments from 8,739 patients. Following Tier-1 filtering, the analysis retains 17,406 assessments from 7,285 patients, using 14 neuropsychological variables across 6 cognitive domains. The pipeline compares 10 imputation methods and evaluates 4 pre-specified hypotheses.

The primary unit of analysis is the assessment. Repeated follow-up assessments are retained as separate rows in most clustering and bootstrap analyses rather than grouped within patients. Consequently, within-patient dependence may inflate apparent stability and narrow assessment-level uncertainty intervals. The H3 multinomial sensitivity analysis is patient-grouped.

## Project Structure

```
├── notebooks/           # Jupyter analysis pipeline (0-14b plus executed copies)
├── analysis/            # Reproducible scripts for report corrections and figures
├── data/                # Input data and imputed CSV outputs
├── results/             # Generated tables, assignments, and serialized results
├── report/              # LaTeX thesis, figures, references, and final PDF
├── presentation/        # Defence decks, transcripts, study cards, and PDFs
└── outputs/             # Generated presentation artifacts
```

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
```

Run `pdflatex` twice after structural edits to resolve cross-references. The compiled thesis is available at `report/main_short.pdf`.

## Defence Materials

The `presentation/` directory contains the professional 20-minute defence deck, transcript, study cards, and supporting PDF exports. Key files include:

- `thesis_defense_20min_professional.pptx`
- `thesis_defense_20min_transcript.pdf`
- `thesis_defense_study_cards.pdf`

## Requirements

- Python 3.10+
- Key packages: pandas, numpy, scikit-learn, umap-learn, hdbscan, matplotlib, seaborn, plotly, streamlit, torch, statsmodels, openpyxl

## License

This project was developed as part of the MSc in Fundamental Principles of Data Science at the Universitat de Barcelona.
