<!-- Exported prose chunk 11. Word count: 1377. -->


## Clinical Implications

_Source: `report/Chapters_short/Chapter5.tex`_

In clinical practice, a three-tier stratification of cognitive severity is more modest than a set of dissociable phenotypes, but it is still useful. Used alongside diagnosis, the tier provides a consistent summary of a patient's overall cognitive impairment across the battery, including imputed values for tests that were not completed and a confidence estimate for the assignment. Rehabilitation services can use this information to calibrate treatment intensity to need. The analysis suggests that this can be done reliably and that the tiers align with existing clinical placement.

The analysis does not support a novel attention-specific cognitive phenotype. The tiers reflect overall cognitive severity, not selective impairment or preservation of one domain. More broadly, unsupervised phenotyping depends heavily on feature engineering, and any striking profile should be tested against scaling, variable-selection, and cohort-definition choices before being given a clinical label. The main contribution of this thesis is a reproducible severity-stratification pipeline for incomplete routine clinical data. It provides a framework for handling missing neuropsychological assessments and creates a basis for future prospective validation against functional outcomes [@maas2017traumatic, corrigan2010epidemiology].



## Limitations

_Source: `report/Chapters_short/Chapter6.tex`_

Several limitations constrain the interpretation and generalisability of these results.

The most immediate limitation is the single-centre design. All data originate from one rehabilitation facility, so selection bias is possible and generalisation to other clinical populations cannot be assumed [@corrigan2010epidemiology]. The use of established neuropsychological tests, including Trail Making, digit span, Rey Auditory Verbal Learning, orientation, and language measures, partly mitigates this concern because these instruments have long clinical histories and international validation [@lezak2012neuropsychological]. The six cognitive domains also provide a standard framework for describing post-injury function. Multi-centre validation is nevertheless required before the severity structure can be interpreted as a general feature of ABI rather than a property of this service.

The structure recovered here is also a limitation on interpretation. The main finding is a continuum, not a set of natural categories. The cohort falls along a single overall-severity dimension, with PC1 explaining 56% of the variance, rather than into clearly dissociable profiles. The three tiers are useful as a discretisation of that gradient, but they should not be treated as phenotypes with hard boundaries. Tier count depends partly on clustering resolution: the primary MICE pipeline produces three, other imputation methods produce three to five, and the result shifts with the missingness threshold. Assessments near boundaries require caution. A continuous severity score may ultimately be more faithful than discrete bands (Section sec:future).

The analysis is also limited in its ability to model longitudinal change. ABI recovery is often fastest in the first months and then continues more slowly over years [@ponsford2014longitudinal, maas2017traumatic]. A single assessment captures only one point in that process. The dataset does include multiple assessments for many patients, which supports the within-patient analysis reported below, but the timing of follow-up is still clinically driven rather than standardised.

Among the 5{,}206 patients with longitudinal data (Section sec:robustness), the pattern is clinically plausible: 50.2% remain in the same tier, and among those who change tier, 706 move toward better function compared with 206 who move toward worse function. This 3:1 ratio matches the expected direction of recovery. However, it cannot fully separate genuine recovery from selection effects, such as patients being discharged once they improve. A future longitudinal design with harmonised assessment intervals is needed for that question.

The imputation strategy imposes additional constraints. The missing-at-random (MAR) assumption cannot be tested from observed data alone [@rubin1976inference, little2019statistical]. In clinical settings, a test may be incomplete precisely because the patient cannot finish it, so the missing value may be informative and may lie in the impaired range. If MNAR patterns of this kind were dominant, function could be overestimated. The conservative tipping-point check (Section sec:robustness) re-imputes every missing value to the worst observed performance. Under that extreme assumption, the Global Impairment tier persists and retains 65% of its members, although the finer partition degrades. A formal delta-shifted sensitivity analysis would refine this bound. The structured co-occurrence of missingness is somewhat reassuring because it points to test-battery protocols rather than purely outcome-based dropout. The comparison of 10 imputation methods also functions as a sensitivity analysis: 86.2% of assessments receive high-confidence consensus labels, suggesting that plausible imputation differences do not alter the main severity structure for most of the cohort.

A related caveat is the Tier-1 filter, which excludes assessments with more than half their values missing. On inspection (Section sec:robustness), excluded records completed only 0.8 of 14 tests on average and were demographically very similar to retained records. The filter therefore appears to remove near-empty administrative records rather than a hidden severe subgroup. Still, the cognitive severity of excluded records cannot be observed directly, and the 30-70% threshold sensitivity analysis only bounds the effect of this choice. Finally, the pipeline imputes and then clusters, rather than using a model-based alternative such as latent profile analysis with full-information maximum likelihood. The Gaussian-mixture baseline (Section sec:robustness) shows the Bayesian Information Criterion falling monotonically with the number of classes, supporting a continuum rather than a discrete optimum. A fuller FIML-based latent-profile analysis remains a worthwhile future extension.

Feature engineering remains consequential. Non-cognitive variables are excluded, and every variable is winsorised, direction-aligned, and standardised before aggregation so that no raw scale can dominate a composite and generate an artificial profile difference. The broader methodological lesson is direct: unsupervised phenotyping depends on preprocessing. Any striking phenotype should be tested against scaling, variable-selection, and cohort-definition choices before it is accepted.

HDBSCAN also introduces hyperparameter sensitivity. I conducted a broad search (9 times 120 configurations) and selected the optimal hyperparameters, including min_cluster_size= 1000 and epsilon= 0.0, by maximising the composite quality criterion Q. Because the underlying structure is a gradient, however, the number of tiers is partly tied to min_cluster_size. More broadly, UMAP+HDBSCAN is stochastic and can be sensitive to random initialisation and imperfect global-structure preservation. I mitigated this through ten random seeds per configuration, per-method bootstrap analysis, 80% subsampling, and comparison with PCA. The headline conclusion does not depend on UMAP alone: PCA also supports the severity gradient (PC1 = 56%). Re-running the pipeline under ten random seeds produced near-identical labels (mean pairwise ARI 0.957; Section sec:robustness). The exact cluster count can fluctuate, but the severity ordering is stable across these checks.

Computational cost is the final practical limitation. Running UMAP+HDBSCAN 50 times for each method is non-trivial, although the modular architecture permits parallelisation. Because the 14 variables are reduced to 6 domain scores, runtimes remained manageable on a consumer-grade laptop.



## Future Directions

_Source: `report/Chapters_short/Chapter6.tex`_

The findings and limitations suggest four concrete directions for future work.

Model the continuum directly. The clearest implication of the severity-gradient finding is that a continuous cognitive-severity score - for example, the first principal component, or a supervised index validated against functional outcome - may be a more faithful and more useful summary than a discrete tier label. Future work should compare a continuous severity index against the tiered representation for prognosis and for matching rehabilitation intensity to need, treating the tiers as an interpretable discretisation of the underlying score rather than as natural kinds.

Longitudinal clustering is the most direct extension. Applying the pipeline to assessments collected at fixed time points would let the analysis describe how a patient's position on the severity gradient changes over the recovery trajectory: whether the initial level predicts long-term outcome, and whether recovery rates differ across the severity range [@ponsford2014longitudinal]. Trajectory-based severity modelling would be a far more useful input to prognosis and rehabilitation-intensity decisions than the cross-sectional snapshot.

Multi-centre validation is the prerequisite for treating the severity stratification as a feature of ABI rather than of this particular service. A multi-centre study across different healthcare systems would test whether the one-dimensional severity structure survives changes in catchment, test battery, and assessment timing, and would let researchers develop harmonisation strategies for cross-centre comparison [@maas2017traumatic].

Neuroimaging integration would bridge the gap between cognitive severity and neural mechanism. Linking a patient's position on the severity gradient to structural and functional brain-imaging measures could identify the neural correlates of global cognitive impairment after ABI, the kind of evidence that could guide targeted intervention [@saatman2008classification, maas2017traumatic].

---REWORK

The current results are consistent with a three-tier cognitive severity stratification system. 
However, there are several limits to this approach.
Firstly, the study was based in a single centre. 
All data were obtained from one rehabilitation unit. 
Therefore, the possibility of selection bias exists and extrapolation to other clinical groups cannot be made. 
Although all tests used have been extensively studied and have international validity, the six cognitive domains provide a common framework for the description of post-injury cognition. 
However, the validation of this cognitive severity structure will require multi-centre studies prior to its acceptance as a general characteristic of ABI rather than as a specific characteristic of this unit.

Secondly, the recovered structure is a limitation on interpretation. 
The major finding is a continuum rather than distinct categories. 
Most of the cohort fall along a single dimension representing overall cognitive severity with PC1 accounting for 56% of the variance. 
The three tiers represent a discretization of this continuum. 
Therefore, the tiers should not be regarded as phenotypic entities with well defined boundaries. 
Tier count will be influenced by both the resolution of clustering and the proportion of missing data. 
Assessments located near tier boundaries should be viewed cautiously. 
Ultimately, a continuous severity score may be more representative than discrete tiers (Section sec:future).

Thirdly, the analytical approach has limited capacity to model temporal change. 
ABI recovery is typically rapid during the early stages and follows a slower rate thereafter [@ponsford2014longitudinal, maas2017traumatic]. 
Therefore, a single assessment provides only a 'snapshot' of a patient's recovery status. 
For many patients in the dataset, the inclusion of multiple assessments allows for the examination of change within patients (below); however, the timing of follow-up assessments is still determined by clinical necessity rather than being standardized.

Of the 5206 patients with longitudinal data (Section sec:robustness), the pattern described above is clinically plausible: 50.2% of patients remain in the same tier, while of those whose tier changed, 706 moved towards improved function whereas 206 moved towards worsened function. 
This 3:1 ratio represents the expected direction of recovery. 
However, the degree to which this reflects true recovery versus selection factors (e.g., patients being discharged when they demonstrate improvement) cannot be completely distinguished.

Future longitudinal designs with standardized assessment intervals will be necessary to determine this question.

Furthermore, the imputation strategy introduces another constraint on interpretation. 
The MAR assumption cannot be tested from observed data alone [@rubin1976inference, little2019statistical]. 
In clinical settings, a test may be incomplete due to the inability of a patient to complete it; therefore, the missing value may be informative and may represent impaired performance. 
If patterns of MNAR were prevalent in clinical settings, function might be overestimated. 
An upper bound on the impact of MNAR is provided by re-imputing every missing value to the lowest observed performance (the "tipping point" check; Section sec:robustness). 
Under that extreme assumption, the Global Impairment tier persisted and included 65% of its original membership; however, the finer partition degraded. 
A formally-specified delta-shifted sensitivity analysis would further refine this bound.

Additionally, a structured co-occurrence of missingness may provide some reassurance regarding test-battery protocol-driven dropout rather than solely outcome-driven dropout. 
The comparison of 10 imputation methods also serves as a sensitivity analysis. 
High-confidence consensus labels were assigned to 86.2% of assessments across methods, indicating that plausible imputation differences did not substantially affect the primary cognitive-severity structure for most of the cohort.

Another related caveat concerns the Tier-1 filter that removes assessments where more than half of their values are missing. 
Upon review (Section sec:robustness), removed records averaged only 0.8 out of 14 completed tests and were highly similar demographically to retained records. 
Therefore, the Tier-1 filter likely removed primarily empty administrative records rather than an undetected severely impaired group. 
Still, due to missing data issues, the cognitive severity of removed records cannot be assessed directly, and only the 30-70% threshold sensitivity analysis bounds the potential effect of this decision.

Finally, the pipeline imputes and then clusters, whereas model-based alternatives exist (such as latent-profile analysis via full-information maximum likelihood). 
The Gaussian-mixture baseline (Section sec:robustness) demonstrated that BIC decreased monotonically with increasing numbers of classes, providing support for a continuum rather than a discrete optimum. 
Thus, developing a latent-profile analysis that utilizes FIML instead of HDBSCAN is another viable area of future development.

Feature-engineering remains relevant. 
Non-cognitive features are eliminated and every feature is standardized (direction aligned), and winsorized prior to summarizing them as composites and generating potentially artificial profile differences. 
More generally, the methodological lesson is clear: unsupervised phenotyping relies on preprocessing. 
Any distinctive phenotype identified in an exploratory fashion should be examined relative to choices about scaling, variable selection and cohort definition before it receives a clinical label.

Finally, HDBSCAN introduces sensitivity to hyperparameters. 
I conducted an extensive search (9 x 120 configuations) and selected optimal parameters [min_cluster_size = 1000 and epsilon = 0.0], maximizing the composite quality metric Q. 
Because the underlying structure is unidimensional, however, there is a relationship between cluster size and number of tiers. 
In addition to examining UMAP + HDBSCAN stochastically and potentially sensitively to random initialization and imperfect preservation of global structure, I applied ten random seeds per configuration/bootstrap sample/variable subset/subsampling rate combination, and PCA as an additional form of comparison. 
The main conclusion does not rely on UMAP alone; PCA also demonstrates that there is a strong cognitive-severity gradient (PC1 = 56%) represented by the first principal component. 
Re-running the entire pipeline with ten random seeds resulted in nearly identical labels (ARI mean pairwise = .957; Section sec:robustness). 
While the exact number of tiers can vary slightly depending upon these checks, the overall order of severity is robust.

Lastly, computational cost presents a fourth practical limit. 
Running UMAP + HDBSCAN fifty times per method is computationally intensive; however, due to modularity allowing for parallel processing, runtime costs were manageable on a typical consumer-grade laptop.

Four potential areas for future work arise from the findings and limitations described above.

Firstly, modeling the continuum directly. 
The most obvious implication of the findings regarding cognitive-severity gradients is that continuous cognitive-severity indices - either derived from PCA or supervised learning models trained on functional-outcome measures - may provide more accurate representations and may be more useful summaries than tier-based classifications. 
Future research should investigate comparing continuous cognitive-severity indexes to tier classification schemes for predicting prognosis and for assigning rehabilitation intensity according to need by treating tier classification as an interpretable discretization of a continuous measure rather than as natural categories.

Secondly, longitudinal clustering represents an obvious next step. 
Applying the developed pipeline to assessments collected at regular time points would allow researchers to describe how individual patients' positions on the cognitive-severity gradient evolve over time as part of their recovery trajectories: i.e., whether patients' initial levels predict longer-term outcomes and whether recovery rates differ depending on severity level [@ponsford2014longitudinal]. 
Severity-based models describing recovery trajectories would represent much more valuable inputs to clinicians determining prognosis and rehabilitation-intensity decisions than cross-sectionally-derived assessments.

Thirdly, multi-center validation represents an essential requirement for considering cognitive-severity stratification as a feature of acquired-brain injury rather than as a feature of this specific service. 
A multi-center study across different health care systems would assess whether the one dimensional cognitive-severity gradient found here survives changes in catchment population and test batteries and assessment schedules [@maas2017traumatic].

Fourthly, integrating neuroimaging will help link cognitive-severity gradings with neural mechanisms. 
By correlating an individual's position on the cognitive-severity gradient to structural-functional imaging metrics, researchers may identify the neural correlates of global cognitive impairments following ABI; this type of evidence may assist in targeting interventions [@saatman2008classification, maas2017traumatic].
