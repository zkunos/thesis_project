<!-- Exported prose chunk 10. Word count: 1375. -->


## A Cognitive Severity Gradient, Not Discrete Phenotypes

_Source: `report/Chapters_short/Chapter5.tex`_

The central empirical result is negative in one sense and informative in another: this ABI cohort does not resolve into qualitatively distinct cognitive phenotypes, but it does exhibit a robust gradation of cognitive severity. The algorithm partitions patients into Above-Average, Near-Normal, and Global Impairment tiers. Those tiers differ by level, not by profile shape. In Figure fig:radar_profiles, all six domains move together; one principal component explains 56 per cent of the variance and loads positively, with similar magnitude, across the domain scores. The recovered structure is therefore better characterised as severity stratification than as a set of dissociable profiles. This remains clinically relevant because the axis is derived from cognitive test performance itself, not from the injury-severity bands or diagnostic categories criticised in Chapter Chapter1. Its association with clinical-unit placement beyond diagnosis (§sec:h3_results) indicates that it captures information used, implicitly or explicitly, in rehabilitation routing.

The finding also informs a broader question in neuropsychology: whether variability across test batteries is primarily domain-specific or dominated by a general factor. In this routinely collected cohort, the general severity axis accounts for most of the recoverable structure. Secondary domain-specific variation is present but does not define the clustering. That pattern is consistent with both clinical observation, where global impairment often separates patients before narrower dissociations are considered, and the positive manifold of inter-test correlations described in neuropsychology [@lezak2012neuropsychological]. The phenotyping result is therefore more conservative than some prior accounts would suggest. When the data are processed under an imputation-robust, sensitivity-tested pipeline, overall severity emerges before specific profile patterns.

This does not invalidate studies such as [@garcia2020data], which report two to four dissociable profiles after brain injury. It qualifies their interpretation. The present pipeline differs in several respects: UMAP+HDBSCAN accommodates non-convex structures and low-density noise; bootstrap analysis evaluates reproducibility; and each variable is winsorised, direction-aligned, and standardised before aggregation. These steps matter. A high-variance raw measure, such as a timed Trail Making score, can dominate an unstandardised composite; a non-cognitive variable can impose an artificial axis; a nearly empty record can perturb density estimates. Apparent phenotypes may then reflect preprocessing rather than neuropsychological structure. Chapter Chapter6 returns to this methodological dependency.

The stability analyses (§sec:h1_results) reinforce the severity-gradient interpretation. Across bootstrap resamples, all ten imputation methods meet the pre-registered H1 criterion. The core Jaccard analysis shows greater stability for the two extreme tiers than for the central Near-Normal tier, which is the expected pattern when a middle band is cut from a continuum. Boundary patients can move between adjacent tiers without undermining the underlying ordering.

For that reason, the three-tier solution from the primary MICE pipeline should be used as an interpretable discretisation rather than as a claim about natural kinds. Other methods recover between three and five tiers. Rubin pooling and threshold sensitivity show that cluster count can vary while severity ordering remains stable. The clinically useful object is the continuum; the tiers are a practical representation of it.



## Imputation Sensitivity

_Source: `report/Chapters_short/Chapter5.tex`_

Hypothesis 2 provides the most important methodological result. Cluster solutions change relatively little across imputation methods: on the domain-level features, the mean pairwise ARI is 0.710, and all 45 method pairs exceed 0.50 (§sec:h2_results). A strong severity gradient is easier to recover than a fragile multidimensional profile structure, which likely explains the robustness while still allowing method-specific variation [@rubin1987multiple].

The method dendrogram in Figure fig:h2_dendrogram makes a clean separation between two imputation families: the smooth, model-based methods (EM, DAE, and VAE), which tend to smooth toward a model-based conditional mean; and the local, donor-based KNN, which relies on a few local donors to plug in missing values. A division along the lines of statistical, machine-learning, or deep-learning families might be expected; however, the more telling distinction is smooth versus local.

At assessment level, instability correlates moderately with the fraction of imputed data (r = 0.474; §sec:h2_results). Method choice matters most when the observed part of the assessment is sparse [@little2019statistical]. Downstream applications should therefore treat heavily imputed assessments differently from nearly complete ones, either by reporting lower confidence or by comparing more than one imputation strategy.

Consensus clustering offers a practical response. The ten methods are aligned, their labels are allowed to vote, and the resulting confidence score quantifies agreement. Overall confidence is high (mean 0.929, with 86.2% of assessments high-confidence), but the minority of lower-confidence cases is clinically informative rather than inconvenient. These patients are typically near tier boundaries and should prompt caution or reassessment.

In the literature, MICE is commonly used for neuropsychological data before clustering [@vanbuuren2011mice], while MissForest [@stekhoven2012missforest] is often preferred when non-linear relationships are expected. After Holm-Bonferroni correction across the 45 pairs (Section sec:robustness), 44 reject the null hypothesis that ARI le 0.5. The KNN-SoftImpute pair remains near the threshold, but the broader result is clear: the severity signal is not dependent on a single imputation method.

The listwise-deletion baseline in Section sec:robustness shows why imputation is necessary. Restricting the analysis to complete cases produces a different cluster count, a lower silhouette (0.257), and only moderate agreement with the MICE solution for the shared patients (ARI 0.625). Imputation is therefore not merely a cosmetic step: removing the 46.9% of assessments with missing data changes the recovered structure. Rubin pooling across independent MICE draws confirms the domain-level advantage and the tier-unit association, although cluster count remains somewhat variable.



## Clinical Unit Association

_Source: `report/Chapters_short/Chapter5.tex`_

Cognitive severity is associated with clinical unit, although the effect size is small by Cohen's conventions. The Cochran-Mantel-Haenszel test indicates that the association is not reducible to diagnosis group (§sec:h3_results). Severity tier therefore carries placement information beyond diagnostic category.

This is clinically plausible. Diagnosis is often used as a proxy for injury mechanism and expected recovery when patients are referred to rehabilitation units [@saatman2008classification, maas2017traumatic]. Yet a patient in the Global Impairment tier generally requires more intensive and structured rehabilitation than a patient in the Above-Average tier, even if diagnostic labels overlap. The persistence of the tier-unit association after diagnostic stratification suggests that rehabilitation services may already be routing patients partly by impairment level. Making that stratification explicit would allow triage decisions to be audited and refined [@corrigan2010epidemiology].



## Feature Engineering

_Source: `report/Chapters_short/Chapter5.tex`_

The H4 result is clear: domain-aggregated features are much better conditioned than variable-level features, even though the improvement in cluster separation is small. The silhouette changes only slightly (0.481 vs. 0.473), but mean VIF falls from 2.77 to 1.88 and the condition number falls from 61.7 to 11.8 (§sec:h4_results). If several highly correlated tests enter the model as separate features, UMAP and HDBSCAN can over-weight the shared cognitive dimension in their distance computations. Aggregation gives one feature per construct, so each domain contributes more evenly. This provides quantitative support for the clinical practice of interpreting test batteries by domain rather than test by test [@lezak2012neuropsychological]. This benefit depends on preprocessing: variables must be winsorised, direction-aligned, and standardised before aggregation so that raw scale differences do not dominate the composites.



## Feature Importance and What Drives Severity

_Source: `report/Chapters_short/Chapter5.tex`_

The feature-importance results (§sec:feature_importance) should be treated as descriptive rather than explanatory. The Random Forest surrogate reaches 99.4% accuracy using the same domain scores that generated the labels, so its ranking mainly reconstructs the partition boundaries. It ranks orientation, visuoperception, and language above attention and executive function, but this ordering should not be given a strong clinical interpretation. The domains are highly correlated, and Gini importance can be unstable under correlated predictors [@boulesteix2012overview].

The more reliable finding is the principal-component structure: one component captures 56% of the variance in overall cognitive severity, with similar positive loadings across all six domains. The tiers are therefore best interpreted as general severity levels rather than as domain-specific dissociations or an attention-specific pattern. The robustness checks (§sec:robustness), including subsampling and missingness-threshold evaluations, support this conclusion. The severity ordering remains stable, even though the exact tier count depends on clustering resolution and inclusion threshold. Data-driven phenotyping studies should therefore report preprocessing choices clearly and include sensitivity analyses.


---REWORK

## a cognitive severity gradient, not discrete cognitive phenotypes

_source: `report/Chapters_short/Chapter5.tex`_

Overall, there was no evidence of discrete cognitive phenotypes in this cohort of people with acquired brain injury (ABI); instead, the results demonstrate a clear cognitive severity gradient. We have identified patients as being in the ‘above average’, ‘near normal’ and ‘global impairment’ tiers based upon their performance across the battery. Importantly, these tiers differ by level, not by profile shape. As illustrated in fig fig:radar_profiles, each of the six domains are moving together. One principal component explained 56% of the variance in the domain scores and loaded positively across all six domains with a similar magnitude. Therefore, we view our results as demonstrating a severity stratification of the cognition of individuals with ABI, rather than an identification of a set of dissociable cognitive profiles. While this is clinically useful, because the axis is derived from performance across the cognitive tests themselves, and not from the injury-severity bands or diagnostic categories criticized in Chapter Chapter1, it is also relevant to note that it demonstrates an association with clinical-unit placement that extends beyond diagnostic category (§sec:h3_results).

Moreover, our results inform a broader question in neuropsychology: whether variability across test batteries is primarily domain-specific or dominated by a general factor. Our results indicate that in this routinely collected cohort, the general severity axis accounted for most of the recoverable structure. There is secondary domain-specific variation present; however, this did not determine the clustering. The pattern demonstrated here is consistent with both clinical experience where global impairment often separates patients before they are differentiated further through narrow dissociations [e.g., @maas2017traumatic], and the positive manifold of inter-test correlations found in neuropsychology [@lezak2012neuropsychological]. Therefore, the phenotyping result reported here is more conservative than suggested by some other accounts. Specifically, when the data were analyzed under conditions of imputation-robust, sensitivity tested pipelines, overall severity emerged before specific patterns of profiles.

Our findings do not refute studies that report multiple dissociable cognitive profiles after brain injury (e.g., @garcia2020data). Rather, they qualify their interpretations. Unlike those studies, our pipeline differed in several ways. For example, UMAP+HDBSCAN allows for processing of non-convex structures and low-density noise; our bootstrap analysis provided an evaluation of the replicability of our clusters; and each variable was standardized and winsorized in addition to being direction-aligned before forming aggregates. Each of these steps made a difference. High variance raw measures (i.e., a timed Trail making score) can dominate an unstandardized composite; non-cognitive variables can establish artificial axes; nearly empty records can disrupt density estimates. Thus apparent phenotypes may represent artifacts of preprocessing rather than true neuropsychological structure. Chapter Chapter6 will examine this relationship further.

The stability analyses (§sec:h1_results) provide additional support for our characterization of the cognitive gradients as a severity gradient. All ten imputation methods met the pre-registered H1 criterion in terms of the stability analyses. The Jaccard analysis shows greater stability for the two extremes (the 'above average' and 'global impairment' tiers) compared to the central tier ('near normal') which has been cut from a continuum. Patients at the boundary between two tiers can move between them without disrupting the underlying order.

Therefore, we advocate that the three-tier solution developed from the primary MICE pipeline be viewed as an interpretable discretization of a continuum rather than as evidence of natural kinds. Other clustering techniques produce between 3 and 5 tiers depending on how they are configured. Rubin pooling and sensitivity to thresholds show that while cluster counts may vary, the ordering by severity remains constant. The clinically useful entity is thus the continuum; the tiers represent a convenient way to describe aspects of it.

## robustness regarding imputation methods

### _source:_ `report/Chapters_short/Chapter5.tex`

Hypothesis 2 represents the major methodological contribution. Clustering solutions change very little with regard to imputation methods: on average, the 45 method-pairs yielded a mean pairwise ari > .70, with 100% yielding an ari > .50 (§sec:h2_results). Therefore, what is easy to recover is a strong severity gradient and less easily recovered is a fragile multi-dimensional profile structure. This is likely responsible for the robustness while still allowing for method-specific variability [@rubin1987multiple].

As depicted in fig fig:h2_dendrogram, a strong separation exists between two families of imputation methods: smooth, model-based methods (EM, DAE, and VAE) that tend to smooth towards a model based conditional mean; local donor-methods (KNN) that rely on a few local donors to plug in missing values. Although many studies use classification criteria related to whether or not an imputation method uses statistical/machine learning/deep learning families, the more salient divide appears to be between smooth and local.

At assessment level: instability correlates moderately with fraction of missing data
Instability correlates moderately with fraction of imputed data (r = .47; §sec:h2_results). As such, downstream applications should treat assessments with heavy amounts of missing data differently from assessments that contain almost no missing data. This could be achieved by reporting decreased confidence or by comparing more than one imputation strategy.

A consensus-clustering approach represents a practical means of addressing this issue. The ten imputation strategies will align their votes regarding label assignments for individual assessments. The resulting confidence score represents an estimate of agreement among strategies. Overall confidence is high (mean 0.93 confidence; 86.2 % of assessments have high confidence). However, as discussed previously, the lower-confidence assessments are clinically meaningful rather than merely inconvenient. Most notably, these assessments represent patients who are located near tier-boundaries and should prompt caution/re-assessment.

In the literature, MICE is commonly used prior to clustering neuropsychological data.
MissForest [@stekhoven2012missforest] is often preferred when non-linear relationships are expected.
After applying Holm-Bonferroni correction across the 45 pairs of comparison (see section sec:robustness), 44 reject the null hypothesis that ari ≤ .50.
Only the KNN-softimpute pair remains at or near threshold levels.
The broader result is clear: the severity signal does not depend upon a single imputation strategy.

We also provided a listwise deletion baseline in section sec:robustness to illustrate why imputation is necessary.
Restricting analysis to only complete cases results in a different number of clusters and silhouette (.25) compared to the MICE solution for shared patients (ari .63).
Thus, while removing the 46.9% of assessments with missing data changes recovered structure, imputation was not merely cosmetic.

## clinical unit relationship

### _source:_ `report/Chapters_short/Chapter5.tex`

Severity tiers were associated with clinical units.
However, the effect size was small by Cohen’s standards.
The Cochran-Mantel-Haenszel test demonstrated that this association was not reducible to diagnostic category.
Therefore, severity tier represents placement information beyond diagnostic category.

This association is clinically plausible.
Diagnosis is frequently used as a proxy for mechanism of injury and expected recovery when patients are referred to rehabilitation units [@saatman2008classification].
However, patients in the Global Impairment tier generally require more intensive and structured rehabilitation than do patients in the Above-Average tier regardless of overlap between diagnostic categories.
Furthermore, persistence of the tier-unit association after controlling for diagnosis suggests that rehabilitation services may already be routing patients in part by impairment level.
Making this stratification explicit would allow decisions about triage to be audited and improved [@corrigan2010epidemiology]

## Feature Engineering

### _source:_ `report/Chapters_short/Chapter5.tex`

H4 indicates that domain-aggregate features are much better conditioned than variable-level features even though separation between clusters increases very little.
The silhouette changes only somewhat (from .47 to .48), however mean vif decreases from 2.78 to 1.88 and condition number decrease from 61.73 to 11.79 (see §sec:h4_results).
If several highly correlated tests enter into an unstandardized composite then UMAP and HDBSCAN can exaggerate distance computation using a common cognitive dimension.
Aggregation provides one feature per construct so each domain contributes equally.
These findings provide quantitative evidence supporting the practice of interpreting test batteries by domain rather than testing by testing [@lezak2012neuropsychological].
Importantly this advantage depends upon preprocessing conditions: variables must first be winsorized direction-aligned standardized before they can be aggregated otherwise raw scale differences will dominate the composites.

## feature importance and how it relates to severity

### _source:_ `report/Chapters_short/Chapter5.tex`

Findings presented in section §sec:feature_importance should be viewed as descriptive rather than explanatory.
Random Forest surrogate achieves 99.4% accuracy using same domain scores that generated labels; therefore ranking mainly recovers partition boundaries.
Random Forest ranked orientation visuo-perceptual abilities language above attention executive function; however this ordering should not be given strong interpretation.
Domains are extremely correlated which makes Gini importance susceptible to variability under correlated predictors [@boulesteix2012overview].

More reliable finding related to principal component structure is that one component explained 56% of total variance in overall cognitive severity; loads positively of similar magnitude across all six domains.
Tiers represent general severity levels rather than domain specific dissociations or an attention specific pattern.
Robustness checks presented in §sec:robustness including subsampling and evaluating sensitivity to amount of missing data support conclusion that severity ordering remains stable but exact tier count is dependent upon resolution clustering criteria inclusion threshold.
Data-driven studies examining phenotyping should report clearly choices made during preprocessing steps and include sensitivity analyses