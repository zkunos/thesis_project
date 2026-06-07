<!-- Exported prose chunk 9. Word count: 1245. -->


## Robustness Analyses

_Source: `report/Chapters_short/Chapter4.tex`_

Several robustness checks contextualise the primary hypothesis tests: a listwise-deletion baseline, subsampling stability, bootstrap confidence intervals for key estimates, Rubin-pooled uncertainty across multiple imputation draws, outcome-adjacent validation using time-since-injury, and multiple-comparison corrections for the 45 pairwise H2 tests.

Bootstrap confidence intervals. A non-parametric bootstrap at the patient level produced tight 95% confidence intervals for the key estimates: 0.710 for the H2 mean ARI; 0.16 for H3 Cramér's V; and 0.05 for the H4 silhouette gap (domain minus variable). These narrow intervals should be interpreted in light of the large cohort size (n = 17{,}406), not as evidence that all effects are large.

H2 and multiple-comparison correction. Testing Hypothesis 2 requires 45 pairwise ARI comparisons against the >0.5 threshold. I applied Holm-Bonferroni correction to control family-wise error and Benjamini-Hochberg correction for the false discovery rate, using a parametric one-sided bootstrap p-value for each pair. Under both corrections, 44 of the 45 pairs rejected the null at alpha = 0.05. The only exception was KNN-SoftImpute (bootstrap mean ARI 0.509, 95% CI ), whose interval straddled the 0.5 threshold. Thus, imputation robustness holds for all method pairings except this borderline case.

Rubin-pooled multiple imputation. To estimate uncertainty from a single MICE run, I generated M = 5 independent draws, ran the full pipeline on each, and pooled the hypothesis-level metrics with Rubin's rules. The estimates remained positive and bounded: 0.154 for Cramér's V (H3) and 0.050 for the silhouette gap (H4). The recovered cluster count varied from three to seven across draws, as expected when discretising a continuous gradient, but the H4 gap was stable. Domain-level features outperformed variable-level features in every independent draw.

Listwise-deletion baseline. Applying the pipeline to the 9{,}245 complete cases produced two clusters with a silhouette of 0.257. Agreement with the MICE solution for those same patients was moderate (ARI 0.625, NMI 0.519), but the solutions were not equivalent. Imputation materially affects the analysis: discarding the 46.9% of assessments with missing values changes both the quality and number of tiers recovered.

Subsampling stability. Random 80% subsamples processed with UMAP+HDBSCAN recovered the same broad severity structure, but exact labels and cluster counts varied from two to five. This is expected when a continuous gradient is converted into discrete categories and is consistent with the per-cluster Jaccard results for Hypothesis 1.

Missingness-threshold sensitivity. I re-ran the full process, including variable filtering, domain recomputation, MICE imputation, and UMAP+HDBSCAN, at five Tier 1 thresholds from 30% to 70%. As Figure fig:sensitivity shows, the solution remained in the two-to-three tier range with silhouettes from 0.39 to 0.52 for thresholds between 40% and 70%. It broke down only at the 30% threshold, which was too restrictive and left too few variables. The 50% threshold used in the main analysis is therefore a reasonable compromise between completeness and variable availability.

Outcome-adjacent validation. Functional outcome variables are unavailable, but within-patient change can be examined through time-since-injury (TSI) at assessment. TSI varies significantly by tier (Kruskal-Wallis test, p = 4 times 10^{-28}): medians are 214 days for Above-Average, 188 for Near-Normal, and 172 for Global Impairment. More impaired patients are assessed slightly earlier after injury. Among the 5{,}206 patients with two or more assessments, 50.2% (n = 2{,}613) remain in the same tier and 49.8% (n = 2{,}593) change tier. Such mobility is more consistent with movement along a severity gradient than with fixed phenotypes. Among the 912 patients with exactly two assessments who change tier, movement toward better function is about three times more frequent than movement toward worse function (706 vs. 206 transitions), matching the expected clinical recovery pattern.

Caption: Sensitivity to the Tier 1 missingness threshold across five values (30-70%). Top row: (a) number of eligible variables and (b) number of clusters recovered. Bottom row: (c) silhouette score and (d) noise proportion. Dashed line marks the 50% threshold used in the primary analysis.

Embedding-seed stability. To check whether the partition depended on UMAP's stochastic initialisation, I re-ran the full embedding-and-clustering pipeline on the MICE-imputed domain scores using ten random seeds with identical hyperparameters. The label sets were highly concordant: the mean pairwise ARI across the ten runs was 0.957 (median 0.96, range 0.90-1.00), increasing to 0.965 after k-nearest-neighbour reassignment. The recovered structure is therefore not driven by random initialisation. Together with the deterministic PCA support for the severity axis (§sec:cluster_profiles), this reduces concern that the result is an unstable artefact of UMAP.

Latent-profile baseline. As a model-based comparison, I fitted Gaussian mixture models with full covariance, corresponding to the engine of latent profile analysis, to the domain scores for k from 2 to 6. The Bayesian Information Criterion fell monotonically with k (from 243{,}249 at k=2 to 92{,}606 at k=6) with no local minimum, a pattern more consistent with a continuum than with well-separated latent classes. The mixture solutions agreed only moderately with the density-based tiers (ARI 0.35-0.40), and the two-component solution had the clearest silhouette (0.45). This model-based baseline therefore supports the same conclusion as the main pipeline: there is no clear discrete-class optimum, consistent with an underlying severity gradient.

MNAR tipping-point. To bound the possible effect of a missing-not-at-random mechanism, I re-imputed every missing value to the worst observed performance on its variable: the minimum value, or the maximum for the timed ATMTA. This is an intentionally extreme and pessimistic assumption. Under this scenario, the partition fragmented and the silhouette fell to 0.03 because forcing all missing values to a single extreme created point-mass spikes. Even so, a distinct lowest-severity tier persisted and retained 65.2% of the assessments originally assigned to Global Impairment. The Global Impairment tier is therefore the most robust part of the solution. The extreme MNAR assumption mainly degrades the finer separation among milder tiers, and a formal delta-shifted tipping-point analysis would be a useful extension.

Characteristics of excluded records. Reconstructing the Tier-1 filter on the full raw cohort retained roughly 16{,}600 of the 22{,}075 records, close to the 17{,}406 used in the main analysis, and excluded about 5{,}500. The excluded records completed only 0.8 of the 14 eligible tests on average, compared with 12.5 among retained records. They therefore appear to be near-empty administrative encounters rather than partially tested, severely impaired patients. The two groups were demographically similar (age at injury 45.7 vs. 46.3 years, Cohen's d = -0.04; 63% vs. 68% male; time-since-injury 2.3 vs. 1.6 years, d = 0.16). The filter is therefore unlikely to hide a severe subgroup on measurable characteristics, although the cognitive severity of excluded records cannot be observed directly.



## Cluster Clinical Naming

_Source: `report/Chapters_short/Chapter4.tex`_

A rule-based labeller was used to assign descriptive names from the domain-level z-score profile of each cluster. Clusters with most domains above +0.5 were labelled Above-Average; clusters mostly below -0.5 were labelled Global Impairment; and clusters near the cohort average were labelled Near-Normal. This produced the final labels Above-Average (n = 6{,}725), Near-Normal (n = 6{,}328), and Global Impairment (n = 4{,}353). Because the tiers differ in overall level rather than profile shape, severity labels are more accurate than phenotype names. They provide useful shorthand for clinical discussion and rehabilitation triage. The full mapping of identifiers and assessment counts is available in the interactive CogDash dashboard.


---REWORK
The above-referenced text contains 18 paragraphs. All 18 will be rewritten.

In addition to rewriting the paragraphs, the first section will include references and/or citations in APA style.

**Robustness Analyses**

_Source: report/Chapters_short/Chapter4.tex_

There are several analyses that have been done to help us understand the robustness of our hypotheses. First, we used a "listwise deletion" baseline. Second, we did a sub sampling stability study. Third, we estimated bootstrap confidence intervals. Fourth, we estimated Rubin-pooled uncertainty across multiple imputation draws. Fifth, we validated our findings using time since injury as an alternative measure. Finally, we used multiple comparison corrections for the 45 pairwise H2 tests.

Bootstrap Confidence Intervals. We performed a nonparametric bootstrap analysis of our data at the individual level. For the major estimates, we obtained very narrow 95% confidence intervals around the estimated effects. For example, the bootstrap 95% confidence interval for the H2 mean ARI is .710; for H3, it is .16 (Cramers V); and for H4, it is .05 (silhouette gap). The small widths of these confidence intervals should be viewed in relation to the large sample size (n = 17{,}406) of our cohort, and not as evidence that all the effects we found are large.

H2 & Multiple Comparison Correction. In order to test H2, we need to perform 45 different pairwise ARI comparisons against a cutoff of greater than .5. Therefore, we applied Holm-Bonferroni corrections to ensure family wise Type I error rates, and Benjamini-Hochberg corrections to ensure false discovery rates. Using a parametric one sided bootstrap p-value for each pair, under both types of corrections, we reject the null for all 44 pairs except KNN-SoftImpute (bootstrap mean ARI = .509, 95% CI ). Thus, with respect to imputation robustness, all method pairs are significant except this one borderline case.

Rubin-Pooled Multiple Imputation. To estimate uncertainty from a single MICE run, we generate M = 5 independent draws, run the entire pipeline on each draw, and then pool the hypothesis-level statistics with Rubins Rules. The resulting estimates remain positive and bounded: .154 for Cramers V (H3), and .050 for the silhouette gap (H4). Furthermore, the number of clusters recovered varied between 3 and 7 across draws as expected given that we are discretizing a continuous gradient; however, the H4 gap remained stable. Also, domain level features outperform variable level features in every one of the independent draws.

Listwise Deletion Baseline. If we discard the 46.9% of the assessments with missing values and apply the pipeline only to the remaining 9{,}245 complete cases, we obtain two clusters with a silhouette of .257. Additionally, agreement between the MICE solution for those same patients and the solution based solely on complete cases is moderate (.625 ARI, .519 NMI), yet they are clearly not equivalent. Hence, imputation has a material impact upon the analysis: discarding the 46.9% of the assessments with missing values changes both the quality and quantity of tiers recovered.

Subsampling Stability. When processing random 80% subsamples of our cohort using UMAP+HDBSCAN, we find that the majority of samples recover the same general severity structure; however, exact labels and numbers of clusters vary from two to five. This is precisely what would be expected if we were converting a continuous gradient into discrete categories and is consistent with the per-cluster Jaccard results for H1.

Missingness Threshold Sensitivity. I also re-ran the entire process -- including variable selection; domain computation; MICE imputation; and UMAP+HDBSCAN -- at five Tier 1 thresholds from 30% to 70%. As shown in Figure fig:sensitivity, the solution remains in the two to three tier range with silhouettes ranging from .39 to .52 over thresholds of 40% to 70%. Only at 30%, where we are being overly restrictive with regards to how many variables we allow, does the solution break down. Therefore, our choice of 50% threshold used throughout our main analysis represents a reasonable balance between how much information is present in each record and how many variables are available.

Outcome-Adjacent Validation. Although functional outcomes are unavailable for use as validating measures of impairment status at discharge; nonetheless, we may examine functional change through time-since-injury (TSI) at each assessment as an alternate validating measure. TSI varies significantly by tier (Kruskal-Wallis test p < 4 x 10^{-28}), with median TSI times of 214 days for Above Average; 188 days for Near Normal; and 172 days for Global Impairment. Thus, as TSI increases, so does severity of impairment -- at least with regard to these three tiers. Among the 5206 patients who have had at least two assessments, 50.2% (2606 patients) maintain their original tier assignment while 49.8% (2593 patients) experience some degree of tier shift. While such movement could suggest that patients possess a set of fixed phenotypic characteristics, such movement is far more indicative of variability in severity along a spectrum of impairment severity. Furthermore, among the 912 patients who experienced exactly two assessments and changed tiers during that period, improvement in functional status occurred approximately three times as frequently as worsening in functional status (706 vs. 206 transitions), consistent with expectations regarding natural clinical recovery patterns.

Figure Caption: Sensitivity to Tier 1 Missingness Threshold Across Five Values (30-70%)

Top Row:

(a) Number of Eligible Variables
(b) Number of Recovered Clusters

Bottom Row:

(c) Silhouette Score
(d) Noise Proportion

Dashed Line Represents Choice of Tier 1 Threshold Used Throughout Primary Analysis

Embedding Seed Stability. To determine whether the clustering was due to UMAP's random initialization or not; we repeated the entire embedding and clustering process on our MICE-imputed domain scores using ten randomly selected seeds with equal hyperparameter settings. There was high concordance between labeling schemes; specifically the mean pairwise ARI across the ten runs was .957 (median = .960, min-max = [0.900;1.000]). After k-nearest neighbor reassignment; this increased to .965. With respect to our finding that there exists a strong underlying severity axis supported by deterministic PCA (see §sec:cluster_profiles); together with embedding seed stability; this further decreases concerns that our solution was simply an artifact of unstable UMAP initialization.

Latent Profile Baseline Model. As a model-based comparison; I fit Gaussian mixture models with full covariance matrices (i.e., analogous to latent class modeling engines) to our domain scores for k varying from 2 through 6. As shown in Figure , BIC decreased monotonically with k (from 243{,}249 at k=2 to 92{,}606 at k=6) without any local minima; suggesting that there is no discrete class optimum -- but rather a continuum. Moreover; mixture model solutions agree modestly with density-based tiers (ARI = .350-.400); and the best silhouette (at k=2) is associated with the highest number of components (k=2). Therefore; model-based baseline supports conclusions made via the primary pipeline; namely that there is no discrete class optimum -- but rather an underlying continuum representing severity.

MNAR Tipping Point. To establish bounds on potential missing-not-at-random mechanisms; I assumed every missing value was replaced by the worst observed performance on that variable -- either the minimum value or the maximum value depending on whether it was a timed ATMTA or not. Clearly this is an intentionally extreme and conservative assumption. Under this condition; even though the partition became fractured; and the silhouette fell to .030 due to creation of point mass spikes when all missing values were forced to extreme values; nevertheless a distinct lowest severity tier still existed; and retained approximately 65.2% of assessments originally labeled as Global Impairment. Therefore; even under extreme MNAR assumptions; Global Impairment is likely the most robust portion of our solution. Most importantly; extreme MNAR assumptions seem to degrade finer separation within lower severity tiers -- and thus a formal delta-shifted tipping point analysis seems like an interesting future direction.

Summary Characteristics of Excluded Records. By reapplying the Tier-1 filter to our entire raw cohort; we were able to retain approximately 16{,}600 of our approximately 22{,}075 records; which is close to the number of records retained in our primary analysis (approximately 17{,}406). Conversely; we discarded approximately 5{,}500 records. Discarded records averaged only .800 of their 14 eligible tests; whereas retained records averaged 12.5 tests per record -- thereby appearing to represent nearly empty administrative encounters instead of incomplete testing of severely impaired individuals. Demographically; both excluded records and retained records are largely indistinguishable (e.g., age at injury: 45.7 vs. 46.3 years; Cohen's d = -0.04; sex: male/female = [63%;37%] vs.[68%;32%]; TSI: 2.3 vs. 1.6 years; d = .16). Therefore; we do not believe that our Tier-1 filter will suppress detection of a cognitively impaired subgroup identifiable via measurable characteristics -- although we obviously cannot assess cognitive impairment directly.

Cluster Clinical Labeling

_Source: report/Chapters_short/Chapter4.tex_

To give our density-based clusters clinically relevant labels; we employed a rule-based naming system based upon the domain-level z-score profiles associated with each cluster.

Clustering Profiles Associated with Domains Having Z-Scores Greater Than +0.5 Were Labeled Above Average.

Profiles Associated with Domains Having Z-Scores Less Than -0.5 Were Labeled Global Impairment.

All other profiles were labeled Near Normal.

This resulted in our final labels being Above Average (n = {,}725), Near Normal (n = {,}328), and Global Impairment (n = {,}353).

Since our tiers differ primarily in terms of overall level and not profile shape -- severity labels are preferable to phenotype names.

They provide valuable shorthand for clinicians engaged in discussing potential rehabilitation options with their patients -- as well as providing useful tier-based guidance for rehabilitation triaging efforts.

The full mapping of identifier codes to assessment frequency is contained within our interactive CogDash dashboard