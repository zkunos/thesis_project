# Proposed clustering extension: implementation protocol

Prepared 15 October 2026. Status: **original prospective design; implementation and results are documented separately in [the results report](clustering_results_2026.md)**. Companion evidence review: [recent research](clustering_research_2026.md). Settings below describe the proposed design; the results report records executed settings, exploratory additions and deviations. They are not validated clinical thresholds or claims from the articles.

**First deliverable: one consistent data contract**

Create a shared preprocessing module before adding models. It should return immutable assessment keys, patient keys, observed-value masks, transformed test variables and six-domain composites. Reconcile eligible rows to the source using explicit keys; do not attach patient IDs or times by unverified row position. Verify uniqueness, join cardinality, domain membership and score directions.

Record input hashes, cohort counts, inclusion rules and software versions. Inspect `ID` and `TSI_TO_ASSESSMENT_DAYS`, which are referenced by NB14; confirm that elapsed time has a consistent clinical origin and that multiple injuries or episodes can be distinguished. Neither field belongs in the cross-sectional cognitive distance matrix. Source spreadsheets are locally modified relative to Git; saved outputs should not be assumed to describe the newest input version.

Fit clipping bounds, scaling parameters and administration-frequency weights using discovery patients only. Apply the fitted transformations unchanged to validation patients. Use NB5's direction-alignment logic as the starting point and verify it against the test definitions. Replace NB14's divergent aggregation in the new shared workflow. Report sensitivity to clipping because clipping does not remove genuine floor or ceiling effects.

For primary cross-sectional discovery, select one clinically defined index assessment per patient, with a documented tie-breaking rule. Selecting the earliest available assessment is a workable default after checking timestamps and eligibility. This changes the estimand from assessment states to patient index profiles; preserve the original all-assessment analysis as a comparison. In analyses retaining all visits, split and resample whole patients. An ordinary mixture likelihood on all visits still assumes independence even when its uncertainty estimates are patient-bootstrapped.

**Proposed NB15 — Original-space structure and incomplete-data models**

Inputs: the verified eligible test matrix, missingness mask and patient manifest.

- Reserve 20% of patients for final validation before tuning; perform method selection within the remaining patients. With a single cohort, this is internal validation, not external replication.
- Check cluster tendency using prespecified PCA/dip and PCA/Silverman analyses of the completed six-domain representation. Repeat across imputations and a complete-case sensitivity set. Treat p-values across imputations as dependent diagnostics; do not average them or pool them using Rubin's rules. Calibrate any combined decision using simulation of the full procedure.
- Benchmark PAM and existing k-means, GMM and HDBSCAN directly in six-domain space; retain the current UMAP branch for comparison. Search candidate counts two through eight for partition algorithms. Include one-component/no-subgroup reference models separately; silhouette is undefined for a one-cluster solution.
- Fit a restricted set of robust mixture families to the incomplete 14-test matrix, allowing one through eight components. Check implementation support for the single-component case and fit an equivalent reference likelihood separately if necessary. Keep bounded/discrete score limitations visible. Do not compare likelihood criteria across different feature spaces, sample sets or incompatible transformations.
- Use multiple starts, record convergence and singular fits, and report BIC/ICL, membership entropy and original-space separation. If the best component count is still at the search boundary, record an unresolved boundary rather than declaring an optimum.
- Add a secondary profile-shape analysis by projecting out the training-derived first principal direction. Work in the remaining five-dimensional basis, so the covariance is not singular by construction. Interpret differences alongside absolute domain means.

Reference simulations should include a continuous severity factor with correlated residuals, skewness, observed score limits and realistic missingness, plus positive controls with overlapping unequal groups. Repeat the entire tuning procedure on each simulated dataset. Simple independent column permutation destroys genuine correlations and is not an adequate continuous-severity null. Rejection of any one null establishes only a mismatch with that null. Where the null is estimated on the same patients, include parameter estimation in the simulation and check calibration.

Proposed output: `results/research_2026/model_comparison.csv`, recording representation, cohort, family, component count, convergence, coverage, original-space metrics and runtime. Save row assignments only with verified keys.

**Proposed NB16 — Independent refitting across imputations and patients**

Start with 20 stochastic imputations and 50 patient subsamples as a feasibility pilot. Increase repetitions only after checking Monte Carlo stability and runtime. Use an imputation model compatible with the feature types and intended cluster structure; adding seeds to a deterministic imputer is not multiple imputation. Model or assess the structured missingness seen in routine clinical test selection. MAR-based methods do not resolve unobserved-value-dependent missingness by themselves.

Compare four explicitly different sources of variation: imputation draw, imputation model, clustering initialization and patient resampling. Keep H2's existing fixed-reference result as its own comparator. For the new ensemble, start with independently fitted k-means/PAM at each fixed candidate count. Compare agglomerative and greedy-NMI aggregation, with NMF as a sensitivity choice. Use the author implementation linked from the evidence review, after checking license and reproducibility.

For subsampled partitions, estimate co-assignment only when both observations are available. For density methods, distinguish joint availability from joint non-noise assignment; report both coverage and conditional agreement. Two noise points are not automatically a shared phenotype. For label-specific summaries use an explicit matching procedure, allowing unmatched clusters. ARI itself is label-invariant and requires no label matching.

Validate on the same untouched patients using a prespecified assignment rule. Separately compare independently discovered partitions on validation patients where sample size permits. Agreement under a fixed assignment rule and recovery after independent discovery must remain separately reported.

At 17,406 rows, one dense float64 co-assignment matrix alone requires about 2.42 GB (2.26 GiB), before intermediates. Start with one row per patient or blockwise/sparse computations and a measured memory budget. Do not silently create one full matrix per bootstrap.

Proposed outputs: `refit_agreement.csv`, `cluster_count_distribution.csv`, `per_cluster_stability.csv`, `assignment_uncertainty.csv` and `missingness_sensitivity.csv`. Report patient counts, noise/coverage, cluster-size distributions and uncertainty; avoid a single winner selected by peak embedded silhouette.

**Proposed NB17 — Patient recovery trajectories, conditional on data adequacy**

First tabulate visits per patient, elapsed-time distribution, duplicate times, changing test availability and dropout. The saved count of patients with at least two visits is not evidence of sufficient repeated measurements for every trajectory model.

Begin with a continuous mixed-effects model of severity over time. Compare a small feature/distance approach with a latent class mixed model only where the measurement schedule supports it. Keep baseline level and rate of change distinct. Use observed time spacing, not visit index as a substitute. Restrict nonlinear or multivariate trajectory mixtures to subsets with adequate observations and report the resulting selection bias. A mixed-effects model can pool information from sparse patients, but their individual class assignments may remain highly uncertain.

Assess random-start convergence, minimum class sizes, patient resampling and whether the apparent classes merely subdivide a continuous distribution of intercepts/slopes. Use the robust multivariate model in the review only after obtaining its full methods and checking software and missing-data assumptions. Do not turn estimated individual slopes into error-free clustering inputs.

Proposed outputs: `trajectory_data_audit.csv`, `trajectory_model_comparison.csv`, `trajectory_membership_uncertainty.csv` and a patient-level validation summary.

**Decision and thesis integration**

Advance a candidate only if it is reproducible across patients and imputations, distinguishable in measured features, and not predominantly an administration/missingness artifact. Report uncertainty for small or weakly separated groups. Check clinical relevance using outcomes not used to construct the groups, preferably comparing a model with continuous severity to the same model plus cluster information. Choose any minimum useful predictive improvement before viewing validation results. If an outcome is unavailable, describe the result as exploratory structure without established clinical utility.

Map NB15 to an H1/H4 extension, NB16 to an H2 extension, and NB17 to a new longitudinal question. Report new results separately from the original prespecified hypotheses; the repository does not establish external preregistration. Keep original outputs intact and save this extension under `results/research_2026/`.

The first implementation milestone is the data contract and NB15 pilot. Proceed to larger ensembles after the pilot verifies input consistency, fit behavior and runtime. The literature review does not establish that any candidate will outperform the existing severity representation.
