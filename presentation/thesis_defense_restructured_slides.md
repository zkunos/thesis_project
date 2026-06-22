---
marp: true
theme: default
paginate: true
size: 16:9
title: Data-Driven Cognitive Phenotyping in Acquired Brain Injury
author: Zoltan Kunos
---

<!-- _paginate: false -->

# Data-Driven Cognitive Phenotyping in Acquired Brain Injury

## Do routine neuropsychological data reveal cognitive subtypes or a severity gradient?

**Zoltan Kunos**  
MSc Fundamental Principles of Data Science  
Universitat de Barcelona

Supervisor: Dr. Alejandro Garcia-Rudolph

---

# Roadmap

1. Clinical problem and research gap
2. Cohort, missingness, and methods
3. Four hypothesis tests
4. Interpretation and practical utility
5. Limitations and conclusions

---

# Clinical Problem

## The same diagnosis can conceal different rehabilitation needs

- ABI can affect attention, memory, language, executive function, orientation, and visuospatial cognition.
- Cognitive impairment does not follow the same pattern in every patient.
- Diagnosis and injury severity provide useful categories, but they do not fully describe cognitive heterogeneity.
- Incomplete assessments are common, particularly among patients with greater impairment.

**Research question:** Can data-driven clustering recover clinically meaningful cognitive organization when missing data are handled explicitly?

---

# Research Gap and Contribution

## Existing cognitive-phenotyping studies have important limitations

| Common limitation | This dissertation |
|---|---|
| Samples often below 200 participants | 17,406 assessments from 7,285 patients |
| Complete-case analysis | Ten imputation strategies |
| Limited algorithmic sensitivity testing | Hyperparameter, seed, and missingness sensitivity analyses |
| Predetermined number of clusters | Density-based clustering with HDBSCAN |
| Limited clinical validation | Association with clinical unit assignment |

---

# Pre-Registered Hypotheses

| Hypothesis | Question | Criterion |
|---|---|---|
| **H1** | Are stable clusters recoverable? | Silhouette > 0.40, noise < 30%, at least two clusters |
| **H2** | Are assignments robust to imputation? | Mean pairwise ARI > 0.50 under fixed reference |
| **H3** | Are tiers clinically relevant? | Clinical-unit association; Cramer's V > 0.10 |
| **H4** | Does domain aggregation help? | Better separation and numerical conditioning |

---

# Cohort and Missingness

## Large-scale routine clinical data

| Measure | Value |
|---|---:|
| Assessments | **17,406** |
| Patients | **7,285** |
| Neuropsychological variables | **14** |
| Cognitive domains | **6** |
| Complete rows | **53.1%** |

Complete-case analysis would discard approximately **46.9%** of assessments.

---

# Why Imputation Is Necessary

## Missingness reflects the clinical testing process

- Fatigue or reduced motivation
- Cognitive overload or task aversion
- Disorientation or motor limitations
- Limited tolerance for lengthy assessments
- Clinician selection of a more appropriate test

Removing incomplete rows may disproportionately exclude patients with greater cognitive impairment.

**Missingness must be managed and tested, not hidden.**

---

# Analysis Pipeline

## One workflow, ten imputation strategies

**Impute**  
10 strategies

&darr;

**Scale and orient scores**  
Higher values indicate better performance

&darr;

**Aggregate**  
14 variables into 6 cognitive domains

&darr;

**UMAP embedding**

&darr;

**HDBSCAN clustering and sensitivity analysis**

---

# Why UMAP and HDBSCAN?

## UMAP

- Represents nonlinear neighbourhood structure.
- Balances local and broader geometric information.
- Reduces dimensionality before density-based clustering.

## HDBSCAN

- Does not require a predefined number of clusters.
- Identifies persistent dense regions across density levels.
- Can label uncertain observations as noise rather than forcing assignment.

**Caveat:** separation measured in UMAP space may be optimistic and must be supported by sensitivity analyses.

---

# H1: Three Severity Tiers

| Tier | Assessments | Interpretation |
|---|---:|---|
| **Above-Average** | **6,725** | Above the cohort mean across domains |
| **Near-Normal** | **6,328** | Close to the cohort average |
| **Global Impairment** | **4,353** | Below the cohort mean across domains |

- All ten imputation methods cleared the pre-registered thresholds.
- MICE reference silhouette: approximately **0.53**.
- Recovered number of tiers: **3**.

**The numerical criteria for H1 were met, but the tiers are not interpreted as natural kinds.**

---

# Continuum Evidence

## The tiers differ mainly by level, not profile shape

- Radar profiles are approximately concentric.
- Cognitive domains move in the same direction across tiers.
- The first principal component explains nearly **56%** of variance.
- All domains load positively on the first component.

**Dominant signal:** global cognitive severity.

**Not dominant:** symptom-specific dissociation or a catalogue of qualitatively distinct subtypes.

---

# H2: Robustness to Imputation

## Fixed-reference comparison

- Mean pairwise ARI: **0.71**
- 95% bootstrap confidence interval: **0.70-0.72**
- **44 of 45** method pairs survived Holm correction
- More than **86%** of assessments received high-confidence consensus labels

**Scope of H2:** point assignments are robust under a fixed scaler, embedding, and partition.

H2 does not establish that independently refitted pipelines recover identical density hierarchies.

---

# Complete-Case Analysis Changes the Result

| Result | MICE reference | Complete case |
|---|---:|---:|
| Assessments retained | 100% | 53.1% |
| Tiers recovered | 3 | 2 |
| Silhouette | approximately 0.53 | approximately 0.26 |
| ARI on shared assessments | - | approximately 0.63 |

Deleting incomplete assessments does not produce a weaker version of the same analysis.

**It changes the recovered partition.**

---

# H3: Clinical Relevance

## Severity tier is associated with clinical unit assignment

- Chi-square statistic: **911**
- Statistical significance: **p < 10^-156**
- Cramer's V: **0.16**
- Pre-registered effect-size threshold: **0.10**

The association remained significant after diagnosis adjustment using the Cochran-Mantel-Haenszel test.

**Interpretation:** severity tier adds information beyond diagnosis, but it does not determine clinical placement.

---

# H4: Domain Aggregation

## Six domains improve stability without sacrificing separation

| Metric | Individual variables | Domains |
|---|---:|---:|
| Silhouette | 0.47 | **0.48** |
| Mean VIF | 2.80 | **1.90** |
| Condition number | 62 | **12** |

- Reduced feature redundancy
- Improved numerical conditioning
- Clearer clinical interpretation

---

# Interpretation

## A severity gradient, not a subtype catalogue

- Subtypes imply qualitatively different cognitive profiles.
- A gradient implies that patients differ mainly along a shared severity axis.
- The recovered tiers are practical bands extracted from that continuum.
- Domain-specific dissociations may still exist, but they are not the dominant structure in this dataset.

Poor scaling, redundant features, non-cognitive measures, or complete-case selection may create misleading subtype-like patterns.

---

# Utility and Translation

## Clinical utility

- Shared vocabulary for discussing rehabilitation intensity
- Confidence scores for borderline assignments
- Additional information alongside diagnosis and clinical judgement

## Analytical utility

- Reproducible missingness-aware pipeline
- Explicit and testable imputation decisions
- Adaptable framework for linking cognition with outcomes

## CogDash

An auditable Streamlit decision-support tool for cluster exploration, patient lookup, and new-patient classification.

---

# Limitations

1. **Single site:** external replication is required.
2. **Limited longitudinal modelling:** repeated assessments do not constitute a full recovery-trajectory model.
3. **Missing-data assumptions:** MAR is a working assumption; MNAR mechanisms cannot be excluded.
4. **No functional outcomes:** return to work, length of stay, and independence were unavailable.
5. **Embedding-based validation:** UMAP-space silhouette may overstate separation.
6. **Pipeline sensitivity:** domain aggregation and density clustering may favour a general severity axis.

---

# Conclusions

## Three contributions

1. **Empirical:** Routine post-ABI neuropsychological data contain a strong cognitive severity gradient.
2. **Methodological:** Imputation is a substantive modelling decision that can alter recovered structure.
3. **Practical:** Domain-level severity tiers provide an interpretable and numerically stable representation.

This dissertation supports an imputation-robust severity-stratification framework rather than strong claims of discrete cognitive phenotypes.

---

<!-- _paginate: false -->

# Questions and Discussion

## A clinically useful severity continuum after acquired brain injury

**Zoltan Kunos**  
Supervisor: Dr. Alejandro Garcia-Rudolph

---

<!-- _class: lead -->

# Appendix

## Backup slides for examiner questions

---

# Appendix A: Ten Imputation Strategies

1. Mean imputation
2. Median imputation
3. Predictive mean matching
4. Expectation-maximization
5. MICE
6. K-nearest neighbours
7. MissForest
8. SoftImpute
9. Non-negative matrix factorization
10. Deep generative approaches

---

# Appendix B: H2 Fixed-Reference Design

1. Fit the reference scaler using MICE-imputed data.
2. Fit one UMAP embedding using the MICE reference.
3. Define the reference partition.
4. Transform each alternative imputed dataset through the frozen pipeline.
5. Compare predicted labels using pairwise ARI.

**Tests:** robustness of point assignments to imputed values.

**Does not test:** full invariance of independently discovered structures.

---

# Appendix C: HDBSCAN Logic

- Estimates local density using core distance.
- Constructs mutual-reachability distances.
- Builds a minimum spanning tree.
- Extracts a hierarchy of density-connected components.
- Selects persistent clusters based on stability.
- Labels observations outside persistent regions as noise.

Unlike DBSCAN, HDBSCAN does not reproduce a single fixed-epsilon DBSCAN solution.

---

# Appendix D: Silhouette Caveats

- UMAP is designed to emphasize neighbourhood structure.
- Silhouette measured in embedded space can overstate separation.
- Hyperparameter and seed selection also make the selected estimate optimistic.
- Seed stability, PCA, and alternative representations provide supporting evidence.

**Interpret silhouette as an internal pipeline-quality metric, not proof of natural categories.**

---

# Appendix E: Missing-Not-At-Random Sensitivity

- MAR was used as the principal working assumption.
- MNAR mechanisms cannot be ruled out from observed values alone.
- Extreme MNAR analyses suggest that Global Impairment is comparatively robust.
- Boundaries between less impaired tiers are more sensitive.

---

# Appendix F: Clinical Interpretation Boundary

The severity tier:

- supplements diagnosis;
- supports rehabilitation discussion;
- can be accompanied by a confidence estimate;
- may assist outcome modelling.

The severity tier does not:

- diagnose a patient;
- prescribe treatment;
- determine clinical placement;
- replace professional judgement.

---

# Appendix G: Future Work

- External replication across rehabilitation centres
- Direct longitudinal modelling of recovery trajectories
- Validation against return to work, length of stay, and independence
- Alternative model-based phenotyping, including latent profile analysis
- Prospective evaluation of CogDash in clinical workflows
- Greater sensitivity to domain-specific dissociations
