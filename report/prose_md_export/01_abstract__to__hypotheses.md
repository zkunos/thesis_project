<!-- Exported prose chunk 1. Word count: 1168. -->


# Abstract

_Source: `report/main_short.tex`_

Following acquired brain injury (ABI), cognitive performance is among the strongest predictors of long-term functional outcome. The patients most likely to require intensive rehabilitation, however, are often the least likely to complete a full neuropsychological battery. Missingness in this setting is therefore clinically informative: fatigue, confusion, motor limitation, test tolerance, and examiner judgement all constrain which measures are administered. A complete-case analysis would preferentially retain healthier assessments and discard many of the most impaired patients. Broad diagnostic categories and injury-severity bands introduce a second limitation, since neither captures the cognitive variation needed for personalised rehabilitation planning.

This thesis addresses these problems by pairing missing-data imputation with unsupervised clustering. Incomplete assessments are retained, cognitive structure is inferred directly from test data, and the dependence of that structure on the selected imputation method is evaluated explicitly.

The analysis used 17,406 neuropsychological assessments from 7,285 patients with ABI. It recovered a three-tier cognitive structure: Above-Average (38.6%, n = 6{,}725), Near-Normal (36.4%, n = 6{,}328), and Global Impairment (25%, n = 4{,}353). The tiers differ primarily in overall cognitive level rather than profile shape. All six cognitive domains co-vary across the tiers, and one severity factor explains 56% of their shared variance. The clusters are therefore better interpreted as a data-driven cognitive-severity continuum than as qualitatively distinct phenotypes. No attention-specific dissociation was supported.

The severity structure was stable across imputation strategies. Under the pre-registered criteria, all ten methods yielded distinct, low-noise solutions, with a mean pairwise Adjusted Rand Index (ARI) of 0.71. The primary MICE solution achieved a full-coverage silhouette of 0.526 and no residual noise points. Tier membership was also associated with clinical-unit placement after adjustment for diagnosis (Cramér's V 0.16; Cochran-Mantel-Haenszel test), indicating that the recovered structure corresponds to clinically meaningful patient routing rather than to a purely methodological artefact. Domain-level aggregation further improved numerical conditioning relative to variable-level clustering, reducing the mean VIF from 2.8 to 1.9 and the condition number from 62 to 12.

CogDash, the accompanying interactive dashboard, implements the full pipeline for future patients and reports both severity tier and consensus confidence across imputation methods. The code, notebooks, and dashboard are available at https://github.com/zkunos/thesis_project.



# Acknowledgements

_Source: `report/main_short.tex`_

My deepest thanks go to my supervisor, Dr. Alejandro Garc'ia-Rudolph, whose expertise in clinical neuropsychology and neurorehabilitation was invaluable in guiding this research and interpreting its results. I also wish to acknowledge Dr. Laura Igual Mu noz for her support during my master's studies. Lastly, I am endlessly grateful to my family for their continued support.



# Statement on the Use of Artificial Intelligence

_Source: `report/main_short.tex`_

In accordance with the guidelines of the Facultat de Matemàtiques i Informàtica of the Universitat de Barcelona regarding the use of Large Language Models (LLMs) in the Final Master's Thesis, I state the following.

During the preparation of this thesis, I used Claude (Anthropic) as an AI assistant to augment my research workflow.

The use of the tool proceeded as follows:

- Code writing: Python code development to perform data preprocessing, imputation, clustering, and visualisation, and debugging.

- Assistance with writing: Editing drafts to enhance academic style and clarity, and rewording rough drafts.

- Dashboard development: Support with the development of the Streamlit interactive dashboard (CogDash).

- LaTeX formatting: thesis formatting, table and figure formatting, and compilation errors.

I am responsible for the research design, hypothesis formulation, methodology, data analysis, interpretation, and discussion. I personally reviewed and edited all AI-generated text, and I cross-checked all referenced material against the original source.



## Background and Problem Statement

_Source: `report/Chapters_short/Chapter1.tex`_

Acquired brain injury (ABI) includes traumatic brain injury (TBI), stroke, encephalitis, and hypoxic-ischaemic injury. The clinical burden is substantial. TBI alone accounts for millions of hospitalisations and emergency-room admissions each year [@maas2017traumatic, brazinova2021epidemiology]; among working-age adults, ABI frequently produces long-term disability involving physical, emotional, and cognitive sequelae [@corrigan2010epidemiology]. Cognitive impairment may involve attention, memory, language, executive function, or several domains simultaneously. Its configuration, however, varies markedly from one patient to another.

That heterogeneity creates a practical problem for rehabilitation. Patients with comparable injury severity may present sharply different cognitive profiles at neuropsychological follow-up, while the labels commonly used for triage, including diagnosis and broad severity bands, are too coarse to parse those differences [@saatman2008classification]. When clinically distinct profiles are aggregated under the same category, the within-group variation most relevant to treatment planning is obscured.

This thesis approaches the problem empirically. Rather than imposing an existing clinical taxonomy on the dataset, I use unsupervised clustering to recover cognitive subgroups from neuropsychological test scores and then assess their clinical relevance. Routinely collected clinical data introduce a second complication: missing values. In rehabilitation practice, full batteries are often curtailed by time constraints, fatigue, clinical judgement, or patient limitations, so omissions cannot be assumed to be random. Imputation allows incomplete assessments to be retained, but each method imposes its own assumptions on the unobserved data. The extent to which those assumptions alter downstream clustering remains insufficiently documented; this thesis evaluates that sensitivity directly.

In this work, phenotyping refers to the data-driven identification of cognitive subgroups. Whether such subgroups represent qualitatively distinct profiles or graded levels of overall severity is left as an empirical question. The present findings support the latter interpretation.



## Research Questions

_Source: `report/Chapters_short/Chapter1.tex`_

There are four questions I want to answer in this work:

- RQ1: Will unsupervised clustering of the imputed data reveal distinct cognitive phenotypes in patients with acquired brain injury?

- RQ2: How much does the choice of imputation method influence the phenotypes that emerge?

- RQ3: Can cluster membership be linked to the clinical unit of assessment? If so, this implies that phenotypes reflect actual differences in the populations seen by different services.

- RQ4: Are the phenotypes more consistent and easier to interpret when clustering on domain-level composites rather than individual test variables?

The broader aim is to build a reproducible phenotyping pipeline for routine clinical data. Missingness is modelled as part of the rehabilitation process itself, not treated as a retrospective nuisance.



## Hypotheses

_Source: `report/Chapters_short/Chapter1.tex`_

This study investigates the following four hypotheses:

H1: Using a UMAP and HDBSCAN pipeline, I expect to identify at least two separate, stable cognitive clusters for most imputation methods, with noise kept under 30% and silhouette scores exceeding 0.40.

H2: There should be moderate to high agreement between cluster solutions derived from different imputation approaches (ARI and NMI both exceeding 0.50). Such agreement would show that the phenotypes are not merely an artefact of the imputation process.

H3: Chi-square tests and Cramér's V effect sizes (above 0.10) should demonstrate a significant connection between cluster membership and clinical unit, thereby mirroring the disparity in cognitive profiles between the services.

H4: By clustering on domain-level features, I expect a representation that is more interpretable than variable-level features; this should be reflected in higher silhouette scores and reduced multicollinearity, evidenced by lower condition numbers and mean variance inflation factors.

---REWORK


# Summary

Source: report/main_short.tex

Cognitive performance post Acquired Brain Injury (ABI) has been identified as one of the greatest predictors of long term functional outcome. However, the patients who need intensive rehabilitation are usually the ones who will be unable to complete a full neuropsychological battery. Therefore, missingness is informative in this context. Fatigue, confusion, motor limitations, test tolerance, and examiner judgment can limit the testing completed. As a result, retaining healthier assessments will favorably bias the selection of patients included in analyses and exclude the most impaired patients. While broad diagnostic categories and injury severity bands provide some way to group patients based upon similar characteristics, they do not capture the necessary variability required to create personalized rehabilitation plans.

This dissertation addresses these concerns through using a combination of missing-data imputation and unsupervised clustering. Complete assessments are retained and cognitive structures are inferred directly from test data. The dependency of the cognitive structures created by the selected imputation strategy is explicitly assessed.

Data were collected from 17,406 neuropsychological evaluations performed on 7,285 patients with ABI. Three cognitive structures were found to exist: Above Average (38.6%, n=6,725); Near Normal (36.4%, n=6,328); and Global Impairment (25%, n=4,353). The main difference between the cognitive structures relates to the general level of cognition instead of the profile shape. All six cognitive domains vary together across the cognitive structures and one severity factor explains 56% of the common variance among them. Therefore, the clusters are better described as a data-derived cognitive severity continuum than as qualitatively distinct phenotypes. Furthermore, there is no evidence to suggest an attention specific dissociation exists.

The cognitive structure found was independent of the imputation strategy. The majority of the imputation strategies produced well-defined clusters with minimal noise. Ten pre-registered imputation strategies produced distinct clusters with little to no residual noise. The average adjusted rand index (ARI) between the imputation strategies was .71. The primary multiple imputation chained equations (MICE) strategy had a full coverage silhouette of .526 and no noise points remained in the sample. After adjusting for diagnosis, the cluster assignment was significantly related to clinical unit placement (Cramér’s V = 0.16; Cochran-Mantel-Haenszel test). This suggests that the cognitive structure discovered reflects real differences in patient populations being served by different clinics. Additionally, aggregating at the domain level produced improved conditions over variable level clustering for numerical computations. Specifically, it resulted in a decrease in the mean variance inflation factor (VIF) from 2.8 to 1.9 and the mean condition number from 62 to 12.

CogDash is an interactive dashboard developed to implement this entire pipeline for future patients. Additionally, it provides both severity tier assignments along with consensus confidence across all imputation methods. The code, notebooks and dashboard are accessible at https://github.com/zkunos/thesis_project.

# Acknowledgments

Source: report/main_short.tex

First and foremost I would like to thank my advisor, Dr. Alejandro Garc’ia Rudolph, for his knowledge and expertise in both clinical neuropsychology and neurorehabilitation which helped guide me throughout my research and provided valuable insights into how to interpret my results. I would also like to express my gratitude toward Dr. Laura Igual Munoz for her assistance during my graduate program. Last but certainly not least I would like to say thank you to my family for their continued support and encouragement throughout my graduate program.

# Use of Artificial Intelligence in this Study

Source: report/main_short.tex

According to the guidelines provided by the Facultad de Matemàtiques i Informàtica of the Universitat de Barcelona regarding the use of large language models (LLMs) in final master’s thesis research I make the following statement.

Throughout my research I utilized Claude (Anthropic) as an AI-assistant tool to improve my research workflow.

Claude was used as follows:

- To write code for Python, for performing data cleaning/preprocessing, imputation, clustering and visualization, and debugging.

- To assist with drafting: editing draft versions to improve academic tone/clarity and rephrase initial drafts.

- To develop dashboard: assisting in developing the Streamlit interactive dashboard (CogDash).

- To format LaTex document: formatting of thesis document (LaTex), tables, figures, compiling issues.

I take responsibility for designing/researching hypothesis creation, methodology development, data analysis and interpretation/discussion. I reviewed/edit all generated AI-texts myself and verified referenced materials with source documents.

## Background and Problem Statement

Source: report/Chapters_short/Chapter1.tex

Acquired Brain Injury (ABI) encompasses traumatic brain injuries (TBIs), strokes, encephalitis and hypoxic-ischemic injuries. Clinical impact is considerable. TBI alone contributes to millions of hospitalizations/emergency room visits annually [@maas2017traumatic,brazinova2021epidemiology] ; Among working age adults ABI causes long-term disability which can include physical, emotional, and cognitive sequelae [@corrigan2010epidemiology]. Cognitive impairments can affect attention/memory/language/executive function/cognitive domains collectively; however configurations vary substantially across patients.

Variability among patients poses a practical challenge for rehabilitation; Patients with identical injury severities may have very different cognitive profiles at follow up evaluation following ABi; whereas common labels used for triage (diagnosis/severity band) aggregate distinctly different cognitive profiles and obscure clinically meaningful variations within groups [@saatman2008classification].

This dissertation addresses the issue empirically; Instead of applying a priori clinical taxonomy to the data set, I employ unsupervised clustering to derive cognitive subgroups from neuropsychological test scores; and subsequently evaluate their clinical relevance. Clinically collected data pose an additional obstacle: missing values. Omission of full batteries occurs regularly in rehabilitation practice due to time restrictions/fatigue/examiner judgment/patient limitations; therefore nonrandom omission of items is expected.

Missing value imputation allows retention of incomplete assessments; however each method introduces its own assumptions about unknown values. Limited documentation exists regarding how those assumptions will impact subsequent clustering; this dissertation evaluates that dependency directly.

Phenotyping refers to identification of cognitive subgroups via data driven approach; whether those subgroups describe qualitative distinct profiles or gradations of overall severity will remain an empirical determination.

## Research Questions

Source: report/Chapters_short/Chapter1.tex

There are four questions I seek to answer in this dissertation:

Question RQ1: Can unsupervised clustering of the imputed data indicate discrete cognitive phenotypes in patients with acquired brain injuries?

Question RQ2: What degree does choice of imputation strategy influence emergent phenotypes?

Question RQ3: Is cluster membership predictive of clinical unit assessment? If so, this would indicate that phenotypes represent actual differences in population serviced by different units.

Question RQ4: Do phenotypes exhibit greater consistency and/or ease-of-interpretation when clustered using domain-level composite versus individual test variables?

The ultimate goal is to construct a replicable phenotyping pipeline for routinely collected clinical data. Missingness will be modeled as part of the rehabilitation process itself rather than considered a posteriori nuisance.

## Hypotheses

Source: report/Chapters_short/Chapter1.tex

This dissertation examines the following four hypotheses:

Hypothesis H1: Using a UMAP/HDBSCAN pipeline I anticipate finding at least two separate stable cognitive clusters for most imputation methods; wherein >90% of observations are assigned a valid cluster assignment and <30% noise point rate; and wherein >80% observations yield a silhouette score > .40.

Hypothesis H2: Agreement should exist between cluster solutions generated using different imputation techniques (ARI/NMI > .50). High levels of agreement would confirm that the phenotypes do not arise solely from artifacts generated by the imputation technique(s).

Hypothesis H3: Chi-Square Tests/Cramérs V Effect Sizes (> .10) should illustrate a statistically significant relationship between cluster membership and clinic unit; thus illustrating that cluster membership reflects actual differences in populations serviced by different clinics.

Hypothesis H4: Aggregating at the domain level should produce representations that are more interpretable than aggregating at the variable level; Thus facilitating increased silhouette scores and decreased multicolinearity represented by reduced Condition Numbers/Variance Inflation Factors (mean VIF = 2.8 vs 1.9; mean CN = 62 vs 12).

CogDash is an interactive dashboard designed to execute this entire pipeline for future patients; additionally it provides both severity tier assignment and consensus confidence across all imputation techniques. The code/notebooks/dashboard are located at https://github.com/zkunos/thesis_project
