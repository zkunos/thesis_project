# Thesis Defense Study Cards

Data-Driven Cognitive Phenotyping in Acquired Brain Injury  
20-minute defense rehearsal cards

## How To Use These Cards

Use each card as a prompt, not as a script. Aim to answer each "Front" from memory in 20-40 seconds, then check the "Back". For the examiner cards, practice giving a calm two-part answer: first the direct answer, then the methodological reason.

## Core Message Cards

### Card 1. One-Sentence Thesis

**Front:** What is the thesis in one sentence?

**Back:** In incomplete routine neuropsychological datasets after acquired brain injury, unsupervised learning identifies a robust cognitive severity gradient rather than a hidden structure of sharply separated cognitive subtypes.

### Card 2. Main Contribution

**Front:** What is the main contribution of the dissertation?

**Back:** I combine missingness-aware imputation, domain-level aggregation, UMAP, HDBSCAN, and sensitivity testing to show that routine clinical neuropsychological data can support clinically interpretable severity stratification.

### Card 3. Conservative Interpretation

**Front:** What is the safest interpretation of the clusters?

**Back:** They are ordered severity tiers, not natural kinds. The tiers are useful bands along a cognitive severity continuum.

### Card 4. Why Missingness Matters

**Front:** Why is missingness central to the thesis?

**Back:** Missingness is clinically structured. It can reflect fatigue, impairment, test tolerance, clinician judgement, or practical assessment limits. Removing incomplete rows would discard many clinically important assessments.

## Slide Cards

### Card 5. Slide 1 - Opening

**Front:** What should Slide 1 establish?

**Back:** The dissertation asks whether routine neuropsychological data can reveal reliable cognitive organization after ABI. The answer is yes, but the main structure is a severity gradient, not sharp subtype separation.

**Key phrase:** "The strongest signal is cognitive severity."

### Card 6. Slide 2 - Thesis In One Sentence

**Front:** What are the three ideas inside the thesis sentence?

**Back:** Diagnosis does not fully explain cognitive variability. Missingness must be handled because it is clinically meaningful. The recovered tiers remain robust across imputation strategies.

### Card 7. Slide 3 - Clinical Problem

**Front:** Why is ABI difficult to classify cognitively?

**Back:** ABI affects multiple domains, including attention, memory, language, executive function, visuospatial perception, and orientation. Patients with the same diagnosis can have different rehabilitation needs.

### Card 8. Slide 3 - Research Question

**Front:** What is the research question?

**Back:** Can data-driven clustering produce clinically meaningful cognitive organization, and can that organization be trusted when missing data are managed rather than ignored?

### Card 9. Slide 4 - H1

**Front:** What does H1 test?

**Back:** H1 tests whether discrete and stable clusters can be recovered. Criteria include silhouette greater than 0.40, less than 30% noise, and at least two clusters for most imputation methods.

### Card 10. Slide 4 - H2

**Front:** What does H2 test?

**Back:** H2 tests robustness to imputation using mean pairwise adjusted Rand index greater than 0.50. It uses a fixed-reference design, so it tests whether imputed points land similarly under a fixed embedding and partition.

### Card 11. Slide 4 - H3

**Front:** What does H3 test?

**Back:** H3 tests whether the cognitive severity tiers are clinically relevant by examining their association with clinical unit assignment, using chi-square statistics, Cramer's V, and diagnosis-adjusted analysis.

### Card 12. Slide 4 - H4

**Front:** What does H4 test?

**Back:** H4 tests whether domain-level aggregation improves the analysis compared with using all individual neuropsychological variables.

### Card 13. Slide 5 - Cohort Numbers

**Front:** What are the key cohort numbers?

**Back:** 17,406 assessments, 7,285 patients, fourteen neuropsychological variables, six cognitive domains, and 53.1% complete rows.

### Card 14. Slide 5 - Why Complete Cases Are Not Enough

**Front:** Why not use only complete cases?

**Back:** Complete-case analysis would discard about 46.9% of assessments. That is not just loss of power; it can change which patients are represented.

### Card 15. Slide 6 - Missingness Mechanism

**Front:** How should missingness be described?

**Back:** Missingness reflects the clinical testing process rather than random administrative failure. It can indicate fatigue, disorientation, motor limitations, low tolerance, or clinician judgement.

### Card 16. Slide 7 - Pipeline

**Front:** What is the analysis pipeline?

**Back:** Impute missing data, scale scores, aggregate into six domains, embed with UMAP, cluster with HDBSCAN, and evaluate separation and noise.

### Card 17. Slide 7 - H2 Fixed Reference

**Front:** What is the fixed-reference design?

**Back:** MICE defines the anchor scaler, UMAP embedding, and HDBSCAN cluster configuration. Other imputation methods are projected through that fixed structure to isolate the effect of imputed values.

### Card 18. Slide 8 - H1 Main Result

**Front:** What are the three recovered tiers?

**Back:** Above-Average, Near-Normal, and Global Impairment.

### Card 19. Slide 8 - Tier Sizes

**Front:** What are the tier sizes?

**Back:** Above-Average: 6,725 assessments. Near-Normal: 6,328 assessments. Global Impairment: 4,353 assessments.

### Card 20. Slide 8 - Interpretation Of Tiers

**Front:** Are the tiers discrete phenotypes?

**Back:** I do not interpret them as sharply separated phenotypes. I interpret them as ordered severity bands along a continuous cognitive axis.

### Card 21. Slide 9 - PCA Evidence

**Front:** What does the PCA show?

**Back:** The first principal component explains nearly 56% of variance, and all domains load positively. This supports a broad cognitive severity dimension.

### Card 22. Slide 9 - Severity Profile

**Front:** What is the strongest signal in the data?

**Back:** Global cognitive severity. The most prominent signal is not a symptom-specific dissociation or a catalogue of distinct subtypes.

### Card 23. Slide 10 - H2 Result

**Front:** What is the main H2 result?

**Back:** The mean pairwise ARI is .71, with a 95% bootstrap confidence interval of .70 to .72. This indicates substantial agreement across imputation methods under the fixed-reference design.

### Card 24. Slide 10 - H2 Caveat

**Front:** What is the important limitation of H2?

**Back:** H2 supports robustness of point assignments under a fixed embedding and partition. It does not prove that every independently refitted UMAP plus HDBSCAN pipeline recovers the same density hierarchy.

### Card 25. Slide 11 - Complete-Case Result

**Front:** What happens with complete-case analysis?

**Back:** Only 53.1% of assessments are retained. The complete-case baseline recovers two clusters rather than the desired three-tier solution, and its silhouette is lower, around .26 versus about .53 for the MICE reference.

### Card 26. Slide 12 - H3 Result

**Front:** What is the clinical association result?

**Back:** Tier membership is associated with clinical unit assignment. The chi-square statistic is 911, the p-value is on the order of 10^(-156), and Cramer's V is 0.16.

### Card 27. Slide 12 - Diagnosis Adjustment

**Front:** Does diagnosis explain the clinical-unit association?

**Back:** Not fully. The Cochran-Mantel-Haenszel test shows the association persists after controlling for diagnosis, so severity tier adds information beyond diagnosis.

### Card 28. Slide 13 - H4 Result

**Front:** Why use domain-level scores?

**Back:** Domain-level scores improve numerical stability and interpretability. Mean VIF decreases from about 2.80 to about 1.90, and the condition number improves from about 62 to about 12.

### Card 29. Slide 13 - Silhouette Difference

**Front:** How different is the silhouette for domains versus individual variables?

**Back:** The difference is small but favorable to domains: about .48 for domains versus .47 for individual variables.

### Card 30. Slide 14 - Four Hypotheses Summary

**Front:** How do the four hypotheses end?

**Back:** H1 is supported as severity tiers, H2 is supported within the fixed-reference design, H3 is supported through clinical-unit association, and H4 is supported through improved numerical properties of domain-level clustering.

### Card 31. Slide 15 - Interpretation

**Front:** What is the central interpretation?

**Back:** The data support a continuum of cognitive severity rather than a set of discrete cognitive subtypes.

### Card 32. Slide 15 - Subtype Caution

**Front:** Does the study prove that domain-specific dissociations do not exist?

**Back:** No. It shows that in this dataset and pipeline, the strongest recoverable signal is overall cognitive severity. Domain-specific dissociations may still exist in other designs or subgroups.

### Card 33. Slide 16 - Clinical Utility

**Front:** How can clinicians use the tiers?

**Back:** The tiers can support discussion of rehabilitation intensity and can be reported with confidence scores. They should supplement clinical judgement, not replace it.

### Card 34. Slide 16 - Analytic Utility

**Front:** How can researchers use the pipeline?

**Back:** Researchers can adapt it as a missingness-aware framework for studying relationships between cognitive severity and outcomes after acquired brain injury.

### Card 35. Slide 17 - CogDash

**Front:** What is CogDash?

**Back:** CogDash is a Streamlit dashboard that makes the analysis explorable through a cluster explorer, patient lookup, new-patient classifier, hypothesis summary, and advanced analytics tools.

### Card 36. Slide 17 - CogDash Boundary

**Front:** What should CogDash not be framed as?

**Back:** It should not be framed as an automated clinical decision-maker. It is a transparent decision-support and exploration tool.

### Card 37. Slide 18 - Limitations

**Front:** What are the main limitations?

**Back:** Single-site data, no full longitudinal recovery model, MAR assumptions for imputation, possible MNAR mechanisms, and no functional outcomes such as return to work or length of stay.

### Card 38. Slide 19 - Conclusion

**Front:** What are the three final conclusions?

**Back:** Routine ABI neuropsychological data contain a cognitive severity gradient. Imputation is a substantive modelling decision. Domain-level severity tiers are clinically interpretable and numerically stable.

### Card 39. Slide 20 - Closing

**Front:** What is the final message before questions?

**Back:** The analysis identifies something clinically useful but conservatively interpreted: an imputation-robust cognitive severity continuum after acquired brain injury rather than discrete cognitive subtypes.

## Examiner Question Cards

### Card 40. Why HDBSCAN?

**Front:** Why did you use HDBSCAN rather than k-means?

**Back:** HDBSCAN can identify dense regions and label noise without forcing every observation into a centroid. That matters in clinical data where borderline or atypical cases may not belong cleanly to a cluster.

### Card 41. Why UMAP?

**Front:** Why use UMAP before clustering?

**Back:** UMAP provides a nonlinear embedding that preserves local neighborhood structure while reducing dimensionality. It helps expose structure in domain-level cognitive data, but I treat UMAP-based silhouette cautiously because the embedding can exaggerate separation.

### Card 42. Is The Silhouette Optimistic?

**Front:** Is the reported silhouette possibly optimistic?

**Back:** Yes. Silhouette in UMAP space can be upward biased because UMAP is designed to emphasize neighborhood separation. I therefore interpret silhouette as an internal pipeline-quality statistic, not proof of natural categories.

### Card 43. Does H2 Prove Full Imputation Invariance?

**Front:** Does H2 prove the discovered structure is completely imputation-invariant?

**Back:** No. H2 tests whether point assignments are robust under a fixed embedding and partition. It does not claim that independently rerunning the full pipeline always recovers identical density hierarchies.

### Card 44. Why Not Complete-Case Analysis?

**Front:** Why is complete-case analysis not acceptable here?

**Back:** It removes nearly half of the analyzed assessments and may preferentially remove more impaired patients. In this study it also changes the recovered clustering structure.

### Card 45. Why Domain Aggregation?

**Front:** What is the argument for domain aggregation?

**Back:** Aggregation reduces redundancy, improves numerical conditioning, and creates clinically interpretable variables. It sacrifices some test-level detail, but the gain in stability and interpretability is valuable for this analysis.

### Card 46. What If Real Subtypes Exist?

**Front:** Could real cognitive subtypes still exist?

**Back:** Yes. The thesis does not rule them out. It shows that this dataset and pipeline primarily recover a severity gradient. More targeted designs may detect domain-specific dissociations.

### Card 47. What Does Clinical Relevance Mean Here?

**Front:** What does clinical relevance mean in H3?

**Back:** It means tier membership is statistically associated with clinical unit assignment and remains associated after diagnosis adjustment. It does not mean the model determines clinical placement.

### Card 48. What Is The Practical Output?

**Front:** What would a practical user get from this work?

**Back:** A severity tier, a confidence estimate, and interpretable domain-level information that can support rehabilitation discussion and research analysis.

### Card 49. What Is The Strongest Defense Of The Thesis?

**Front:** What is the strongest defense of the thesis?

**Back:** Multiple lines of evidence converge: stable tier recovery, PCA showing a broad severity dimension, imputation robustness under fixed reference, clinical-unit association, and better numerical properties from domain aggregation.

### Card 50. What Is The Most Important Caveat?

**Front:** What caveat should you be ready to say clearly?

**Back:** The clusters should not be overclaimed as discrete phenotypes. The strongest justified conclusion is severity stratification along a continuum.

## Rapid Number Drill

| Prompt | Answer |
|---|---:|
| Assessments analyzed | 17,406 |
| Patients | 7,285 |
| Neuropsychological variables | 14 |
| Cognitive domains | 6 |
| Complete rows | 53.1% |
| Incomplete rows | 46.9% |
| Above-Average tier | 6,725 |
| Near-Normal tier | 6,328 |
| Global Impairment tier | 4,353 |
| PC1 variance | nearly 56% |
| H2 mean ARI | .71 |
| H2 bootstrap CI | .70 to .72 |
| High-confidence consensus labels | over 86% |
| Complete-case silhouette | about .26 |
| MICE reference silhouette | about .53 |
| H3 chi-square | 911 |
| H3 Cramer's V | 0.16 |
| H4 domain silhouette | .48 |
| H4 variable silhouette | .47 |
| Mean VIF change | about 2.80 to 1.90 |
| Condition number change | about 62 to 12 |

## Final Rehearsal Mantra

The analysis does not claim to discover sharp cognitive subtypes. It supports a robust, clinically interpretable severity gradient that remains meaningful when missingness is handled explicitly.
