<!-- Exported prose chunk 6. Word count: 1381. -->


## Hypothesis Definitions

_Source: `report/Chapters_short/Chapter3.tex`_

noindent H1 (Existence of Cognitive Clusters). The UMAP + HDBSCAN pipeline is expected to identify at least two separate, stable cognitive clusters for most imputation methods. H1 is supported if the best solution from at least eight of the ten methods satisfies both criteria: mean silhouette ge 0.40, indicating adequate separation and cohesion, and noise proportion < 0.30, indicating that most observations are assigned to substantive clusters. The 80% criterion allows limited method-specific failure without rejecting the overall hypothesis.

noindent H2 (Robustness Across Imputation Methods). Cluster solutions should show moderate to high agreement across imputation methods. H2 is supported if the median pairwise ARI and NMI across all binom{10}{2} = 45 method pairs exceed 0.50. This threshold is above chance and indicates substantial membership overlap, without requiring exact identity across solutions.

noindent H3 (Association with Clinical Unit). Cluster membership is expected to be associated with clinical unit. For each imputation method, a contingency table is constructed and a chi-square test of independence is applied. H3 is supported if the association remains significant at alpha = 0.05 after Bonferroni correction and Cramér's V exceeds 0.10. A Cochran-Mantel-Haenszel (CMH) test, stratified by an appropriate covariate, is used as a sensitivity check for confounding.

noindent H4 (Domain-Level vs. Variable-Level Clustering). I expect domain-level features to produce a clustering representation that is easier to interpret and at least as well separated as the variable-level representation. H4 is considered supported if the domain-level approach outperforms the variable-level approach on at least two of three measures: a higher silhouette score, a lower mean variance inflation factor (VIF), and a lower condition number. Lower VIF and condition number values indicate less multicollinearity and better numerical conditioning. Cross-method agreement is not used for H4 because it is already evaluated under H2; this comparison focuses only on feature representation.



### Statistical Conventions

_Source: `report/Chapters_short/Chapter3.tex`_

The inferential analysis follows standard statistical practice. Each test evaluates the data against a null hypothesis (H_0), which represents the no-effect baseline. The p-value is the probability of observing a test statistic as extreme as the one obtained, assuming H_0 is true; smaller values provide stronger evidence against H_0. A significance level of alpha = 0.05 is pre-registered as the rejection threshold. For any parameter, a 95% confidence interval represents the range that would contain the true value in 95% of repeated samples under the same procedure.

When bootstrap methods are used, the observed data are resampled with replacement to approximate the sampling distribution of a statistic. The 2.5th and 97.5th percentiles of that empirical distribution form the bootstrap confidence interval. A z-score expresses a value in standard deviations from the mean of a reference distribution. For the neuropsychological tests used here, standardisation against normative populations allows scores to be compared across instruments.

Effect sizes follow Cohen's conventions. The standardised mean difference, Cohen's d, is calculated as with s_p being the pooled standard deviation. By this measure, d=0.2 is small, 0.5 medium, and 0.8 large. In the case of Cramér's V as an effect size for chi-squared tests (Eq. eq:cramersv), V = 0.10 is taken as small, 0.30 as medium, and 0.50 as large.



### Tests and Validation Procedures

_Source: `report/Chapters_short/Chapter3.tex`_

noindent Bootstrap stability. I run a bootstrap stability analysis for every imputation method, using 50 resamples each. For each resample, HDBSCAN is re-fitted on the cached UMAP embedding, and the median silhouette (Eq. eq:silhouette) and pre-KNN noise proportion are recorded. The noise proportion is the share of observations that HDBSCAN does not assign to a substantive cluster: This is also the value used in the selection score Q (Eq. eq:quality). Under H1's pre-registered rules, a method passes if its median silhouette is above 0.40 and its pre-KNN noise is below 0.30; at least eight of the ten methods must pass. For per-cluster stability, Hennig (2007) matching is applied to the pre-KNN labels using the conventional 0.7 threshold.

noindent Pairwise agreement. To isolate the effect of imputed values from other sources of pipeline variability, I use a shared pipeline. A single StandardScaler, UMAP model, and k-means model are fitted on the MICE-imputed domain scores. The remaining methods are then standardised, projected, and classified using those same MICE-fitted components. This produces the 10 times 10 ARI (Eq. eq:ari) and NMI (Eq. eq:nmi) matrices shown as heatmaps in Chapter Chapter4. Consensus confidence for an assessment is the proportion of the M=10 methods that assign it to the modal cluster: and an assessment counts as high-confidence once mathrm{conf}(i)ge 0.8.

noindent textbf{Chi-squared, Cramér's V, and CMH.} Cross-tabulating two categorical variables, such as cluster label and clinical unit, gives a contingency table of joint counts. Pearson's chi-squared test compares the observed counts O_{ij} with the expected counts E_{ij} under the null hypothesis of independence: with O_{icdot} and O_{cdot j} being the row and column totals. The statistic is referred to a chi-squared distribution on (r-1)(c-1) degrees of freedom to obtain the p-value. To make the association sample-size invariant, Cramér's V is used, a value between 0 and 1. The Cochran-Mantel-Haenszel test is an extension of this for data in strata (here, diagnosis groups, h=1,dots,K). It indicates whether the cluster-unit link holds up after stratifying, where for the 2times2 table in stratum h having total n_h, mathbb{E}=(a_h+b_h)(a_h+c_h)/n_h and operatorname{Var}(a_h)=(a_h+b_h)(c_h+d_h)(a_h+c_h)(b_h+d_h)/. If both the unadjusted chi-squared and the CMH come back significant, the association cannot be put down to the stratifying variable.

noindent Variance inflation factor. To measure multicollinearity, VIF is used. For any variable j it is R_j^2 being the coefficient of determination when regressing j on the rest. Anything in excess of 10 is cause for concern and serves to guide the interpretation at the variable level and the domain-level analysis that follows.



## Exploratory Data Analysis

_Source: `report/Chapters_short/Chapter4.tex`_

After Tier 1 filtering (Chapter Chapter3) and exclusion of assessments without any cognitive test, the final dataset comprised 17{,}406 assessments from 7{,}285 patients. The retained matrix contained 14 cognitive variables spanning 6 domains. Missingness rates are reported in Table tab:missing_descriptive.

Caption: Missingness summary for the 14 eligible neuropsychological variables after Tier 1 filtering. The final row reports the number of complete cases (rows with no missing values across all 14 variables).

Data availability is uneven. Missingness ranges from 0.7% for orientation items to 27.8% for ATMTA. Only 9{,}245 of 17{,}406 records contain all 14 variables, so complete-case analysis would exclude 46.9% of the dataset and create a clear risk of selection bias [@rubin1976inference]. Imputation was therefore used to preserve the full clinical sample.

Figure fig:missingness_barplot shows the per-variable missingness rates. More specialised assessments consistently exhibit higher missingness; this reflects standard clinical practice, in which test batteries are tailored to the patient's functional status [@lezak2012neuropsychological].

Caption: Proportion of missing values for each cognitive variable, ordered by missingness rate. Specialised assessments show higher missingness than the routinely administered screening measures.

A co-occurrence heatmap (not shown) reveals blocks of variables that are absent together, a pattern consistent with a missing-at-random mechanism [@rubin1976inference, little2019statistical]. Such dependency favours conditional imputation over naive substitution. Among observed values, within-domain correlations are strong and cross-domain associations are more modest, probably reflecting shared variance with general cognitive ability [@lezak2012neuropsychological]. The clustering results later make this shared severity dimension explicit.



## Imputation Results

_Source: `report/Chapters_short/Chapter4.tex`_

To prepare the datasets for downstream clustering, I evaluated all ten imputation methods, shown in Figures fig:imputation_comparison and fig:imputation_comparison_b. Mean Imputation behaves differently from the other methods because, as expected for single-value imputation, it compresses variance [@rubin1987multiple]. The remaining nine methods preserve the marginal distributions more closely. Donor-based methods such as KNN and PMM retain more discrete structure, while model-based approaches such as MICE, MissForest, and EM produce smoother continuous reconstructions.

Caption: Distribution comparison across ten imputation methods for ATMTA and VPIMATGES. Mean Imputation compresses variance; model-based methods preserve distributional shape.

Caption: Distribution comparison for MRAVLT015R and MRAVLT015. Deep learning methods (DAE, VAE) closely match model-based methods.

---REWORK

Hypothesis Definition 
Source: report/Chapters_short/Chapter3.tex

noindent H1 (Existence of Cognitive Clusters) . The UMAP + HDBSCAN pipeline will likely find at least two distinct , stable cognitive clusters for most imputation techniques . The existence of these clusters can be demonstrated as long as the best solution from at least 8 of the 10 different methods have both characteristics : average silhouette ≥ 0.40 , and the percentage of noisy points < 0.30 . Since we allow some method-specific failures , the 80% criterion provides a margin for error .

noindent H2 (Robustness Across Imputation Techniques ) . Solutions for the clustering problems should show reasonable to high agreement among the imputation methods . H2 is confirmed if the median pair-wise ARI and NMI for each of the {10 \choose 2 } = 45 combinations of methods exceeds 0.50 . Although there is considerable flexibility in setting this threshold , it is greater than chance and implies a substantial overlap in group membership , regardless of the degree to which individual solutions are identical .

noindent H3 (Relationship Between Clinical Unit & Cluster Membership ). Cluster membership is expected to be related to clinical unit . For each imputation technique , a contingency table is created and a chi-square test of independence is conducted . H3 is confirmed if the relationship remains statistically significant at α = 0.05 after a Bonferroni adjustment and Cramér’s V > 0.10 . As a sensitivity check for potential confounds , a Cochran-Mantel-Haenszel (CMH) test is performed, conditioned on an appropriate covariate .

noindent H4 (Clustering at Domain-Level vs. At Variable Level ). I expect the cognitive features at the domain-level to result in a clustering representation that is more interpretable and at least as well-separated as the representation based on cognitive features at the variable-level . H4 will be confirmed if the domain-level approach performs at least as well as or better than the variable-level approach on at least two of three metrics : (1) higher silhouette scores ; (2) lower mean VIFs ; and (3) lower condition numbers . Smaller values of VIF and condition number imply less multicollinearity and better numerical conditioning . Because cross-method agreement has already been assessed in H2 , comparisons of feature representations are made in H4 exclusively .

Statistical Conventions 
Source: report/Chapters_short/Chapter3.tex

Each statistical evaluation of hypotheses follows typical statistical practice . Each evaluation assesses the data relative to a null hypothesis (H0), representing a "no-effect" baseline. The p-value is the probability of obtaining a test statistic as extreme as that obtained assuming H0 to be true; smaller p-values represent stronger evidence against H0. A predetermined significance level of alpha = 0.05 serves as the threshold for rejecting H0. For any parameter, a 95% CI represents the range that would include the population parameter in 95% of repeated random samples from the same population using the same methodology.

For applications of bootstrapping, observed data are randomly sampled with replacement to generate a simulated approximation of the sampling distribution of a statistic. The 2.5th and 97.5th percentiles of that simulated distribution define the bootstrap CI. A z-score quantifies how many standard deviations away from the mean of a specified reference distribution a given value lies. With respect to the psychological testing instruments employed here, standardized testing permits scores derived from different instruments to be compared.

Cohen defined standards for interpreting the magnitude of effects, specifically for standardized differences, i.e., Cohen’s d. Specifically, d = 0.20 is interpreted as a small effect size, d = 0.50 as a medium-sized effect, and d = 0.80 as a large effect size. When applying Cramér’s V as an effect size for evaluating chi-squared tests (Equation eq:cramersv), V = 0.10 is interpreted as a small effect size, V = 0.30 as a medium effect size, and V = 0.50 as a large effect size.

Tests and Validation Procedures 
Source: report/Chapters_short/Chapter3.tex

noindent Bootstrap Stability . I conduct a bootstrap stability analysis for every imputation method using B = 50 resamplings. For each resampling, I refit HDBSCAN on the cached UMAP embeddings, recording the median silhouette (Equation eq:silhouette) and pre-KNN noise proportions. Pre-KNN noise proportion is equal to the proportion of observations that do not belong to any meaningful cluster : this is also the value used in defining quality function Q (Equation eq:quality). According to H1’s pre-defined conditions, a method will be deemed successful if its median silhouette is larger than or equal to 0.40 and its pre-KNN noise proportion is less than or equal to 0.30 ; at least 8 of the 10 methods will need to satisfy both conditions. To evaluate per-cluster stability, I apply Hennig (2007)’s matching algorithm to the pre-KNN labels using the default threshold (i.e., 0.7).

noindent Pair-Wise Agreement . In order to remove imputation-induced variability caused by variations in other parts of pipelines, I employ a shared pipeline strategy. One StandardScaler, one UMAP model, and one k-means model are trained on MICE-imputed domain scores. The remaining methods are then standardized, projected onto this MICE-trained pipeline, and classified using that same MICE-trained pipeline. This creates the ARI (Equation eq:ari) and NMI (Equation eq:nmi) matrices comparing each method to each other shown as heatmaps in Chapter Chapter4. High-confidence assessments are those whose assessments were placed into the mode cluster by at least M/10 = 0.8*10 = 8 methods.

noindent Chi-Square Test , Cramér’s V, CMH Test . Contingency tables arise from cross-classifying two categorical variables — e.g., cluster assignment and clinical unit — giving joint counts. Pearson’s Chi-Square Test evaluates observed counts O_{ij} against expected counts E_{ij} under the null hypothesis that the two variables are independent: with O_{icdot}, O_{cdot j}, etc., denoting row sums and column sums, respectively. The test statistic is referenced against a Chi-Square distribution with (r − 1)(c − 1) degrees of freedom to yield the p-value. Cramér’s V is used to render association statistics scale-free for sample-size purposes, since it takes on values between zero and one. The Cochran-Mantel-Haenszel Test extends Pearson’s Chi-Square Test for data organized into strata (e.g., diagnosis subgroups). The CMH Test determines whether the association between cluster assignments and clinical units remains significant even when stratifying by an appropriate covariate.

noindent Variance Inflation Factor . To quantify multicolliinearity in regression models , VIF is used. For any variable j, it is Rj^2 , where Rj^2 denotes the coefficient of determination when regressing j on all other predictors. Any value exceeding 10 constitutes grounds for concern, and influences interpretation both at the variable level and in subsequent analyses at the domain level.

## Exploratory Data Analysis 
Source: report/Chapters_short/Chapter4.tex

Following Tier-1 filtering (Chapter Chapter3) and removal of all assessments lacking any cognitive measures , the remaining dataset consisted of 17{,}406 assessments from 7{,}285 patients. The resulting matrix included cognitive variables amounting to 14 variables over six domains. The percentages of missing values are provided in Table tab:missing_descriptive.

Caption: Summary statistics for missingness of neuropsychological variables available after Tier-1 filtering. The bottom row lists the number of completely observed assessments (assessments containing all 14 variables).

Data availability is inconsistent. The missingness levels vary from 0.7 % for Orientation items through to 27.8 % for ATMTA. Therefore, complete-case analysis would lose approximately half of the total clinical sample (46.9%) and introduce clear selection bias [ @ rubin1976inference ]. Consequently, data imputation was adopted to conserve the entire clinical sample.

In Figure fig:missingness_barplot , missingness levels for each cognitive variable are displayed in descending order. Highly specialized assessments consistently demonstrate higher levels of missingness than routine screening measures [ @ lezak2012neuropsychological ].

Caption: Proportions of missing values for each cognitive variable listed according to increasing missingness level. Higher missingness levels are generally found for highly specialized assessments compared to routine screening measures.

From a co-occurrence heatmap (not shown), blocks of variables are identified that are missing simultaneously, suggesting a missing-at-random mechanism [ @ rubin1976inference , @ little2019statistical ]. Dependency among missing values thus supports the application of conditional imputation rather than naive substitution. Within-domain correlation coefficients are generally high, whereas cross-domain relationships appear less prominent, suggesting common variance due to general cognitive ability [ @ lezak2012neuropsychological ]. Subsequent clustering results illustrate this common variance dimension explicitly.

## Imputation Results 
Source: report/Chapters_short/Chapter4.tex

Prior to conducting clustering evaluations on their respective datasets , I tested all ten imputation techniques represented in Figures fig:imputation_comparison and fig:imputation_comparison_b. Due to compression of variance [ @ rubin1987multiple ], Mean Imputation behaves differently from all other methods. All nine remaining methods maintain closer adherence to marginal distributions. Discrete structure retention is greater among donor-based methods like KNN and PMM than among model-based approaches including MICE, MissForest and EM that produce smoothed continuous reconstructions.

Caption: Distribution comparison across ten imputation methods for ATMTA and VPIMATGES. Model-based methods retain distributional shape much more than Mean Imputation does.

Caption: Distribution comparison for MRAVLT015R and MRAVLT015. Deep learning methods (DAE,V AE) reproduce model-based methods very accurately
