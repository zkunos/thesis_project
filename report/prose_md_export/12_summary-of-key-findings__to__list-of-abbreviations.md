<!-- Exported prose chunk 12. Word count: 1058. -->


## Summary of Key Findings

_Source: `report/Chapters_short/Chapter7.tex`_

The primary aim of this research was to determine whether data-driven clustering of neuropsychological assessments can recover a cognitive structure in acquired brain injury that is robust, interpretable, and clinically meaningful. Four hypotheses were evaluated with a pipeline combining UMAP dimensionality reduction, HDBSCAN density-based clustering, and multiple imputation methods for incomplete clinical data.

The main conclusion is that the recovered structure is a cognitive severity gradient, not a set of separate phenotypes. The cohort lies along one axis of overall severity. The first principal component explains 56% of the variance across the six cognitive domains, with nearly equal positive loadings. The pipeline discretises this gradient into three tiers: Above-Average (38.6%, n = 6{,}725), Near-Normal (36.4%, n = 6{,}328), and Global Impairment (25.0%, n = 4{,}353). Level separates the tiers. Shape does not.

Hypothesis 1 is supported, with an important qualification. The pipeline identifies stable groups, but those groups are best interpreted as severity bands. All ten imputation methods meet the pre-registered silhouette and noise criteria, and the two outer tiers remain reasonably stable under Hennig per-cluster matching (core Jaccard 0.63 and 0.62 respectively; §sec:h1_results).

Hypothesis 2 is also supported. Under a shared pipeline, the mean Adjusted Rand Index across all 45 pairwise method comparisons is 0.710 (95% bootstrap CI ), above the 0.50 threshold. After Holm-Bonferroni correction, 44 of the 45 pairs reject H_0: ARI le 0.5 at alpha = 0.05; KNN-SoftImpute is the only borderline case. Consensus clustering reaches a mean confidence of 0.929, with 86.2 per cent of assessments assigned high-confidence labels. The listwise-deletion baseline confirms that imputation is analytically necessary: removing the 46.9 per cent of assessments with missing values changes the cluster count and lowers the silhouette to 0.257.

Hypothesis 3 is supported as well. Clinical unit is significantly associated with cognitive severity tier (chi^2 = 911.3, p approx 4 times 10^{-156}), although the effect size is modest (Cramér's V = 0.162). The Cochran-Mantel-Haenszel test indicates that the association is not explained by diagnosis group alone [@cochran1954some]. Cognitive severity therefore contributes to unit placement beyond diagnostic category.

Finally, Hypothesis 4 is supported. Domain-level aggregation produces cluster separation comparable to variable-level features (silhouette 0.481 vs. 0.473), while reducing multicollinearity (mean VIF 1.88 vs. 2.77) and improving numerical conditioning (11.8 vs. 61.7). This provides quantitative support for interpreting cognitive performance at the domain level.



## Methodological Contribution

_Source: `report/Chapters_short/Chapter7.tex`_

This thesis makes two methodological contributions. First, it provides an imputation-robustness framework. Pairwise ARI and NMI comparisons, combined with consensus confidence scores, offer a structured way to test whether clustering results depend on the missing-data method. Because the framework is domain-agnostic, it can be transferred to other incomplete clinical or biomedical datasets, including electronic health records, genomics, or survey data.

Second, it provides a methodological caution. Unsupervised cognitive phenotyping is highly sensitive to feature engineering. A demographic variable included by mistake, a record without cognitive test data, or variables aggregated across incompatible raw scales can create an apparent phenotype that is actually a preprocessing artefact. The pipeline reduces this risk by excluding non-cognitive variables, requiring at least one cognitive measure per record, and winsorising, direction-aligning, and standardising every variable before aggregation. Clinical labels should be assigned only after this preprocessing and sensitivity checking have been completed.



## Clinical Recommendations

_Source: `report/Chapters_short/Chapter7.tex`_

In light of these findings, I offer the following recommendations:

- Pair diagnosis with a battery-wide severity summary. A severity tier provides a reproducible description of overall cognitive impairment for a given visit, including imputed values for tests that were not completed. Rehabilitation teams can use this alongside diagnosis to calibrate treatment intensity to need.

- Flag boundary assessments rather than hiding uncertainty. Consensus clustering assigns 86.2% of assessments high-confidence labels, but about 2{,}400 assessments are sensitive to the imputation method and lie near a tier boundary. Decision-support tools should report confidence scores rather than forcing all labels to appear equally certain.

- Prefer model-based imputation for operational use. MICE, EM, MissForest, and the autoencoder methods produce broadly similar results, with pairwise ARI values as high as 0.88. KNN is more idiosyncratic, and Mean Imputation loses variance. MICE is a sensible operational default, while MissForest is a useful non-parametric option when non-linear relationships are expected.

- Define rehabilitation goals at the domain level. Domain aggregation gives clustering performance comparable to individual variables while reducing multicollinearity. This supports the established neuropsychological practice of interpreting batteries by cognitive domain [@lezak2012neuropsychological]. Progress monitoring and treatment plans should follow the same structure.



## Final Remarks

_Source: `report/Chapters_short/Chapter7.tex`_

When applied with careful attention to scaling and data structure, unsupervised clustering recovers a cognitive severity gradient in ABI that is robust across imputation methods and diagnostic groups and interpretable at the domain level. In this cohort, the recovered structure reflects overall cognitive severity rather than dissociable phenotypes.

Prospective validation is required before this framework can be integrated into routine care:

- Can a severity tier or score predict functional outcomes - such as return to work or length of stay - better than diagnosis and current scales?

- Will allocating resources based on severity make a difference in a controlled setting, or is it merely formalising the findings of the CMH analysis?

- Will the one-dimensional structure I see here persist in an independent multi-centre cohort, or will the granularity shift with the catchment and timing of the assessment?

The pipeline and dashboard are designed to support that next phase. During validation, a new cohort can be processed through the same MICE, UMAP, and HDBSCAN pipeline so that CogDash returns a tier and consensus-confidence score for each patient. Until prospective validation is complete, severity stratification should be treated as a decision-support signal, not as a substitute for clinical judgement.



# Imputation Hyperparameters

_Source: `report/Appendices/AppendixA.tex`_

This appendix lists the hyperparameters used for each of the ten imputation methods evaluated in this thesis. Settings followed published defaults where defaults exist; remaining choices were selected by cross-validation or grid search as noted. The methods themselves are described in Chapter Chapter3, §sec:imputation.

Caption: Hyperparameters for the ten imputation methods.



# List of Abbreviations

_Source: `report/Appendices/AppendixB.tex`_

The abbreviations and acronyms used throughout this thesis are listed below.

---REWORK
## Summary of Key Findings

_Source: `report/Chapters_short/Chapter7.tex`

The purpose of this study was to find out if data-driven clustering of neuropsychological testing could show a cognitive pattern in acquired brain injury (ABI) that would be reliable, understandable and useful to clinicians. Four hypotheses were tested using a pipeline that consisted of UMAP dimensionality reduction, HDBSCAN density-based clustering, and multiple imputation methods for missing clinical data.

Overall, the major finding of this research was that the cognitive structure found through the clustering process represents a cognitive severity gradient, not a distinct number of phenotypes. The cohort represents a single dimension of overall cognitive severity. The first principle component accounts for approximately 56% of the total variability among the six cognitive domains, with almost identical positive weights. The pipeline takes this continuum and divides it into three tiers: Above Average (38.6%, n=6725), Near Normal (36.4%, n=6328), and Globally Impaired (25.0%, n=4353). The Level determines which tier a participant falls into. However, there is no evidence that shape affects this outcome.

Hypothesis 1 is supported with an important caveat. There are identifiable clusters that are relatively stable. However, these are best viewed as severity bands. Each of the ten imputation methods meets the pre-specified silhouette and noise thresholds, and the two extreme tiers remained fairly consistent under Hennig per-cluster matching (Core Jaccard 0.63 and 0.62, respectively; §sec:h1_results).

Hypothesis 2 is also supported. Using a common pipeline, the average Adjusted Rand Index across all forty-five pairwise method comparisons is .710 (95% bootstrap CI [.695,.724]), greater than the .500 threshold. Following Holm-Bonferroni adjustment, forty-four of fifty-five pair-wise combinations reject H_0: ARI ≤ .5 at α = .05. Only KNN-SoftImpute is borderline. Consensus clustering achieves a mean confidence of .929, with 86.2 percent of assessments receiving high-confidence assignment. The baseline comparison with listwise deletion verifies that imputation is analytically required: Removing missing values from 46.9 percent of the assessments alters the number of clusters and lowers the silhouette value to .257.

Hypothesis 3 is supported as well. Clinical Unit is significantly correlated with cognitive severity tier (χ^2 = 911.3, p ≈ 4 × 10^(-156)), however, the magnitude of the correlation is small (Cramér’s V = .162). The Cochran-Mantel-Haenszel statistic demonstrates that clinical unit is not solely determined by diagnosis group [@cochran1954some]. Thus, cognitive severity appears to contribute to clinical unit designation independently of diagnostic category.

Lastly, Hypothesis 4 is supported. Variable-level aggregation generates cluster separation equivalent to that produced by domain-level aggregation (silhouette .481 vs .473), and variable-level aggregation also decreases multivariate collinearity (mean VIF 1.88 vs 2.77) and increases numerical stability (11.8 vs 61.7). These results provide empirical support for conceptualizing cognitive performance at the domain level.

## Methodological Contribution

_Source: `report/Chapters_short/Chapter7.tex`_

There are two methodological contributions made within this dissertation. First, an imputation-robustness framework is presented. The combination of ARI/NMI comparison, and consensus confidence measures provide a systematic means to evaluate whether differences in clustering result arise due to differing missing-value algorithms. Due to its domain agnostic nature, the framework may be employed with other types of partially observed clinical or biomedical data including genomic data or survey responses.

Second, a cautionary note is provided regarding feature engineering. As demonstrated in this dissertation, unsupervised cognitive phenotyping is very susceptible to how features are constructed. For example, inclusion of an unintended demographic variable or failure to include any cognitive test information in the assessment record can create an artifact representing what appears to be a phenotypic grouping that in reality arises from poor construction of features. The pipeline developed in this dissertation reduces this potential source of error by excluding non-cognitive variables, ensuring that at least one cognitive variable exists for each assessment record, and performing Winsorisation, direction-alignment, and standardization on each variable prior to aggregation. Clinical labeling should occur only after these processing steps have taken place and evaluation for sensitivity.

## Clinical Recommendations

_Source: `report/Chapters_short/Chapter7.tex`_

Based upon these findings, I recommend the following:

- Use a global severity index to supplement a diagnosis. The global severity index provides a reproducible summary description of overall cognitive function at time of assessment, regardless of the type of assessment (including imputed values for uncompleted tests). Rehabilitation teams can use both the diagnosis and a global severity index to inform their determination of appropriate treatment intensity for each patient.

- Label uncertain cases instead of discarding them. Consensus clustering provides high confidence labels for 86.2 percent of assessments but about 2400 assessments lie close to a tier boundary and thus will vary depending on choice of algorithm. Decision-support systems should report the confidence with which labels were generated instead of artificially confining label certainty uniformly.

- Choose model-based imputation for practical use. Although MICE, EM, MissForest, and autoencoder imputation produce similarly robust results (pairwise ARI values as large as .88) compared to each other, KNN tends to behave differently from the others and Mean Imputation loses variance relative to the others. Therefore, MICE seems like a reasonable choice for practical application purposes whereas MissForest may prove useful for nonparametric modeling applications where nonlinear relationships are expected.

- Develop treatment objectives at the domain level. Clustering at the domain level produces separations among clusters similar to variable-level aggregation while simultaneously reducing multivariate collinearity (mean VIF 1.88 vs 2.77) and increasing numerical conditionability (11.8 vs 61.7). This lends further support to the long-established neuropsychological practice of evaluating batteries according to domain of cognitive functioning [@lezak2012neuropsychological].

## Conclusion

_Source: `report/Chapters_short/Chapter7.tex`_

Using a dimensional reduction technique called UMAP and clustering technique called HDBSCAN on reduced data with imputation algorithms that handle missing values, this study demonstrates that unsupervised clustering can uncover a continuous cognitive severity gradient in ABI that is robust to different imputation strategies and clinical groups and interpretable at the domain level. Furthermore, this research shows that there are no separate phenotypes in this cohort but rather a single dimension of overall cognitive severity.

Therefore, this dissertation provides empirical support for developing rehabilitation planning guidelines using severity levels for patients who have suffered an acquired brain injury. Future studies will be needed to validate the usefulness of using cognitive severity levels for rehabilitation planning purposes:

- Does cognitive severity levels predict future outcomes better than diagnosis and current measures?

- Would using a severity system improve resource allocation in controlled environments or is it just a formalization of what was discovered in CMH analyses?

- Are there additional subgroups present in independent cohorts across multiple centers that were not evident in this sample or do they emerge due to varying characteristics of the populations sampled and/or assessment times?

