# Data-Driven Cognitive Phenotyping in Acquired Brain Injury

MSc Thesis — Fundamental Principles of Data Science, Universitat de Barcelona

**Author:** Zoltan Kunos
**Supervisor:** Alejandro García-Rudolph

## Overview

This project investigates whether unsupervised clustering of neuropsychological assessment data can identify discrete, stable cognitive phenotypes in patients with acquired brain injury (ABI), while assessing the robustness of these phenotypes to different missing-data imputation strategies.

The analysis pipeline processes 22,075 assessments from 8,739 patients across 15 neuropsychological variables spanning 6 cognitive domains, applies 10 imputation methods from 5 taxonomic categories, and tests 4 formal hypotheses.

## Project Structure

```
├── notebooks/           # 16 Jupyter notebooks (0–13, 14, 14b), sequential pipeline; H1 stability is NB6
├── data/                # Raw input files and imputed CSV outputs
├── results/             # Generated outputs (pickle, CSV, JSON)
├── report template/     # LaTeX thesis (main.tex, 7 chapters, references.bib)
├── dashboard/           # Streamlit interactive dashboard (CogDash)
│   ├── Home.py
│   ├── pages/           # 9 dashboard modules (incl. Robustness)
│   ├── components/      # Charts, filters, classifier, styles
│   ├── data/            # Data loader
│   ├── Dockerfile
│   └── requirements.txt
└── papers/              # Reference papers (PDF)
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
| 12 | Cross-Validation Stability |
| 13 | Sensitivity Analysis |
| 14 | Backlog Additions — Bootstrap CIs (A-3), Holm correction (A-2), Rubin pooling (A-4), Listwise baseline (A-5), Outcome validation (D-1) |
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

- **H1**: Discrete cognitive profiles exist — *Supported* (8/10 imputation methods clear pre-registered silhouette/noise thresholds; per-cluster MICE Hennig Jaccard 0.631 / 0.632)
- **H2**: Imputation robustness — *Supported* (mean ARI = 0.684, median 0.716)
- **H3**: Clinical unit association — *Supported* (chi2 = 634.65, CMH p = 2.21e-14)
- **H4**: Domain-level superiority — *Supported* (silhouette 0.405 vs 0.087)

## Robustness Suite (NB14 / NB14b)

Five reviewer-facing checks that supplement the headline H1–H4 results:

| Item | Method | Output |
|------|--------|--------|
| A-3 | Bootstrap 95% CIs (B=500) on H1–H4 metrics | `Backlog_Bootstrap_CIs.csv` |
| A-2 | Holm-Bonferroni + BH correction over the 45 H2 ARI pairs (parametric one-sided p-values, B=1000) | `Backlog_H2_Holm.csv` |
| A-4 | Rubin's-rules pooling across M=5 MICE imputations | `Backlog_Rubin_Pooled.csv` |
| A-5 | Complete-case (listwise) baseline + ARI/NMI vs the imputed labels | `Backlog_Listwise_Comparison.csv` |
| D-1 | TSI by phenotype (Mann–Whitney U) + within-patient phenotype stability | `Backlog_TSI_Phenotype.csv`, `Backlog_Within_Patient_Transitions.csv` |

A consolidated `results/backlog_results.pkl` powers the dashboard's Robustness page (`dashboard/pages/9_Robustness.py`) and is referenced from §4.12 of the report.

## Dashboard

Run CogDash locally after executing notebooks 0–10:

```bash
cd dashboard
pip install -r requirements.txt
streamlit run Home.py
```

Or via Docker:

```bash
cd dashboard
docker build -t cogdash .
docker run -p 8501:8501 \
  -v $(pwd)/../results:/app/../results:ro \
  -v $(pwd)/../data:/app/../data:ro \
  cogdash
```

Access at `http://localhost:8501`.

## Requirements

- Python 3.10+
- Key packages: pandas, numpy, scikit-learn, umap-learn, hdbscan, matplotlib, seaborn, plotly, streamlit, torch, statsmodels, openpyxl

## Report

The LaTeX thesis is in `report template/`. Compile with:

```bash
cd "report template"
pdflatex main.tex && biber main && pdflatex main.tex && pdflatex main.tex
```

## License

This project was developed as part of the MSc in Fundamental Principles of Data Science at the Universitat de Barcelona.
