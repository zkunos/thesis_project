<div class="titlepage">

<div class="center">

<span class="smallcaps"></span>

<span class="smallcaps">Fundamental Principles of Data Science Master’s Thesis</span>  
  

  

<div class="minipage">

<div class="flushleft">

*Author:*  
[](http://www.johnsmith.com)

</div>

</div>

<div class="minipage">

<div class="flushright">

*Supervisor:*  
[](http://www.jamessmith.com)

</div>

</div>

  

*A thesis submitted in partial fulfillment of the requirements  
for the degree of MSc in Fundamental Principles of Data Science*  
*in the*  
  

2026-06-11  

</div>

</div>

<div class="acknowledgements">

First and foremost I would like to thank my advisor, Dr. Alejandro García Rudolph, for his knowledge and expertise in both clinical neuropsychology and neurorehabilitation which helped guide me throughout my research and provided valuable insights into how to interpret my results. I would also like to express my gratitude toward Dr. Laura Igual Munoz for her assistance during my graduate program. Last but certainly not least I would like to say thank you to Daniel for his continued support and encouragement throughout my graduate program.

</div>

# Statement on the Use of Artificial Intelligence

According to the guidelines provided by the Facultad de Matemàtiques i Informàtica of the Universitat de Barcelona regarding the use of large language models (LLMs) in final master’s thesis research I make the following statement.

Throughout my research I utilized Claude (Anthropic) as an AI-assistant tool to improve my research workflow.

Claude was used as follows:

- To write code for Python, for performing data cleaning/preprocessing, imputation, clustering and visualization, and debugging.

<!-- -->

- To assist with drafting: editing draft versions to improve academic tone/clarity and rephrase initial drafts.

<!-- -->

- To develop dashboard: assisting in developing the Streamlit interactive dashboard (CogDash).

<!-- -->

- To format LaTex document: formatting of thesis document (LaTex), tables, figures, compiling issues.

I take responsibility for designing/researching hypothesis creation, methodology development, data analysis and interpretation/discussion. I reviewed/edit all generated AI-texts myself and verified referenced materials with source documents.

# Introduction

## Background and Problem Statement

Acquired Brain Injury (ABI) encompasses traumatic brain injuries (TBIs), strokes, encephalitis and hypoxic-ischemic injuries. Clinical impact is considerable. TBI alone contributes to millions of hospitalizations/emergency room visits annually (Maas et al. 2017; Brazinova et al. 2021); among working-age adults, ABI causes long-term disability, which can include physical, emotional, and cognitive sequelae (Corrigan, Selassie, and Orman 2010). Cognitive impairments can affect attention, memory, language, executive function, and other cognitive domains collectively; however, configurations vary substantially across patients.

Variability among patients poses a practical challenge for rehabilitation. Patients with identical injury severities may have very different cognitive profiles at follow-up evaluation following ABI, whereas common labels used for triage (diagnosis/severity band) aggregate distinctly different cognitive profiles and obscure clinically meaningful variations within groups (Saatman et al. 2008).

This dissertation addresses the issue empirically. Instead of applying a priori clinical taxonomy to the data set, I employ unsupervised clustering to derive cognitive subgroups from neuropsychological test scores and subsequently evaluate their clinical relevance. Clinically collected data pose an additional obstacle: missing values. Omission of full batteries occurs regularly in rehabilitation practice due to time restrictions, fatigue, examiner judgment, and patient limitations; therefore, nonrandom omission of items is expected.

Missing value imputation allows retention of incomplete assessments; however, each method introduces its own assumptions about unknown values. Limited documentation exists regarding how those assumptions will impact subsequent clustering; this dissertation evaluates that dependency directly.

Phenotyping refers to identification of cognitive subgroups via a data-driven approach. Whether those subgroups describe qualitatively distinct profiles or gradations of overall severity remains an empirical determination.

## Research Questions

There are four questions I seek to answer in this dissertation:

Question RQ1: Can unsupervised clustering of the imputed data indicate discrete cognitive phenotypes in patients with acquired brain injuries?

Question RQ2: What degree does choice of imputation strategy influence emergent phenotypes?

Question RQ3: Is cluster membership predictive of clinical unit assessment? If so, this would indicate that phenotypes represent actual differences in population serviced by different units.

Question RQ4: Do phenotypes exhibit greater consistency and/or ease-of-interpretation when clustered using domain-level composite versus individual test variables?

The ultimate goal is to construct a replicable phenotyping pipeline for routinely collected clinical data. Missingness will be modeled as part of the rehabilitation process itself rather than considered a posteriori nuisance.

## Hypotheses

This dissertation examines the following four hypotheses:

Hypothesis H1: Using a UMAP/HDBSCAN pipeline, I anticipate finding at least two separate stable cognitive clusters for most imputation methods, with a noise point rate below 30% and a silhouette score above 0.40.

Hypothesis H2: Agreement should exist between cluster solutions generated using different imputation techniques (ARI/NMI $`> 0.50`$). High levels of agreement would confirm that the phenotypes do not arise solely from artifacts generated by the imputation technique(s).

Hypothesis H3: Chi-square tests and Cramér’s V effect sizes ($`> 0.10`$) should illustrate a statistically significant relationship between cluster membership and clinical unit, indicating that cluster membership reflects actual differences in populations serviced by different clinics.

Hypothesis H4: Aggregating at the domain level should produce representations that are more interpretable than aggregating at the variable level, thus facilitating comparable silhouette scores and decreased multicollinearity represented by reduced condition numbers and variance inflation factors (mean VIF 2.77 to 1.88; mean CN 61.7 to 11.8).

CogDash is an interactive dashboard designed to execute this entire pipeline for future patients; additionally it provides both severity tier assignment and consensus confidence across all imputation techniques. The code/notebooks/dashboard are located at <https://github.com/zkunos/thesis_project>.

# Literature Review

## Acquired Brain Injury and Cognitive Assessment

In the current clinical context, "acquired brain injury" (abi) refers to a non-inherited/non-congenital insult to the brain that is either degenerative or due to perinatal trauma. While abi is used to classify different injuries (e.g., stroke, encephalitis, hypoxic/ischemic brain damage and traumatic brain injury (TBI)) their etiologies vary, they share common rehabilitation challenges: cognitive outcomes are frequently major determinants of long-term functional status post-acute injury resolution. The primary tool for measuring the impact of these injuries is neuropsychological evaluation. Standardized neuropsychological batteries generally assess performance in several areas including visuospatial abilities, language, executive functions, learning/memory, and processing speed. Each of these areas represents practical issues that arise during rehabilitation. For example, attention difficulties can limit the patient’s participation in therapy. Memory impairments can preclude the development of new strategies to compensate for lost skills. Executive and/or language impairments can affect a person’s ability to plan and advocate for themselves, as well as communicate their needs. Visuospatial impairments can affect a person’s ability to navigate independently. Therefore, a cognitive profile will provide valuable information regarding the course of rehabilitation, medicolegally, and ultimately regarding return-to-work issues.

It is also important to note that in individuals who sustain a moderate to severe TBI, there may be persistent cognitive deficits that do not uniformly resolve. In some cases, patients may demonstrate recovery of attention, while their memory and executive functions remain impaired. Conversely, other patients may display the opposite pattern, as documented in (Ponsford et al. 2014)’s longitudinal study. Similarly, (Rabinowitz and Levin 2014), in their meta-analysis, indicated that significant cognitive deficits were present regardless of injury severity. Thus, severity of injury does not adequately represent the organization of each individual’s cognitive deficit.

Additionally, assessment practices introduce further variability into cognitive assessments. Neuropsychologists adjust standardized batteries based on a variety of factors, including referral questions, patient tolerance for testing and clinical judgment. As a result, the resultant databases exhibit considerable structured missingness. Therefore, multivariate analyses should accommodate this structural aspect of missingness rather than treat missing values as just another minor technical issue.

## Missing Data in Clinical Research

Missing Data are ubiquitous in clinical studies. (Gravesteijn et al. 2021) indicate that approximately 20% of clinical trials report greater than 10% Missing Data rates. (Rubin 1976) delineated three ways missing values could occur. Missing completely at random (MCAR) implies that missingness occurs randomly and independently of observed and unobserved variables. Missing at random (MAR) suggests that missingness is associated with observed variables but not with the missing variable given those variables are controlled for. Missing not at random (MNAR) suggests that missingness is dependent on the unobserved variable.

The type of missingness affects what methods can be applied. Listwise deletion is unbiased when the missingness follows an MCAR pattern but results in loss of efficiency. Methods like multiple imputation and maximum likelihood estimation allow valid inference when the assumptions for MAR are met and when the model is properly formulated. Sensitivity analysis is necessary when assuming MNAR behavior since there is no method using only observable data which can remove dependency on unobservable values (Rubin 1987).

This distinction between types of missingness is particularly critical in clinical neuropsychology. For example, a severely impaired patient in terms of attentional functioning may not have sufficient energy to complete an executive-functioning task. A disoriented patient may receive no memory test whatsoever. Both situations describe missing scores which are likely related to the value that would have been scored if they had completed the test. Thus, MAR is a reasonable working assumption rather than a proven fact. It is possible that MNAR patterns exist simultaneously with missingness due to adherence to protocol. Although the specific mechanism of missingness cannot be determined solely from the observed data, auxiliary variables can help make the MAR assumption more plausible by controlling for clinically relevant information (Little and Rubin 2019).

The proportion of Missing Data is only part of the issue. The way data are missing influences potential biases. Simply knowing that data are missing (how frequent the Missing Data are) is only part of the problem. More importantly, understanding why data are missing and how they came to be missing determines how large an expected bias will be. Because broad neuropsychological batteries are typically incomplete and thus necessitate imputations (many clinically meaningful evaluations are done incompletely), the reliability of imputed values depend upon observed relationships among variables. Prior to performing preprocessing that retains variables containing enough observed data to enable conditional estimation; the subsequent cluster analysis must take into account the uncertainty propagated through imputation.

## Imputation Methods

Each of the ten methods used in this dissertation will be presented in order of increasing complexity. Consider the data matrix $`X \in \mathbb{R}^{n \times p}`$, which contains $`n`$ assessments and $`p`$ variables. Assume the $`i`$-th assessment includes $`p`$ variables $`x_{ij}`$, and let $`\Omega = \{(i, j): x_{ij} \text{ is observed}\}`$. Then $`\Omega_j = \{i : (i, j) \in \Omega\}`$ represents the observed rows for the $`j`$-th variable. Define the operator $`P_\Omega`$ as follows: for any entry $`x_{ij}`$ of the matrix $`X`$, $`P_\Omega(x_{ij}) = x_{ij}`$, if $`x_{ij} \in \Omega`$; otherwise, $`P_\Omega(x_{ij}) = 0`$. The objective is to estimate $`\hat{x}_{ij}`$ for entries not in $`\Omega`$.

**Mean Imputation Method**.

The mean imputation method substitutes each missing value with the arithmetic mean of the observed values for that variable.

``` math
\label{eq:mean}
\hat{x}_{ij}=\bar{x}_j=\frac{1}{|\Omega_j|}\sum_{i\in\Omega_j}x_{ij}.
```

The mean imputation method is fast and does not require any iteration. However, it reduces variance and covariance, creates distorted marginal distributions, and results in underestimated standard errors. Therefore, it was only used in this study as a baseline.

**K-Nearest Neighbors (KNN)**.

The KNN imputation method finds the $`k`$ most similar donor cases and assigns the missing value a weighted average of their observed values based on the Euclidean distance as the similarity measure. We can define the KNN imputation method as follows:

``` math
\label{eq:knn}
\hat{x}_{ij}=\frac{\sum_{k\in\mathcal{N}_i}w_{ik}\,x_{kj}}{\sum_{k\in\mathcal{N}_i}w_{ik}},\qquad w_{ik}=\frac{1}{d(i,k)},
```

where $`\mathcal{N}_i`$ is the set of $`k`$ nearest donors and $`d(i,k)`$ is the distance between observations on the jointly observed variables. Since KNN is a non-parametric method, it can better capture the local structure than mean imputation. There are some limitations for KNN. Small values of $`k`$ may fit the noise, while large values of $`k`$ may smooth too much meaningful pattern. As the size of the dataset increases, the computational cost of KNN becomes greater.

**Multiple Imputation by Chained Equations (MICE)**.

Multiple Imputation by Chained Equations imputes each variable conditionally on all other variables and iteratively repeats this process over several iterations (Buuren and Groothuis-Oudshoorn 2011). In each iteration $`t`$, each variable is drawn anew from its conditional model:

``` math
\label{eq:mice}
x_{ij}^{(t)}\sim p\!\left(x_{ij}\,\middle|\,\mathbf{x}_{i,-j}^{(t)};\,\theta_j\right),\qquad j=1,\dots,p,
```

We can adapt the form of the conditional model to the type of data; e.g., we can use linear models for continuous variables and logistic models for binary variables. MICE retains multivariate relationships and can produce multiple imputations to quantify uncertainty. One of its limitations is that we must specify a model for every variable, and there are possibilities for problems during convergence.

**Predictive Mean Matching (PMM)**.

PMM is a semi-parametric method that is commonly employed within MICE. The predictive mean matching algorithm first predicts new values for each missing value using a regression model. The imputed value is then randomly selected from among all previously observed values with similarly predicted values:

``` math
\label{eq:pmm}
\hat{x}_{ij}\sim\operatorname{Unif}\bigl\{x_{kj}:k\in\mathcal{D}_{ij}\bigr\},\qquad
\mathcal{D}_{ij}=\bigl\{\,d\text{ observed }k\text{ minimising }|\hat{x}_{kj}-\hat{x}_{ij}|\,\bigr\}.
```

In doing so, imputed values will always lie within the range of observed data, thus avoiding impossible values (e.g., negative scores on tests that include floors). However, one limitation is that a limited donor pool can cause repeated usage of the same observed values.

**MissForest**.

MissForest is an iterative random-forest imputation method (Stekhoven and Bühlmann 2012). For each variable $`j`$, we train a forest $`f_j`$ using all available data with the remaining variables as predictors. Afterward, we update missing values using the newly created forest and repeat this procedure until little change occurs:

``` math
\label{eq:missforest}
\hat{x}_{ij}=f_j\!\left(\mathbf{x}_{i,-j}\right)\quad\text{until}\quad \sum_{(i,j)\notin\Omega}\bigl(x_{ij}^{(t)}-x_{ij}^{(t-1)}\bigr)^2 \text{ stops decreasing.}
```

Because MissForest is a non-parametric method, it can model complex non-linear relationships and accommodate both continuous and discrete variables. Often MissForest performs well on benchmark datasets; however, it is computationally intensive and scales poorly when either the number of rows or trees is large.

**Expectation-Maximization (EM)**.

EM is another method that iterates between an E-step, which computes the expected sufficient statistic, and an M-step, which adjusts the parameters by maximizing the log-likelihood (Dempster, Laird, and Rubin 1977). When assuming multivariate normality, EM converges to the maximum likelihood estimator, and missing blocks are filled-in using their conditional mean:

``` math
\label{eq:em}
\hat{\mathbf{x}}_{\mathrm{mis}}=\boldsymbol\mu_{\mathrm{mis}}+\Sigma_{\mathrm{mis},\mathrm{obs}}\,\Sigma_{\mathrm{obs},\mathrm{obs}}^{-1}\!\left(\mathbf{x}_{\mathrm{obs}}-\boldsymbol\mu_{\mathrm{obs}}\right),
```

with the parameters $`\boldsymbol\mu`$ and $`\Sigma`$ being re-computed at each step. However, if many of the variables are severely skewed or bounded, then the multivariate normality assumption may be unreasonable.

**SoftImpute**.

SoftImpute employs a soft-thresholded singular-value decomposition to estimate a low-rank representation of the original data matrix (Mazumder, Hastie, and Tibshirani 2010). It solves:

``` math
\label{eq:softimpute}
\min_{Z}\ \tfrac12\bigl\lVert P_\Omega(\mathbf{X}-Z)\bigr\rVert_F^2+\lambda\lVert Z\rVert_*,
```

where $`S_\lambda(Z)=U\operatorname{diag}\bigl((d_i-\lambda)_+\bigr)V^\top`$. Thus, $`\lambda`$ determines what percentage of the variation in $`Z`$ can be captured. Although SoftImpute is highly efficient for large sparse matrices, it could potentially ignore structure that does not fit within a low-rank model.

**Non-Negative Matrix Factorization (NMF)**.

Similarly to SoftImpute, NMF factorizes the data into two non-negative lower-rank matrices (Lee and Seung 1999):

``` math
\label{eq:nmf}
\min_{W\ge0,\,H\ge0}\ \bigl\lVert P_\Omega(\mathbf{X}-WH)\bigr\rVert_F^2,\qquad W\in\mathbb{R}^{n\times r}_{\ge0},\ H\in\mathbb{R}^{r\times p}_{\ge0}.
```

The non-negative constraints make sense in terms of neuropsychological scores since they cannot be less than zero. Additionally, the factors derived from NMF can sometimes be interpreted as additive contributions to cognition. Similar to SoftImpute, NMF works best when the data can be summarized by a small number of non-negative factors. Thus, choosing the correct rank $`r`$ is critical.

**Denoising Autoencoder (DAE)**.

A denoising autoencoder (DAE) trains a neural network to predict complete data given intentionally degraded versions of that data under the MIDA framework (Gondara and Wang 2018). Using encoder $`f_\theta`$, decoder $`g_\theta`$, and corrupted input $`\tilde{\mathbf{x}}`$, the goal is to minimize the reconstruction error:

``` math
\label{eq:dae}
\mathcal{L}_{\mathrm{DAE}}(\theta)=\mathbb{E}\bigl\lVert\mathbf{x}-g_\theta\!\left(f_\theta(\tilde{\mathbf{x}})\right)\bigr\rVert^2.
```

Thus, imputations are made by training multiple networks with varying random seed numbers and taking averages of their reconstructions. DAEs may outperform traditional methods when there are strong non-linear relationships among variables.

**Variational Autoencoder (VAE)**.

A variational autoencoder (VAE) constructs a probabilistic generative latent space model by mapping observations onto probability distributions (Kingma and Welling 2014; McCoy, Kroon, and Auret 2018). To maximize the evidence lower bound (ELBO):

``` math
\label{eq:vae}
\mathcal{L}_{\mathrm{VAE}}=\mathbb{E}_{q_\phi(z\mid x)}\!\left[\log p_\theta(x\mid z)\right]-\beta\,D_{\mathrm{KL}}\!\left(q_\phi(z\mid x)\,\big\Vert\,p(z)\right),
```

the prior is assumed to follow $`p(z)=\mathcal{N}(\mathbf{0},\mathbf{I})`$. Recently (Mattei and Frellsen 2019) proposed importance-weighted bounds for missing data while (Yoon, Jordon, and Schaar 2018) proposed a GAN-based approach. In VAEs, imputed values are produced via samples from the latent distribution followed by decodings of each sample, providing a natural mechanism for representing uncertainty if trained properly.

Deep learning methods typically require more computation than simple methods; however, they provide two potential benefits. They allow capturing non-linear structures without an explicit parametric model; additionally their stochastic elements - e.g., dropout in DAEs or latent sampling in VAEs - provide a natural mechanism for generating multiple imputations. Two disadvantages of deep learning methods are: sensitivity to overfitting and dependency upon architecture choices. This dissertation examines how well they function on the relatively small-to-medium sized low dimensional data characteristic of clinical neuropsychology (Prakash et al. 2024)

(Afkanpour et al. 2024) categorize imputation methods for clinical research into four classes: traditional methods (mean, EM, MICE); machine learning methods (KNN, MissForest); hybrid methods like PMM; and matrix completion methods like SoftImpute and NMF. I add a fifth class to these: Deep Learning - specifically for DAEs and VAEs. By comparing methods across these classes we can determine whether the recovered cognitive structure is stable across assumptions of the imputation method.

## Clustering in Neuropsychology

Clustering is a commonly employed statistical method within neuropsychology. A primary way of establishing clinical diagnoses or severity levels for patients who have experienced stroke, traumatic brain injury (TBI), or mild cognitive impairment (MCI) is to use diagnostic and/or severity categories. However, cluster analyses performed across different clinical groups, including TBI and MCI, show that statistically derived groupings of cognitive performance data do not always align with clinical diagnosis or severity level. From an empirical standpoint, this indicates that medical classifications used to represent cognitive heterogeneity after injury may fail to portray the full extent of that heterogeneity.

A review of data-driven cognitive phenotyping following brain injury was completed by (García-Rudolph et al. 2021). Several common findings emerged across the reviewed studies. First, most studies identified two to four data-driven cognitive groupings. Second, grouping was usually based on comparisons between relative cognitive strengths and weaknesses in relation to each individual’s overall level of cognitive functioning. Third, when applicable outcome measures were available, group membership was significantly associated with meaningful outcomes, such as return to work.

Despite these findings, several gaps remain in the literature on data-driven cognitive phenotyping following brain injury. Sample sizes in many studies range from approximately 100 to fewer than 200 participants. Missing values are often excluded from analyses through complete-case methods, even though this can bias the resulting sample when missingness is informative. Few studies systematically evaluate the algorithmic sensitivity of clustering methods. This is particularly relevant for k-means, a widely used clustering algorithm that requires users to determine the number of clusters, $`k`$, before analysing the data.

Consequently, this dissertation proposes four design features to address limitations in the existing literature. Chapter <a href="#Chapter3" data-reference-type="ref" data-reference="Chapter3">3</a> uses a larger clinical database; compares ten imputation methodologies against complete-case analysis; evaluates sensitivity to changes in hyperparameters and missingness thresholds; and uses HDBSCAN, which does not force outlier observations into predetermined centroids but instead identifies denser regions of observations as clusters.

## UMAP and HDBSCAN

There are two primary components to our clustering pipeline. First UMAP reduces the dimensionality of our data. Second HDBSCAN identifies dense regions of observations as clusters.

### UMAP

UMAP is a type of non-linear manifold learning that preserves the general topological features of the data while reducing higher-dimensional data into lower-dimensional spaces. As such, this method does not use linear techniques like PCA, but instead seeks out the geometry of the original data. There is always a trade-off between preserving both local and global structure in the data. Three primary hyperparameters used in UMAP can help to achieve an optimal balance between the two:

- `n_neighbors`: Number of neighbors to consider when drawing connections between original space objects. Higher values of `n_neighbors` create a larger-scale picture of the global properties of the data; conversely, lower values draw attention to the details of local structure.

- `min_dist`: Minimum distance required between objects within the new space. If set too large, object proximity may become less meaningful; if set too small, object proximity will be highly relevant.

- `n_components`: Target number of components in the new space.

Technically, UMAP works with a graph of weighted neighbors. For each pair of an object $`x_i`$ and one of its neighboring objects $`x_j`$, there exists a directed membership probability denoted by $`p_{j\mid i}`$. In Equation <a href="#eq:umap_p" data-reference-type="ref" data-reference="eq:umap_p">[eq:umap_p]</a>, $`\rho_i`$ denotes the distance from $`x_i`$ to its closest neighbor and $`\sigma_i`$ denotes a calibration factor such that $`\sum_j p_{j\mid i}=\log_2(k)`$, where $`k`$ is the value specified for `n_neighbors`. The directed probabilities are then made symmetric according to Equation <a href="#eq:umap_sym" data-reference-type="ref" data-reference="eq:umap_sym">[eq:umap_sym]</a>. Finally, in Equation <a href="#eq:umap_q" data-reference-type="ref" data-reference="eq:umap_q">[eq:umap_q]</a>, $`q_{ij}`$ defines the low-dimensional membership probability, with $`a`$ and $`b`$ being functions of `min_dist`. Next, UMAP minimizes the cross-entropy in Equation <a href="#eq:umap_ce" data-reference-type="ref" data-reference="eq:umap_ce">[eq:umap_ce]</a> between the high-dimensional and low-dimensional memberships.

``` math
\label{eq:umap_p}
p_{j\mid i}=\exp\!\left(-\frac{\max\{0,\,d(x_i,x_j)-\rho_i\}}{\sigma_i}\right),
```

``` math
\label{eq:umap_sym}
p_{ij}=p_{j\mid i}+p_{i\mid j}-p_{j\mid i}p_{i\mid j}.
```

``` math
\label{eq:umap_q}
q_{ij}=\left(1+a\,\lVert y_i-y_j\rVert_2^{2b}\right)^{-1},
```

``` math
\label{eq:umap_ce}
C=\sum_{i\ne j}\left[p_{ij}\log\frac{p_{ij}}{q_{ij}}+(1-p_{ij})\log\frac{1-p_{ij}}{1-q_{ij}}\right],
```

### HDBSCAN

HDBSCAN extends the capabilities of traditional DBSCAN by generating hierarchical representations of clusterings at varying levels of density and by identifying those aspects of the data that remain consistent across different clusterings. One major limitation of DBSCAN is that nested or variable-density clusters are difficult to recover from a single fixed neighbourhood radius. HDBSCAN addresses this issue directly by defining noise and allowing for automatic determination of the number of clusters. Key parameters include:

- `min_samples`: Density estimate parameter.

- `min_cluster_size`: Smallest acceptable cluster size.

- `cluster_selection_epsilon`: Specifies how aggressively clusters should be merged.

In addition to adjusting distance measurements based on local density, HDBSCAN also uses mutual reachability distance as defined in Equation <a href="#eq:mreach" data-reference-type="ref" data-reference="eq:mreach">[eq:mreach]</a> to connect pairs of objects. An MST is generated over these adjusted distances to form the basis for a hierarchical representation. Each node in this tree corresponds to either an object or a previously formed cluster. Persistent clusters are then selected based on their stability as described in Equation <a href="#eq:hdbscan_stab" data-reference-type="ref" data-reference="eq:hdbscan_stab">[eq:hdbscan_stab]</a>, where $`\lambda_{\mathrm{birth}}(C)`$ represents the density level at which cluster $`C`$ was created and $`\lambda_{\max}(x,C)`$ represents the highest density level at which point $`x`$ remained part of cluster $`C`$. Any remaining points that do not belong to any persistent cluster are designated as noise.

``` math
\label{eq:mreach}
d_{\mathrm{mreach}}(a,b)=\max\bigl\{\operatorname{core}_k(a),\,\operatorname{core}_k(b),\,d(a,b)\bigr\}.
```

``` math
\label{eq:hdbscan_stab}
S(C)=\sum_{x\in C}\bigl(\lambda_{\max}(x,C)-\lambda_{\mathrm{birth}}(C)\bigr),\qquad \lambda=\frac{1}{d_{\mathrm{mreach}}},
```

Both UMAP and HDBSCAN have found widespread applications throughout computational biology and related fields because they can effectively discover structural elements in very-high-dimensional datasets.

## Cluster Validation

When a gold standard is absent, assessing the validity of discovered clusters is indirect. Henceforth, we employ a combination of internal validations, external consistency measurements and sensitivity analyses.

### Internal Validation

Internal validation involves comparing various attributes of different possible cluster solutions. Here we primarily rely on silhouette coefficients (Rousseeuw 1987), which compare within-cluster cohesion (the average similarity of each data-point to the other data-points in its own cluster) and between-cluster separation (the average similarity between each data-point and data-points outside its cluster). The silhouette value for an individual item lies in the interval \[-1,+1\]: Positive values denote good fit, values close to zero signify poor fit (as either an item fits poorly into its own group or fits very well into adjacent group(s)), and negative values represent incorrect assignment. The individual silhouette value is defined in Equation <a href="#eq:silhouette" data-reference-type="ref" data-reference="eq:silhouette">[eq:silhouette]</a>, where $`a(i)`$ denotes the mean intra-cluster dissimilarity for observation $`i`$, and $`b(i)`$ denotes the mean dissimilarity between observation $`i`$ and members of the nearest alternative cluster. The average silhouette is then obtained by taking the mean of $`s(i)`$ across all observations. As previously stated, we utilize the mean silhouette as our principal internal evaluation measure. Noise percentage is our second measure of evaluating how much of our total population is clustered in meaningful ways.

``` math
\label{eq:silhouette}
s(i)=\frac{b(i)-a(i)}{\max\{a(i),\,b(i)\}}.
```

### External Validation

Measuring two different cluster solutions, e.g., when examining how consistent cluster assignments are between two different imputation methods, necessitates the employment of external validation measures. One common method is the Adjusted Rand Index (ARI) (Hubert and Arabie 1985). The ARI examines how many pairs of cases have been assigned to identical clusters across two separate clusterings and then adjusts this count for chance. Let $`U = \{U_i\}`$ and $`V = \{V_j\}`$ be two clusterings of $`n`$ objects with contingency counts $`n_{ij} = |U_i \cap V_j|`$, marginal sums $`a_i = \sum_j n_{ij}`$ and $`b_j = \sum_i n_{ij}`$. The ARI is calculated using Equation <a href="#eq:ari" data-reference-type="ref" data-reference="eq:ari">[eq:ari]</a>; +1 represents perfect agreement, 0 represents random agreement, and values below 0 demonstrate systematic disagreement (Robert, Vasseur, and Brault 2020). Next, we calculate Normalized Mutual Information (NMI), a mutual-information-theoretic method of quantifying how much one clustering discloses regarding another clustering normalized by entropy. Specifically, using mutual information $`I(U;V)`$ and Shannon entropies $`H(\cdot)`$ (Shannon 1948), Equation <a href="#eq:nmi" data-reference-type="ref" data-reference="eq:nmi">[eq:nmi]</a> defines full agreement as 1 and no agreement as 0.

For an additional insight into individual clusters’ similarities/differences, we apply the Jaccard index. If $`A`$ and $`B`$ denote sets containing points that make up a specific cluster under two respective solutions, the Jaccard index is computed using Equation <a href="#eq:jaccard" data-reference-type="ref" data-reference="eq:jaccard">[eq:jaccard]</a>; thus values lie in \[0, 1\], with larger values demonstrating closer membership. Finally, we use Hennig Matching (Hennig 2007) as a bootstrapping method of assessing cluster stability. Across $`R`$ bootstrap iterations, we pair each original cluster $`C_k`$ with the resampled cluster whose Jaccard overlap with it is maximal. The stability score of each original cluster $`C_k`$ is then taken as the mean of these maxima in Equation <a href="#eq:hennig" data-reference-type="ref" data-reference="eq:hennig">[eq:hennig]</a>. By convention, a per-cluster score \> 0.7 is considered stable.

Collectively, NMI and ARI evaluate whether two cluster solutions exhibit significant substantive agreement.

``` math
\label{eq:ari}
\mathrm{ARI}=\frac{\displaystyle\sum_{ij}\binom{n_{ij}}{2}-\Bigl[\sum_i\binom{a_i}{2}\sum_j\binom{b_j}{2}\Bigr]\Big/\binom{n}{2}}{\displaystyle\tfrac12\Bigl[\sum_i\binom{a_i}{2}+\sum_j\binom{b_j}{2}\Bigr]-\Bigl[\sum_i\binom{a_i}{2}\sum_j\binom{b_j}{2}\Bigr]\Big/\binom{n}{2}}.
```

``` math
\label{eq:nmi}
\mathrm{NMI}(U,V)=\frac{2\,I(U;V)}{H(U)+H(V)},
```

``` math
\label{eq:jaccard}
J(A,B)=\frac{|A\cap B|}{|A\cup B|}.
```

``` math
\label{eq:hennig}
\hat{S}_k=\frac{1}{R}\sum_{r=1}^{R}\max_{k'}\,J\!\left(C_k,\,C_{k'}^{(r)}\right).
```

# Methodology

## Data Description

Data originates from a clinical neuropsychology database managed by a rehabilitation center. Raw data includes 22,075 records from 8,739 unique individuals with repeated follow-up assessments. Each assessment consists of 31 features relating to demographics/administrative details/injury specifics/neuropsychological results across six cognitive domains: Orientation/Attention/Visuospatial Perception/Language/Memory/Executive Function. Following Tier-1 filtering (described in Section <a href="#sec:filtering" data-reference-type="ref" data-reference="sec:filtering">3.2</a>), our analyzed dataset contains 17,406 assessments from 7,285 subjects.

Given that these data originate from routine clinical practice rather than a specifically constructed research protocol, test selection was influenced by both the neuropsychologist conducting testing/referral questions/patient engagement capabilities. Therefore, missingness in our dataset is structured. Certain measures appear in almost every assessment; however, some are only available in response to certain clinical circumstances. Unlike missingness originating from research protocols that may control missingness through design; missingness in this dataset varies greatly; ranging from approximately 5% for screening tools to over 90% for specialty assessments.

Additionally, measures fall along varying scales (standardized z-scores/scaled scores/raw timed measures). During domain aggregation (Section <a href="#sec:domain_scores" data-reference-type="ref" data-reference="sec:domain_scores">3.4</a>), these scales were unified. In Table <a href="#tab:missing_descriptive" data-reference-type="ref" data-reference="tab:missing_descriptive">4.1</a>, we display missingness distribution for our fourteen candidate variables. Only 53.1% (9,245 assessments) of our 17,406 records contained complete data across all fourteen variables; if we applied listwise deletion, 46.9% (8,161 assessments) of our sample could potentially be lost as a consequence of our inability to analyze this portion of our dataset. Our imputation strategy (Section <a href="#sec:imputation" data-reference-type="ref" data-reference="sec:imputation">3.3</a>) is intended to avoid losing clinical information associated with this portion of our sample.

All data have undergone deidentification according to established standards for protecting patient privacy.

## Tier 1 Filtering

Since many variables in our dataset exhibit large amounts of missingness, we performed filtering prior to performing imputation/clustering. In general, our primary analysis employs a fifty-percent filter. Any variable that exhibits more than fifty percent missingness is eliminated; any record exhibiting more than fifty percent missingness among remaining variables is eliminated.

Our choice represents a compromise between maximizing data retention versus minimizing the amount of missingness placed on imputation models. While employing a seventy-percent filter would retain significantly more records/variables; this would increase the likelihood that artificial structure exists in our imputed data. Conversely, employing a thirty-percent filter would likely produce a clean matrix; however, it would eliminate substantially more clinically relevant records while reducing analytical capability.

We perform sensitivity analyses utilizing filters between thirty percent and seventy percent in Section <a href="#sec:robustness" data-reference-type="ref" data-reference="sec:robustness">4.10</a>.

Following application of this filter and elimination of assessments without documented cognitive testing, our dataset contains fourteen neuropsychological variables; seventeen thousand four hundred-six assessments from seven thousand two-hundred-eighty-five patients.

<div id="tab:eligible_vars">

| **Cognitive Domain** | **Variables** | **Count** |
|:---|:---|:--:|
| Orientation | `OPERSONA`, `OESPAI`, `OTEMPS` | 3 |
| Attention | `ASPAN`, `ATMTA` | 2 |
| Visuoperception | `VPIMATGES` | 1 |
| Language | `LREPETICIOTB`, `LDENOMINACIOTB`, `LCOMPRENSIOTB` | 3 |
| Memory | `MDIGITS`, `MRAVLT075`, `MRAVLT015`, `MRAVLT015R` | 4 |
| Executive Function | `FEPMR` | 1 |
| **Total** |  | **14** |

Eligible neuropsychological variables after Tier 1 filtering, organised by cognitive domain.

</div>

## Imputation Methods

The next part of this section presents the ten different types of multiple imputation methods, grouped into the five categories outlined previously. For clustering performance, both silhouette score and number of clusters $`k`$, I chose the optimal combination of UMAP+HDBSCAN using the domain-level features. The silhouette value calculated here is based only on the high-density region clustered by HDBSCAN before performing the $`k`$-nearest-neighbour noise-assignment process. Consequently, the silhouette value is somewhat higher than reported in the literature for fully covered assessments (see Section <a href="#sec:h1_results" data-reference-type="ref" data-reference="sec:h1_results">4.5</a>); for example, MICE achieved 0.598 in the high-density area before reassignment and 0.526 when assessed across all assigned cases.

The two deep learning methods required additional training choices, so their technical details are specified here. For the denoising autoencoder (DAE), deliberately corrupted inputs were generated by masking the observed values. The corruption mask was sampled as follows:

``` math
\label{eq:dae_corrupt}
\mathbf{m}_i\sim
\begin{cases}
P_{\mathrm{miss}} & \text{with probability } 0.5,\\[2pt]
\operatorname{Bernoulli}(1-\rho)^{\otimes p} & \text{with probability } 0.5,
\end{cases}
```

where $`P_{\mathrm{miss}}`$ denotes the empirical distribution of missingness patterns and $`\rho`$ denotes the uniform corruption rate. This scheme allows the DAE to learn from random corruption as well as from missingness structures that resemble those observed in the clinical data.

For the variational autoencoder (VAE), cyclical annealing was used for the $`\beta`$ term in the evidence lower bound. The annealing schedule was:

``` math
\label{eq:beta_cyclical}
\beta(t)=\beta_{\max}\,\frac{t \bmod T}{T},\qquad T=40,\ \beta_{\max}=0.1,
```

The deep-learning imputations were evaluated by holding out a subset $`H`$ of observed entries and comparing the imputed values with the original values. Root mean square error and mean absolute error were computed as:

``` math
\label{eq:rmse}
\mathrm{RMSE}=\sqrt{\frac{1}{|H|}\sum_{(i,j)\in H}\bigl(\hat{x}_{ij}-x_{ij}\bigr)^2},\qquad
\mathrm{MAE}=\frac{1}{|H|}\sum_{(i,j)\in H}\bigl|\hat{x}_{ij}-x_{ij}\bigr|.
```

<div id="tab:method_summary">

| **Category** | **Method** | **Year** | **$`k`$** | **Sil.** | **Advantages** | **Limitations** |
|:---|:---|:--:|:--:|:--:|:---|:---|
| Conventional | Mean | — | 4 | 0.604 | Simplest; fast; universal baseline | Collapses variance & covariance |
| Statistical | EM | 1977 | 4 | 0.587 | Principled MLE; preserves covariance | Assumes multivariate normality |
|  | MICE | 2011 | 3 | 0.598 | Flexible; preserves distribution | Requires model per variable |
| Machine | KNN | 2001 | 4 | 0.576 | Non-parametric; captures local structure | Sensitive to $`k`$; slow for large $`n`$ |
| Learning | MissForest | 2012 | 3 | 0.606 | Non-linear; handles mixed types | Computationally expensive |
| Hybrid | PMM | — | 4 | 0.498 | Preserves marginal distribution | Requires adequate donor pool |
| Matrix | SoftImpute | 2010 | 4 | 0.571 | Efficient for sparse matrices | Assumes low-rank structure |
| Completion | NMF | 1999 | 3 | 0.546 | Non-negativity natural for scores | Sensitive to rank choice |
| Deep | DAE | 2018 | 5 | 0.510 | Non-linear; multiple imputations | Requires hyperparameter tuning |
| Learning | VAE | 2014 | 4 | 0.603 | Probabilistic; principled uncertainty | Complex training; $`\beta`$-tuning |

A summary of the ten imputation methods broken down by the five-category taxonomy. The clustering performance columns report the optimal UMAP+HDBSCAN solution on domain-level features, using the high-density HDBSCAN core before $`k`$-nearest-neighbour noise assignment.

</div>

*References:* Little and Rubin (Little and Rubin 2019); PMM and MICE (Buuren and Groothuis-Oudshoorn 2011); EM (Dempster, Laird, and Rubin 1977); KNN (Troyanskaya et al. 2001); MissForest (Stekhoven and Bühlmann 2012); SoftImpute (Mazumder, Hastie, and Tibshirani 2010); NMF (Lee and Seung 1999); DAE (Gondara and Wang 2018); VAE (Kingma and Welling 2014; McCoy, Kroon, and Auret 2018).

## Calculating Scores for Each Cognitive Domain

A set of cognitive-domain-level features was created to represent aggregate versions of the variables related to each cognitive domain, while retaining the same 14 individual neuropsychological variables for comparison. Since many of the original measures are recorded on different scales (e.g., standardised scores versus scaled scores), direct aggregation may create scale-related problems unless scale alignment is performed first. To reduce potential problems from extreme imputations caused by outliers or sentinel codes, three processing steps were applied to each variable before aggregation:

1.  Winsorizing each variable over the 1st to 99th percentile range.

2.  Reversing the sign of all timed test results, so that positive values indicate better performance.

3.  Standardising all variables to a mean of 0 and variance of 1.

Reliability-weighted averages of variables representing each domain were then used as domain scores. Reliability weights ($`w_j = 1 - r_j`$, where $`r_j`$ represents the missingness rate) were assigned to each variable $`j`$. These weights were then normalised within domains. Thus, variables administered more frequently contribute proportionately more heavily to their respective domain-level composite scores. By reducing dimensionality from 14 individual variables to six domain-level scores, the number of variables available for distance-based algorithms is reduced, improving feature-space geometry. Furthermore, creating domain-level profiles facilitates clinical conceptualisation of cognitive deficit in relation to cognitive domains rather than individual variables. Some detail is sacrificed. For example, two patients could obtain equal average memory scores while differing in immediate versus delayed recall. Whether there is sufficient rationale for sacrificing this detail in exchange for improved stability and interpretability is assessed in Hypothesis H4.

## UMAP + HDBSCAN Pipeline

Figure <a href="#fig:pipeline_diagram" data-reference-type="ref" data-reference="fig:pipeline_diagram">3.1</a> shows the end-to-end process from imputed data to final cluster assignment. Prior to performing dimensional reduction using UMAP/HDBSCAN, we apply robust scaling using the median and interquartile range to reduce influence of floor and ceiling effects common in neuropsychological assessment (Bellio et al. 2020; Pinsky and Klawansky 2023). Floor effects occur when severely impaired patients accumulate at minimum values for an assessment tool (Pinsky and Klawansky 2023), whereas ceiling effects occur when patients with no impairments accumulate at maximum values (Pinsky and Klawansky 2023). Scale-free metrics like median and inter-quartile ranges help mitigate these effects. For each of the twenty imputed datasets (ten methods $`\times`$ two feature representations), we perform UMAP followed by HDBSCAN. Like other machine learning algorithms that rely heavily on initial conditions (in this case, random initialization), UMAP is stochastic. Therefore, a single embedding could capture variability due to either random initialization or geometric properties of the data. Therefore, we repeat each hyperparameter combination ten times and choose the embedding with highest silhouette score (based on initial HDBSCAN clustering).

<figure id="fig:pipeline_diagram">

<figcaption>This is an end-to-end clustering pipeline. Once the data have been imputed, they first pass through a robust scaler. Next, after being scaled, the imputed data pass into a UMAP hyperparameter grid with 10 random seeds for each of nine configurations, and the resulting embeddings that yield the highest silhouette value are retained. HDBSCAN then does the clustering in a 120-configuration sweep, based upon the composite quality measure <span class="math inline"><em>Q</em> = silhouette × (1 − noise fraction)</span>, where all boundary noise points are assigned back to their respective cluster(s) via k-nearest neighbour. This entire process is run over each of the 10 possible imputation outcomes.</figcaption>
</figure>

### UMAP Parameter Grid

We utilized Euclidean distance as our distance metric and `min_dist`$`=0.0`$ to encourage separation between dense areas in our embedding.

<div id="tab:umap_grid">

| **Parameter**  | **Values** |
|:---------------|:-----------|
| `n_neighbors`  | 15, 30, 50 |
| `min_dist`     | 0.0        |
| `n_components` | 3, 5, 8    |

UMAP hyperparameter grid. All combinations of these values were put through their paces, for a total of 9 configurations.

</div>

### HDBSCAN Parameter Grid

Each UMAP embedding produced 120 possible candidate solutions (due to 120 different possible HDBSCAN configurations). To determine which configuration was "best," we employed a composite quality score that punished solutions with high silhouettes by allocating many assignments to noise:

``` math
Q = \text{silhouette} \times (1 - \text{noise proportion})
\label{eq:quality}
```

<div id="tab:hdbscan_grid">

| **Parameter**               | **Values**                  |
|:----------------------------|:----------------------------|
| `min_cluster_size`          | 500, 1000, 1500, 2000, 3000 |
| `min_samples`               | 5, 10, 25, 50               |
| `cluster_selection_method`  | eom, leaf                   |
| `cluster_selection_epsilon` | 0.0, 0.1, 0.5               |

HDBSCAN hyperparameter grid. All listed value combinations were evaluated, giving me 120 configurations for each UMAP embedding.

</div>

### Sweep Procedure

The following procedures were employed for each imputed dataset: First, we preprocessed each dataset using a robust scaler. Second, we conducted a ten-fold cross-validation on each UMAP hyperparameter combination (yielding ten embeddings per combination). From these ten embeddings, we chose the best embedding based on silhouette score. Third, we conducted a 120-fold cross-validation on each HDBSCAN configuration and selected the configuration yielding the best-quality score $`Q`$. Fourth, we re-labeled any observations previously labeled as noise. In doing so, noise points assigned by HDBSCAN are relocated to the nearest substantively clustered group based on k-nearest neighbor ($`k = 10`$) similarity in UMAP-space. Given that residual noise is negligible on these features, this process yields 100% coverage and thus assigns labels to every assessment. Re-labeling is only allowed if silhouettes decrease by less than 10%, maintaining separations between clusters.

### Worked Example

Assume a hypothetical patient completes only those neuropsychological assessments related to orientation and digit span but fails to complete those related to Trail Making Test due to physical limitations or the delayed recall portion of the Rey Auditory Verbal Learning Test due to exhaustion. Upon application of Tier 1 filtering, however, the patient remains in the dataset with eligible variables only. The two missing scores are subsequently filled in by MICE based on observed information. The 14 variable-level scores are then subjected to winsorizing, aligned for direction, standardized, and weighted as defined in Section <a href="#sec:domain_scores" data-reference-type="ref" data-reference="sec:domain_scores">3.4</a> to produce six domain-composite scores. The robust scaler is applied to minimize the effect that floor and ceiling effects may have on aggregate measures. The resulting six-dimensional vector is then mapped into the cohort’s UMAP representation space. The patient is then classified into one of three cognitive-severity tiers: Above Average, Near Normal, or Globally Impaired. If a patient falls into a sparse area of low density and was classified as noise, KNN reassignment utilizes neighboring assessments in UMAP-space ($`k = 10`$) and assigns them to the most closely located substantively-clustered tier. The final output includes a tier label and confidence score based on how often each imputation method agrees under hypothesis H2.

## Hypothesis Definitions

**H1 (Existence of Cognitive Clusters)**. The UMAP + HDBSCAN pipeline will likely find at least two distinct, stable cognitive clusters for most imputation techniques. The existence of these clusters can be demonstrated as long as the best solution from at least 8 of the 10 different methods has both characteristics: average silhouette $`\geq`$ 0.40 and percentage of noisy points $`< 0.30`$. Since we allow some method-specific failures, the 80% criterion provides a margin for error.

**H2 (Robustness Across Imputation Techniques)**. Solutions for the clustering problems should show reasonable to high agreement among the imputation methods when the embedding geometry and partition model are held fixed. The primary discovery pipeline remains UMAP+HDBSCAN. For H2 only, I use a deliberately fixed secondary agreement diagnostic: a $`k`$-means labelling rule is trained on the MICE embedding and then applied unchanged to all other imputations. H2 is confirmed if the median pairwise ARI and NMI for each of the $`\binom{10}{2} = 45`$ combinations of methods exceeds 0.50. Although there is considerable flexibility in setting this threshold, it is greater than chance and implies substantial overlap in group membership under a common projection and labelling rule. This hypothesis therefore tests robustness of point assignments under a fixed reference structure; it does not require, or claim, that independently refitted UMAP+HDBSCAN solutions recover the identical number of tiers.

**H3 (Relationship Between Clinical Unit & Cluster Membership)**. Cluster membership is expected to be related to clinical unit. For each imputation technique, a contingency table is created and a chi-square test of independence is conducted. H3 is confirmed if the relationship remains statistically significant at $`\alpha = 0.05`$ after a Bonferroni adjustment and Cramér’s $`V > 0.10`$. As a sensitivity check for potential confounds, a Cochran-Mantel-Haenszel (CMH) test is performed, conditioned on an appropriate covariate.

**H4 (Clustering at Domain-Level vs. At Variable Level)**. I expect the cognitive features at the domain level to result in a clustering representation that is more interpretable and at least as well separated as the representation based on cognitive features at the variable level. H4 will be confirmed if the domain-level approach performs at least as well as or better than the variable-level approach on at least two of three metrics: (1) higher silhouette scores; (2) lower mean VIFs; and (3) lower condition numbers. Smaller values of VIF and condition number imply less multicollinearity and better numerical conditioning. Because cross-method agreement has already been assessed in H2, comparisons of feature representations are made in H4 exclusively.

## Statistical Tests and Validation

### Statistical Conventions

Each statistical evaluation of hypotheses follows typical statistical practice. Each evaluation assesses the data relative to a null hypothesis $`H_0`$, representing a "no-effect" baseline. The p-value is the probability of obtaining a test statistic as extreme as that obtained assuming $`H_0`$ to be true; smaller p-values represent stronger evidence against $`H_0`$. A predetermined significance level of $`\alpha = 0.05`$ serves as the threshold for rejecting $`H_0`$. For any parameter, a 95% CI represents the range that would include the population parameter in 95% of repeated random samples from the same population using the same methodology.

For applications of bootstrapping, observed data are randomly sampled with replacement to generate a simulated approximation of the sampling distribution of a statistic. The 2.5th and 97.5th percentiles of that simulated distribution define the bootstrap CI. A z-score quantifies how many standard deviations away from the mean of a specified reference distribution a given value lies. With respect to the psychological testing instruments employed here, standardized testing permits scores derived from different instruments to be compared.

Cohen defined standards for interpreting the magnitude of effects, specifically for standardized differences, i.e., Cohen’s $`d`$. Specifically, $`d = 0.20`$ is interpreted as a small effect size, $`d = 0.50`$ as a medium-sized effect, and $`d = 0.80`$ as a large effect size. When applying Cramér’s V as an effect size for evaluating chi-squared tests, $`V = 0.10`$ is interpreted as a small effect size, $`V = 0.30`$ as a medium effect size, and $`V = 0.50`$ as a large effect size.

``` math
\label{eq:cohend}
d=\frac{\bar{x}_1-\bar{x}_2}{s_p},\qquad s_p=\sqrt{\frac{(n_1-1)s_1^2+(n_2-1)s_2^2}{n_1+n_2-2}},
```

### Tests and Validation Procedures

**Bootstrap Stability**. I conduct a bootstrap stability analysis for every imputation method using $`B = 50`$ resamplings. For each resampling, I refit HDBSCAN on the cached UMAP embeddings, recording the median silhouette (Eq. <a href="#eq:silhouette" data-reference-type="ref" data-reference="eq:silhouette">[eq:silhouette]</a>) and pre-KNN noise proportions. Pre-KNN noise proportion is equal to the proportion of observations that do not belong to any meaningful cluster:

``` math
\label{eq:noise}
\text{noise}=\frac{1}{n}\bigl|\{\,i:\text{label}(i)=\text{noise}\,\}\bigr|,
```

This is also the value used in defining quality function $`Q`$ (Eq. <a href="#eq:quality" data-reference-type="ref" data-reference="eq:quality">[eq:quality]</a>). According to H1’s pre-defined conditions, a method will be deemed successful if its median silhouette is larger than or equal to 0.40 and its pre-KNN noise proportion is less than or equal to 0.30; at least 8 of the 10 methods will need to satisfy both conditions. To evaluate per-cluster stability, I apply Hennig (2007)’s matching algorithm to the pre-KNN labels using the default threshold (i.e., 0.7).

**Pairwise Agreement**. In order to remove variability caused by refitting other parts of the pipeline, I employ a shared reference-pipeline strategy. This is a secondary sensitivity analysis, not the clustering procedure used to discover the primary tiers. One StandardScaler, one UMAP model, and one $`k`$-means model with $`k=3`$ are trained on MICE-imputed domain scores. The remaining methods are then standardized, projected onto this MICE-trained pipeline, and classified using that same MICE-trained $`k`$-means model. The use of $`k`$-means here is intentional: it supplies a fixed labelling function so that the imputed values are the only element varying across methods. This design tests whether assessments produced by different imputation methods land in similar regions under a fixed embedding and partition; it does not test whether a newly fitted UMAP+HDBSCAN pipeline would reconstruct the same geometry, density hierarchy, or number of tiers from each imputed dataset. It creates the ARI (Eq. <a href="#eq:ari" data-reference-type="ref" data-reference="eq:ari">[eq:ari]</a>) and NMI (Eq. <a href="#eq:nmi" data-reference-type="ref" data-reference="eq:nmi">[eq:nmi]</a>) matrices comparing each method to each other shown as heatmaps in Chapter <a href="#Chapter4" data-reference-type="ref" data-reference="Chapter4">4</a>. Confidence for each assessment is defined as:

``` math
\label{eq:consensus}
\mathrm{conf}(i)=\max_{\ell}\frac{1}{M}\sum_{m=1}^{M}\mathbf{1}\!\left[\text{label}_m(i)=\ell\right],
```

High-confidence assessments are those whose assessments were placed into the mode cluster by at least $`M/10 = 0.8 \times 10 = 8`$ methods.

**Chi-Square Test, Cramér’s V, CMH Test**. Contingency tables arise from cross-classifying two categorical variables - e.g., cluster assignment and clinical unit - giving joint counts. Pearson’s Chi-Square Test evaluates observed counts $`O_{ij}`$ against expected counts $`E_{ij}`$ under the null hypothesis that the two variables are independent:

``` math
\label{eq:chi2}
\chi^2=\sum_{i=1}^{r}\sum_{j=1}^{c}\frac{(O_{ij}-E_{ij})^2}{E_{ij}},\qquad E_{ij}=\frac{O_{i\cdot}\,O_{\cdot j}}{n},
```

with $`O_{i\cdot}`$ and $`O_{\cdot j}`$ denoting row sums and column sums, respectively. The test statistic is referenced against a Chi-Square distribution with $`(r - 1)(c - 1)`$ degrees of freedom to yield the p-value. Cramér’s V is used to render association statistics scale-free for sample-size purposes, since it takes on values between zero and one:

``` math
\label{eq:cramersv}
V=\sqrt{\frac{\chi^2}{n\,(k-1)}},\qquad k=\min(r,c),
```

The Cochran-Mantel-Haenszel Test extends Pearson’s Chi-Square Test for data organized into strata (e.g., diagnosis subgroups). The CMH Test determines whether the association between cluster assignments and clinical units remains significant even when stratifying by an appropriate covariate:

``` math
\label{eq:cmh}
\chi^2_{\mathrm{CMH}}=\frac{\bigl(\sum_{h}(a_h-\mathbb{E}[a_h])\bigr)^2}{\sum_{h}\operatorname{Var}(a_h)}.
```

**Variance Inflation Factor**. To quantify multicollinearity in regression models, VIF is used. For any variable $`j`$, it is defined as:

``` math
\label{eq:vif}
\mathrm{VIF}_j=\frac{1}{1-R_j^2},
```

where $`R_j^2`$ denotes the coefficient of determination when regressing $`j`$ on all other predictors. Any value exceeding 10 constitutes grounds for concern, and influences interpretation both at the variable level and in subsequent analyses at the domain level.

### Implementation

All analyses were implemented in Python (version 3.13). Imputation used `scikit-learn` (KNN, NMF), `fancyimpute` (SoftImpute, EM), `miceforest` (MICE, PMM), and `missforest` (MissForest). DAE and VAE used `PyTorch`. UMAP used `umap-learn`; HDBSCAN used the `hdbscan` library. Statistical tests used `scipy.stats` and `statsmodels`. Validation metrics used `scikit-learn`. The full source code, notebooks, and dashboard are available at <https://github.com/zkunos/thesis_project>.

# Results

## Exploratory Data Analysis

Following Tier-1 filtering (Chapter <a href="#Chapter3" data-reference-type="ref" data-reference="Chapter3">3</a>) and removal of all assessments lacking any cognitive measures, the remaining dataset consisted of 17,406 assessments from 7,285 patients. The resulting matrix included cognitive variables amounting to 14 variables over six domains. The percentages of missing values are provided in Table <a href="#tab:missing_descriptive" data-reference-type="ref" data-reference="tab:missing_descriptive">4.1</a>.

Data availability is inconsistent. The missingness levels vary from 0.7% for Orientation items through to 27.8% for ATMTA. Therefore, complete-case analysis would lose approximately half of the total clinical sample (46.9%) and introduce clear selection bias (Rubin 1976). Consequently, data imputation was adopted to conserve the entire clinical sample.

From a co-occurrence heatmap (not shown), blocks of variables are identified that are missing simultaneously, suggesting a missing-at-random mechanism (Rubin 1976; Little and Rubin 2019). Dependency among missing values thus supports the application of conditional imputation rather than naive substitution. Within-domain correlation coefficients are generally high, whereas cross-domain relationships appear less prominent, suggesting common variance due to general cognitive ability (Lezak et al. 2012). Subsequent clustering results illustrate this common variance dimension explicitly.

<div id="tab:missing_descriptive">

<table>
<caption>Missingness summary for the 14 eligible neuropsychological variables after Tier 1 filtering. The final row reports the number of complete cases (rows with no missing values across all 14 variables).</caption>
<thead>
<tr>
<th style="text-align: left;"><strong>Variable</strong></th>
<th style="text-align: left;"><strong>Domain</strong></th>
<th style="text-align: right;"><strong><span class="math inline"><em>N</em></span> Observed</strong></th>
<th style="text-align: right;"><strong><span class="math inline"><em>N</em></span> Missing</strong></th>
<th style="text-align: right;"><strong>Missing %</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><code>OTEMPS</code></td>
<td style="text-align: left;">Orientation</td>
<td style="text-align: right;">17<span>,</span>286</td>
<td style="text-align: right;">120</td>
<td style="text-align: right;">0.7</td>
</tr>
<tr>
<td style="text-align: left;"><code>OPERSONA</code></td>
<td style="text-align: left;">Orientation</td>
<td style="text-align: right;">17<span>,</span>284</td>
<td style="text-align: right;">122</td>
<td style="text-align: right;">0.7</td>
</tr>
<tr>
<td style="text-align: left;"><code>OESPAI</code></td>
<td style="text-align: left;">Orientation</td>
<td style="text-align: right;">17<span>,</span>282</td>
<td style="text-align: right;">124</td>
<td style="text-align: right;">0.7</td>
</tr>
<tr>
<td style="text-align: left;"><code>ASPAN</code></td>
<td style="text-align: left;">Attention</td>
<td style="text-align: right;">15<span>,</span>611</td>
<td style="text-align: right;">1<span>,</span>795</td>
<td style="text-align: right;">10.3</td>
</tr>
<tr>
<td style="text-align: left;"><code>MRAVLT075</code></td>
<td style="text-align: left;">Memory</td>
<td style="text-align: right;">15<span>,</span>523</td>
<td style="text-align: right;">1<span>,</span>883</td>
<td style="text-align: right;">10.8</td>
</tr>
<tr>
<td style="text-align: left;"><code>MDIGITS</code></td>
<td style="text-align: left;">Memory</td>
<td style="text-align: right;">15<span>,</span>373</td>
<td style="text-align: right;">2<span>,</span>033</td>
<td style="text-align: right;">11.7</td>
</tr>
<tr>
<td style="text-align: left;"><code>FEPMR</code></td>
<td style="text-align: left;">Executive Function</td>
<td style="text-align: right;">14<span>,</span>682</td>
<td style="text-align: right;">2<span>,</span>724</td>
<td style="text-align: right;">15.6</td>
</tr>
<tr>
<td style="text-align: left;"><code>LCOMPRENSIOTB</code></td>
<td style="text-align: left;">Language</td>
<td style="text-align: right;">14<span>,</span>686</td>
<td style="text-align: right;">2<span>,</span>720</td>
<td style="text-align: right;">15.6</td>
</tr>
<tr>
<td style="text-align: left;"><code>LDENOMINACIOTB</code></td>
<td style="text-align: left;">Language</td>
<td style="text-align: right;">14<span>,</span>677</td>
<td style="text-align: right;">2<span>,</span>729</td>
<td style="text-align: right;">15.7</td>
</tr>
<tr>
<td style="text-align: left;"><code>LREPETICIOTB</code></td>
<td style="text-align: left;">Language</td>
<td style="text-align: right;">14<span>,</span>634</td>
<td style="text-align: right;">2<span>,</span>772</td>
<td style="text-align: right;">15.9</td>
</tr>
<tr>
<td style="text-align: left;"><code>MRAVLT015</code></td>
<td style="text-align: left;">Memory</td>
<td style="text-align: right;">14<span>,</span>281</td>
<td style="text-align: right;">3<span>,</span>125</td>
<td style="text-align: right;">18.0</td>
</tr>
<tr>
<td style="text-align: left;"><code>MRAVLT015R</code></td>
<td style="text-align: left;">Memory</td>
<td style="text-align: right;">14<span>,</span>199</td>
<td style="text-align: right;">3<span>,</span>207</td>
<td style="text-align: right;">18.4</td>
</tr>
<tr>
<td style="text-align: left;"><code>VPIMATGES</code></td>
<td style="text-align: left;">Visuoperception</td>
<td style="text-align: right;">12<span>,</span>992</td>
<td style="text-align: right;">4<span>,</span>414</td>
<td style="text-align: right;">25.4</td>
</tr>
<tr>
<td style="text-align: left;"><code>ATMTA</code></td>
<td style="text-align: left;">Attention</td>
<td style="text-align: right;">12<span>,</span>575</td>
<td style="text-align: right;">4<span>,</span>831</td>
<td style="text-align: right;">27.8</td>
</tr>
<tr>
<td colspan="3" style="text-align: left;"><strong>Complete cases (all 14 variables observed)</strong></td>
<td colspan="2" style="text-align: right;"><strong>9<span>,</span>245 (53.1%)</strong></td>
</tr>
</tbody>
</table>

</div>

In Figure <a href="#fig:missingness_barplot" data-reference-type="ref" data-reference="fig:missingness_barplot">4.1</a>, missingness levels for each cognitive variable are displayed in descending order. Highly specialized assessments consistently demonstrate higher levels of missingness than routine screening measures (Lezak et al. 2012).

<figure id="fig:missingness_barplot">
<figcaption>Missingness bar plot for all cognitive variables, ordered by missingness rates. Missingness rates were higher among the specialised assessments compared to the routine screening assessments.</figcaption>
</figure>

## Imputation Results

Prior to conducting clustering evaluations on their respective datasets, I tested all ten imputation techniques represented in Figure <a href="#fig:imputation_comparison" data-reference-type="ref" data-reference="fig:imputation_comparison">4.2</a> and Figure <a href="#fig:imputation_comparison_b" data-reference-type="ref" data-reference="fig:imputation_comparison_b">4.3</a>. Due to compression of variance (Rubin 1987), Mean Imputation behaves differently from all other methods. All nine remaining methods maintain closer adherence to marginal distributions. Discrete structure retention is greater among donor-based methods like KNN and PMM than among model-based approaches including MICE, MissForest and EM that produce smoothed continuous reconstructions.

<figure id="fig:imputation_comparison">
<figcaption>Comparison of distributions for each of the 10 different imputation methods for ATMTA and VPIMATGES. Mean imputation reduces variance whereas model-based methods maintain the distributional characteristics of the original data.</figcaption>
</figure>

<figure id="fig:imputation_comparison_b">
<figcaption>Comparison of distributions for MRAVLT015R and MRAVLT015. Deep learning models (DAE, VAE) closely approximate model-based methods.</figcaption>
</figure>

## Baseline and Primary Clustering

This section describes the main steps taken to fit the HDBSCAN solution and to evaluate the hypotheses.

The first step in this process was to perform some exploratory work to determine whether there would be a reasonable basis for applying HDBSCAN. Specifically, I needed to know whether there were enough points in the dataset that clustered well together. To assess this, I applied two baseline clustering algorithms: K-Means and Gaussian Mixture Models. Each type of clustering had been run over a large range of possible numbers of clusters ($`k = 2`$ through $`k = 6`$) in order to determine whether either algorithm produced a clearly interpretable solution. However, neither method found an optimal solution. This is reflected in the plots shown below, where I present the results from K-Means. While the Elbow Plot does appear to decline fairly sharply, I cannot identify a particularly strong "elbow" or break in the slope. Similarly, while the Silhouette Plots do appear to peak when $`k = 2`$, they also appear to fall off fairly quickly once $`k > 2`$. The lack of a strong Elbow Plot and the rapid decline in Silhouette Scores led me to consider other approaches to finding clusters. I decided to try an alternative approach called Density-Based Spatial Clustering of Applications with Noise (DBSCAN) and later Gaussian Mixture Models (GMMs) with a DBSCAN-like initialization. I discuss both methods further down.

As mentioned previously, one problem with many unsupervised learning methods is that they can easily get stuck in local minima and fail to identify a good representation of the underlying data. One common way to address this issue is to use multiple initializations of the model parameters and select the best performing model. In this analysis, I did not take that approach. Instead, I relied on the quality of the solutions obtained using the baseline methods and on visual inspection to detect meaningful patterns in the data. If the baseline methods produced good results and I could visually confirm meaningful structure in the data, then I proceeded with selecting a final solution.

I selected HDBSCAN as the primary clustering algorithm for several reasons. First, HDBSCAN is designed to handle irregularly shaped clusters and noisy data, both of which are characteristics of these data. Second, HDBSCAN allows the minimum number of samples (MinPts) for a dense region of points to be considered a cluster to be specified. Third, HDBSCAN includes a notion of outliers – points that do not belong to any cluster – and assigns them a special label ("noise"). Fourth, HDBSCAN uses a variant of DBSCAN’s reachability graph construction and performs hierarchical clustering based on this graph. Fifth, rather than extracting clusters at a single fixed neighbourhood radius as DBSCAN does, HDBSCAN evaluates density structure across a hierarchy and selects clusters that remain stable across density levels. Sixth, HDBSCAN includes a notion of cluster hierarchy – the hierarchy is represented by a tree structure and is typically plotted as dendrograms or heatmaps. Finally, HDBSCAN produces a hierarchical clustering output for all MinPts specifications. Therefore, HDBSCAN provides multiple layers of detail regarding how the data are structured.

Because my goal is to identify meaningful subgroups in the data, I expected that many of the subgroups would consist of assessments taken by individuals who exhibit some form of impairment. Therefore, I expected these subgroups to contain a mix of individuals with different levels of impairment. As such, I needed an algorithm that could capture complex structures in the data. An additional reason why I chose HDBSCAN as the primary clustering algorithm is its ability to automatically assign outlier status to points that do not belong to any cluster. Outliers represent assessments that could not be classified into any subgroup. Because I anticipated that many assessments would not belong to any subgroup (i.e., they would not fit perfectly into any subgroup), I expected that identifying outliers would help clarify how the data are organized.

Given that my primary interest is identifying meaningful subgroups in the cognitive performance data, and given that many of these subgroups may consist of assessments taken by individuals with some form of impairment, I expected many subgroups to contain assessments with varying levels of impairment. Therefore, I needed an algorithm that could capture complex structures in the data. Additionally, because I anticipated that many assessments would not belong to any subgroup (i.e., they would not fit perfectly into any subgroup), I expected that identifying outliers would help clarify how the data are organized. Given these needs, I selected HDBSCAN as the primary clustering algorithm because it provides tools for identifying clusters regardless of shape or orientation, while also identifying outliers. I expected both features to be useful when identifying meaningful subgroups in cognitive performance data.

The second piece of supporting evidence for Hypothesis 1 comes from comparing t-SNE and UMAP projections. The results are presented below.

For the UMAP+HDBSCAN combination, the hyperparameters I settled on were: `n_components`$`=8`$, `n_neighbors`$`=15`$, and `min_dist`$`=0.0`$ for UMAP (to allow for tight packing in the embedding space (McInnes, Healy, and Melville 2018)); and for HDBSCAN, `min_cluster_size`$`=1000`$ and `min_samples`$`=50`$ with `cluster_selection_method`$`=\text{eom}`$ and `epsilon`$`=0.0`$. I chose a large cluster size to ensure that only substantive groupings are retained.

<figure id="fig:tsne_umap">
<figcaption>Two-dimensional representations of the data using t-SNE (left) and UMAP (right), with HDBSCAN cluster assignments coloured. UMAP reveals clearer separation of cluster areas.</figcaption>
</figure>

## Cognitive Profiles of the Clusters

Below are the radar plots showing mean cognitive domain score per tier, expressed as a z-score from the cohort mean. The three polygons are roughly concentric (every domain moves together), so the tiers differ in overall level rather than in profile shape.

Additionally, I created a random forest surrogate that attempts to recover the tier labels from the domain scores. The Gini importance for each domain shows which domains contribute most strongly to distinguishing among tiers. There is considerable inter-correlation between the domain scores (because they are all based on cognitive performance), so interpreting this figure requires caution: although Attention appears to have low Gini Importance relative to Working Memory and Processing Speed, for example, this may simply reflect a high degree of correlation between Attention and Working Memory rather than anything about attention being clinically unimportant.

<figure id="fig:radar_profiles">
<figcaption>Left: Mean score for each cognitive domain in each tier, expressed as a z-score from the cohort mean (the dotted ring indicates the cohort average). The three polygons are approximately circular because each domain moves collectively; therefore, the tiers differ in terms of global levels rather than shapes. Right: Gini importance from a random forest surrogate that recovers tier labels from domain scores (accuracy = 0.994). Since these labels are derived from those same scores, this panel describes the decision boundaries of the partitions instead of providing independent importance measurements, and the ordering depends on inter-domain correlation (see Section <a href="#sec:feature_importance" data-reference-type="ref" data-reference="sec:feature_importance">4.9</a>). It should not be interpreted as suggesting that attention has no clinical significance.</figcaption>
</figure>

## Hypothesis 1: Discrete, Stable Clusters

Hypothesis 1 states that cognitive impairments form discrete and stable clusters. We tested this hypothesis using two complementary approaches:

**Cluster Stability Analysis.** We performed a series of cluster stability analyses by fitting HDBSCAN to bootstrapped versions of the original UMAP embeddings. Specifically, we randomly sampled 50 bootstrap iterations (with replacement) from our full sample of $`n = 17{,}406`$ cognitive assessments. For each iteration, we fit HDBSCAN and recorded both the silhouette score and percentage of non-noise points assigned by HDBSCAN. These silhouette values are computed in the UMAP embedding rather than in the original six-domain space. This distinction matters because UMAP is designed to sharpen local neighbourhood structure; for the MICE tier labels, the full-coverage silhouette is 0.526 in the UMAP embedding but 0.079 in the robust-scaled six-domain feature space. The embedding silhouette should therefore be interpreted as an internal pipeline-quality statistic, not as a stand-alone estimate of natural cluster separation in the original domain scores.

The resulting distributions are shown in the histograms shown below:

Consistent with Hypothesis 1, both measures are generally quite high across all ten imputation methods. Notably, however, KNN-SoftImpute exhibits lower cluster stability than all nine remaining methods according to both metrics.

**Core Jaccard Matching.** In addition to assessing cluster stability via silhouette and noise rates, we also assessed how well individual clusters were reproduced across bootstrap iterations using Hennig (2007)’s core Jaccard matching statistic for cluster assignments generated prior to reassignment by nearest neighbor. Core Jaccard measures how much overlap exists between corresponding subsets of points assigned by each pair of clustering solutions. Values close to 1 indicate very similar cluster assignments between two solutions, whereas values closer to zero indicate nearly no similarity.

For each bootstrap iteration $`i`$ and each method $`m`$, we computed the core Jaccard index $`cJ_{i,m}`$ between cluster assignments $`\{A^*_{i,j}\}_j`$ on iteration $`i`$ generated under method $`m`$ prior to reassignment and $`\{C^*_{i,j}\}_j`$ on iteration $`i`$ generated after reassignment.

We then averaged these values across bootstrap iterations for each method and cluster assignment type separately.

The median core Jaccard indices across all bootstrap iterations for each method are summarized in the table below:

Consistent with Hypothesis 1, all three tiers exhibited high median core Jaccard indices greater than 0.6 across all ten imputation methods, indicating that cluster assignments remained relatively consistent across bootstrap iterations.

## Hypothesis 2: Imputation Sensitivity Under a Fixed Partition

Hypothesis 2 posits that different imputation methods will produce largely overlapping assignments when applied to the same incomplete data and evaluated within a fixed embedding and partition model.

To investigate whether this is true, we compared pairwise agreements among all ten imputation methods using adjusted rand indexes (ARIs). This analysis should not be read as a second HDBSCAN clustering run. The primary tier solution was discovered with UMAP+HDBSCAN, whereas the H2 sensitivity test used the shared reference design specified in Section <a href="#sec:stats" data-reference-type="ref" data-reference="sec:stats">3.7</a>: a StandardScaler, UMAP model, and $`k`$-means model with $`k=3`$ were fitted once on the MICE-imputed domain scores, and all other imputation outputs were projected through that frozen structure before labels were predicted. The $`k`$-means step therefore functions as a fixed labelling rule for comparing imputed point locations, not as a replacement for the primary density-based clustering pipeline.

**Adjusted RAND INDEX (ARI):** The ARI takes into account both true positives and false positives/negatives, making it suitable for evaluating agreement between partitions generated by different methods. **Normalised Mutual Information (NMI):** NMI evaluates mutual information between two partitions generated by different methods. **Agreement Threshold:** For ARI/NMI evaluation purposes, we specified an arbitrary agreement threshold $`\geq`$ 0.5.

The table below summarizes pairwise ARIs among all ten imputation methods:

Note that since there are 10 methods total, there are $`\binom{10}{2}`$ = 45 pairs of methods total.

**Median ARI Across Methods:** When calculating the median ARI across methods for comparison purposes, we excluded Mean Imputation since it tends to produce partitions very dissimilar from those generated by other methods. **Pairwise Comparison Results:** Every single pair of methods exceeded our 0.5 agreement threshold (range \[0.509-0.880\]). Some pairs were highly correlated; notably EM-DAE (ARI = 0.880), DAE-VAE (ARI = 0.863), and EM-VAE (ARI = 0.828). **Mean ARI Across Method Pairs:** The mean ARI across method pairs was 0.710 with a median ARI across pairs of 0.739 (range \[0.509-0.880\]).

Since this far exceeds our pre-registered threshold ($`\geq`$ 0.5), Hypothesis 2 is supported under the fixed embedding and $`k`$-means partition diagnostic. This finding does not establish that each imputation method would independently recover the same HDBSCAN density hierarchy.

**Confidence Calculations:** For purposes of estimating confidence in tier assignments generated from each method individually, we used majority voting on all ten methods for each assessment as follows: **Majority Voting:** Each method generates an individual label assignment for each assessment; if eight or more methods agree on a label assignment for a given assessment, then that assessment receives a confident label assignment. **Confidence:** The confidence metric reflects the proportion of methods agreeing with the final label assignment selected via majority voting. **Confirmed Assessments:** Using this methodology, mean confidence was 0.929, and 86.2% of the cohort received a high-confidence tier label ($`\geq 0.8`$).

Therefore, Hypothesis 2 is supported with this defined scope: point assignments are reliable across imputation methods when the embedding geometry and partition model are held constant.

To test Hypothesis 2, I implemented a standardised agreement diagnostic. This shared design ensured that the effects of the imputation were isolated. The workflow proceeded as follows: the `StandardScaler`, UMAP, and $`k`$-means models were fitted once on the MICE-imputed data with $`k=3`$, and then applied (via `transform`/`predict`) to every other method, so that the imputed values were the only thing varying. I quantified agreement with the Adjusted Rand Index (ARI; (Hubert and Arabie 1985)) and Normalised Mutual Information (NMI; (Vinh, Epps, and Bailey 2010)). This $`k`$-means step was not part of the primary discovery pipeline; it was used only to provide a fixed partition against which imputed point locations could be compared. The result should therefore be interpreted as robustness of point assignments under a fixed embedding and partition, not as evidence that every imputation method independently recovers the same HDBSCAN clustering structure. When the full UMAP+HDBSCAN pipeline is refitted independently, Table <a href="#tab:method_summary" data-reference-type="ref" data-reference="tab:method_summary">3.2</a> shows that the recovered number of tiers varies from $`k=3`$ to $`k=5`$; Rubin-pooled multiple-imputation draws vary from $`k=3`$ to $`k=7`$ (Section <a href="#sec:robustness" data-reference-type="ref" data-reference="sec:robustness">4.10</a>). That sensitivity is consistent with discretising a cognitive continuum.

<figure id="fig:h2_ari_nmi">
<figcaption>Adjusted Rand Index (ARI) at top and normalised mutual information (NMI) at bottom for pairwise comparisons across the 10 different imputation methods. High agreement was found throughout, although KNN showed lower agreement with the smoother model-based methods.</figcaption>
</figure>

<figure id="fig:h2_consensus">
<figcaption>Histogram of consensus confidence values (proportions of methods assigning to the same class). Assessments whose assignment is highly confident across multiple imputation methods have higher consensus confidence values.</figcaption>
</figure>

<figure id="fig:h2_dendrogram">
<figcaption>Dendrogram of imputation methods using average linkage clustering on ARI-based distance metrics. KNN separates itself from other branches, and tighter grouping occurs among the smoother model-based methods.</figcaption>
</figure>

## Hypothesis 3: Clinical Unit Association

Finally, Hypothesis 3 predicts that cognitive severity tier should predict clinical unit assignment independently of diagnostic category.

To test this prediction formally, we employed a Chi-square Test of Independence. **Chi Square Tests:** $`\chi^2 = 911.3`$, p-value $`\approx 4 \times 10^{-156}`$, Cramér’s $`V = 0.162`$.

By Cohen’s criteria for effect sizes, the effect size (0.162) corresponds to a small effect size. However, by the pre-registered standards, this effect size constitutes a meaningful effect size.

These findings demonstrate that cognitive severity tier adds predictive power beyond diagnostic category alone – specifically when determining which clinical unit(s) an individual belongs to.

To assess potential confounding effects from diagnostic categories themselves, we conducted Cochran-Mantel-Haenszel (CMH) tests to control for diagnostic category effects. The CMH tests indicated that cognitive severity tier continued to significantly predict clinical unit assignment even after adjusting for diagnostic category effects.

**Rubin-Pooled Multiple Imputation:** To additionally establish robustness against potential biases arising from single-draw estimates, we utilized Rubin-Pooled Multiple Imputation and repeated our calculation of Cramér’s V. Rubin-Pooled Multiple Imputation yielded a pooled Cramér’s $`V = 0.154`$, which falls squarely above the hypothesis threshold.

Thus, all evidence supports Hypothesis 3.

<figure id="fig:h3_heatmap">
<figcaption>Heatmap of cluster assignments (columns) by clinical unit (rows). Cell colors represent frequencies. Specific tiers occur more frequently in certain units.</figcaption>
</figure>

## Hypothesis 4: Feature Engineering

The main hypothesis was that aggregate measures of features based on Domain would produce more stable clusters than separate feature-level data. To test these hypotheses, I compared two different sets of measures for all three features across the three previously mentioned criteria: silhouette scores, condition number, and variance inflation factors (VIF).

Aggregate measures produced a marginally greater average silhouette score than did the individual variable-based measure (0.481 vs. 0.473; Figure <a href="#fig:h4_comparison" data-reference-type="ref" data-reference="fig:h4_comparison">4.10</a>). More importantly, there was significant change in terms of how each set of measures conditioned the feature space. The average VIF decreased significantly, from 2.77 to 1.88, and the condition number decreased similarly, from 61.7 to 11.8. High VIFs indicate multicollinearity, which distorts computation of distances needed to perform the UMAP and HDBSCAN algorithms. Therefore, the decrease in VIFs indicates that the aggregation process reduced redundancy while maintaining the underlying cognitive constructs measured by the tests (Lezak et al. 2012).

Therefore, hypothesis 4 is supported and aggregate measures provide improved numerical stability without losing cluster separation.

<figure id="fig:h4_comparison">
<figcaption>Comparison of domain-aggregated and variable-level features: silhouette (0.481 vs. 0.473), mean VIF (1.88 vs. 2.77), and condition number (11.8 vs. 61.7). Aggregation at the domain level produces similar separations but much less correlated, well-conditioned features.</figcaption>
</figure>

## Feature Importance Analysis

To conduct this analysis, I trained a Random Forest surrogate model on the MICE-imputed Domain scores and used the tier labels as targets. It obtained an accuracy rate of 99.4% in five-fold cross-validation. The accuracy of this surrogate model measures how well the tier labels can be predicted from the Domain scores. However, because the tier labels were created from the same Domain scores used in the clustering algorithm (UMAP + HDBSCAN), the surrogate model is essentially creating its own versions of the clustering boundaries. Therefore, since the surrogate model performs so well (i.e., nearly perfect accuracy), the tier labels demonstrate high degrees of separability in Domain space.

I employed Gini and permutation rankings to help illustrate the relative importance of each Domain. Orientation ranked highest ($`\text{Gini}=0.49`$), followed closely by visuoperceptual ($`\text{Gini}=0.24`$) and language ($`\text{Gini}=0.17`$), with attention ($`\text{Gini}=0.03`$) and executive function ($`\text{Gini}=0.02`$) last among the six domains (Figure <a href="#fig:feature_importance" data-reference-type="ref" data-reference="fig:feature_importance">4.11</a>). Although this order may provide some useful information about the importance of each Domain in terms of their relationships to one another, this ordering should be interpreted cautiously. It represents only what is internal to the clustering methodology and has been influenced partially by circularity. Additionally, Gini importance is biased when predictors are highly correlated (Boulesteix et al. 2012). As stated earlier, the six domains are highly positively correlated (both theoretically as part of the cognitive positive manifold and empirically as indicated by the first principal component in §<a href="#sec:cluster_profiles" data-reference-type="ref" data-reference="sec:cluster_profiles">4.4</a>). Once a tree splits on a highly correlated Domain like orientation, attention appears redundant. Thus, even though attention ranks lowest, it is incorrect to infer that attention is clinically irrelevant. Rather, attention’s position is best understood within the context of Figure <a href="#fig:radar_profiles" data-reference-type="ref" data-reference="fig:radar_profiles">4.5</a> where the concentric profiles and principal component loadings determine whether the tiers represent total clinical severity or a Domain-specific dissociation.

<figure id="fig:feature_importance">
<figcaption>Random Forest surrogate trained to recover tier labels from domain scores. Left: Gini importance. Right: Permutation importance with error bars. Since labels are derived from the same scores, this panel describes the decision boundaries of the clustering partitions rather than independently evaluating their relative importance. Because the domains are strongly intercorrelated, rankings should not be taken as implying clinical insignificance of attention.</figcaption>
</figure>

## Robustness Analyses

There are several analyses that have been done to help us understand the robustness of our hypotheses. First, we used a "listwise deletion" baseline. Second, we did a sub sampling stability study. Third, we estimated bootstrap confidence intervals. Fourth, we estimated Rubin-pooled uncertainty across multiple imputation draws. Fifth, we validated our findings using time since injury as an alternative measure. Finally, we used multiple comparison corrections for the 45 pairwise H2 tests.

**Bootstrap Confidence Intervals.** We performed a nonparametric bootstrap analysis of our data at the individual level. For the major estimates, we obtained very narrow 95% confidence intervals around the estimated effects. For example, the bootstrap 95% confidence interval for the H2 mean ARI is 0.710 \[0.704, 0.716\]; for H3, it is 0.16 \[0.15, 0.18\] (Cramér’s V); and for H4, it is 0.05 \[0.04, 0.06\] (silhouette gap). The small widths of these confidence intervals should be viewed in relation to the large sample size ($`n = 17{,}406`$) of our cohort, and not as evidence that all the effects we found are large.

**H2 & Multiple Comparison Correction.** In order to test H2, we need to perform 45 different pairwise ARI comparisons against a cutoff of greater than 0.5. Therefore, we applied Holm-Bonferroni corrections to ensure family-wise Type I error rates, and Benjamini-Hochberg corrections to ensure false discovery rates. Using a parametric one-sided bootstrap p-value for each pair, under both types of corrections, we reject the null for 44 of the 45 pairs; the only exception is KNN-SoftImpute (bootstrap mean $`\mathrm{ARI}=0.509`$, 95% CI \[0.497, 0.521\]). Thus, with respect to imputation robustness, all method pairs are significant except this one borderline case.

**Rubin-Pooled Multiple Imputation.** To estimate uncertainty from a single MICE run, we generate $`M = 5`$ independent draws, run the entire pipeline on each draw, and then pool the hypothesis-level statistics with Rubin’s rules. The resulting estimates remain positive and bounded: 0.154 \[0.049, 0.259\] for Cramér’s V (H3), and 0.050 \[0.043, 0.058\] for the silhouette gap (H4). Furthermore, the number of clusters recovered varied between 3 and 7 across draws as expected given that we are discretizing a continuous gradient; however, the H4 gap remained stable. Also, domain-level features outperform variable-level features in every one of the independent draws.

**Listwise Deletion Baseline.** If we discard the 46.9% of the assessments with missing values and apply the pipeline only to the remaining 9,245 complete cases, we obtain two clusters with a silhouette of 0.257. Additionally, agreement between the MICE solution for those same patients and the solution based solely on complete cases is moderate (ARI 0.625, NMI 0.519), yet they are clearly not equivalent. Hence, imputation has a material impact upon the analysis: discarding the 46.9% of the assessments with missing values changes both the quality and quantity of tiers recovered.

**Subsampling Stability.** When processing random 80% subsamples of our cohort using UMAP+HDBSCAN, we find that the majority of samples recover the same general severity structure; however, exact labels and numbers of clusters vary from two to five. This is precisely what would be expected if we were converting a continuous gradient into discrete categories and is consistent with the per-cluster Jaccard results for H1.

**Missingness Threshold Sensitivity.** I also re-ran the entire process – including variable selection; domain computation; MICE imputation; and UMAP+HDBSCAN – at five Tier 1 thresholds from 30% to 70%. As shown in Figure <a href="#fig:sensitivity" data-reference-type="ref" data-reference="fig:sensitivity">4.12</a>, the solution remains in the two to three tier range with silhouettes ranging from 0.39 to 0.52 over thresholds of 40% to 70%. Only at 30%, where we are being overly restrictive with regards to how many variables we allow, does the solution break down. Therefore, our choice of 50% threshold used throughout our main analysis represents a reasonable balance between how much information is present in each record and how many variables are available.

<figure id="fig:sensitivity">
<figcaption>Effect of varying Tier 1 missingness threshold across five values (30 – 70%). Upper row: (a) Number of available variables and (b) Number of clusters identified. Lower row: (c) Silhouette score and (d) Proportion of noise. Vertical dashed lines indicate Tier 1 missingness threshold used in primary analyses.</figcaption>
</figure>

**Outcome-Adjacent Validation.** Although functional outcomes are unavailable for use as validating measures of impairment status at discharge, we may examine functional change through time-since-injury (TSI) at each assessment as an alternate validating measure. TSI varies significantly by tier (Kruskal-Wallis test $`p = 4 \times 10^{-28}`$), with median TSI times of 214 days for Above Average, 188 days for Near Normal, and 172 days for Global Impairment. Thus, as TSI increases, severity of impairment decreases across these three tiers. Among the 5,206 patients who have had at least two assessments, 50.2% (2,613 patients) maintain their original tier assignment while 49.8% (2,593 patients) experience some degree of tier shift. While such movement could suggest that patients possess a set of fixed phenotypic characteristics, such movement is far more indicative of variability in severity along a spectrum of impairment severity. Furthermore, among the 912 patients who experienced exactly two assessments and changed tiers during that period, improvement in functional status occurred approximately three times as frequently as worsening in functional status (706 vs. 206 transitions), consistent with expectations regarding natural clinical recovery patterns.

**Embedding Seed Stability.** To determine whether the clustering was due to UMAP’s random initialization, we repeated the entire embedding and clustering process on our MICE-imputed domain scores using ten randomly selected seeds with equal hyperparameter settings. There was high concordance between labeling schemes; specifically, the mean pairwise ARI across the ten runs was 0.957 (median $`= 0.960`$, min-max $`= [0.900, 1.000]`$). After k-nearest neighbor reassignment, this increased to 0.965. With respect to our finding that there exists a strong underlying severity axis supported by deterministic PCA (see §<a href="#sec:cluster_profiles" data-reference-type="ref" data-reference="sec:cluster_profiles">4.4</a>), together with embedding seed stability, this further decreases concerns that our solution was simply an artifact of unstable UMAP initialization.

**Gaussian Mixture / Latent Profile Baseline.** As a model-based comparison, I fit Gaussian mixture models with full covariance matrices to the imputed domain scores for $`k`$ varying from 2 through 6. This analysis is analogous to latent profile analysis in that it estimates model-based continuous-profile classes, but it is not a formal latent profile analysis with full-information maximum likelihood on the incomplete raw data. BIC decreased monotonically with $`k`$ (from 243,249 at $`k = 2`$ to 92,606 at $`k = 6`$) without any local minimum, suggesting that there is no discrete class optimum, but rather a continuum. Moreover, mixture model solutions agree modestly with density-based tiers ($`\mathrm{ARI} = 0.350-0.400`$), and the two-component solution had the clearest silhouette (0.45). Therefore, the model-based baseline supports conclusions made via the primary pipeline: there is no discrete class optimum, but rather an underlying continuum representing severity. A formal latent profile analysis with FIML remains a separate model-based extension.

**MNAR Tipping Point.** To establish bounds on potential missing-not-at-random mechanisms, I assumed every missing value was replaced by the worst observed performance on that variable – either the minimum value or the maximum value depending on whether it was a timed ATMTA or not. Clearly, this is an intentionally extreme and conservative assumption. Under this condition, even though the partition became fractured and the silhouette fell to 0.030 because point-mass spikes were created when all missing values were forced to extreme values, a distinct lowest severity tier still existed and retained approximately 65.2% of assessments originally labeled as Global Impairment. Therefore, even under extreme MNAR assumptions, Global Impairment is likely the most robust portion of our solution. Most importantly, extreme MNAR assumptions seem to degrade finer separation within lower severity tiers, and thus a formal delta-shifted tipping-point analysis seems like an interesting future direction.

**Summary Characteristics of Excluded Records.** Applying the Tier-1 filter to the full raw cohort retained 17,406 of the 22,075 records used in the source extract and excluded 4,669 records. Discarded records averaged only 0.800 of their 14 eligible tests, whereas retained records averaged 12.5 tests per record, thereby appearing to represent nearly empty administrative encounters instead of incomplete testing of severely impaired individuals. Demographically, both excluded records and retained records are largely indistinguishable (e.g., age at injury: 45.7 vs. 46.3 years; Cohen’s $`d = -0.04`$; sex: male/female = \[63%;37%\] vs. \[68%;32%\]; TSI: 2.3 vs. 1.6 years; $`d = 0.16`$). Therefore, we do not believe that our Tier-1 filter will suppress detection of a cognitively impaired subgroup identifiable via measurable characteristics – although we obviously cannot assess cognitive impairment directly.

## Cluster Clinical Naming

To give our density-based clusters clinically relevant labels; we employed a rule-based naming system based upon the domain-level z-score profiles associated with each cluster.

Clustering Profiles Associated with Domains Having Z-Scores Greater Than +0.5 Were Labeled Above Average.

Profiles Associated with Domains Having Z-Scores Less Than -0.5 Were Labeled Global Impairment.

All other profiles were labeled Near Normal.

This resulted in our final labels being Above Average ($`n = 6{,}725`$), Near Normal ($`n = 6{,}328`$), and Global Impairment ($`n = 4{,}353`$).

Since our tiers differ primarily in terms of overall level and not profile shape – severity labels are preferable to phenotype names.

They provide valuable shorthand for clinicians engaged in discussing potential rehabilitation options with their patients – as well as providing useful tier-based guidance for rehabilitation triaging efforts.

The full mapping of identifier codes to assessment frequency is contained within our interactive CogDash dashboard

# Discussion

## A Cognitive Severity Gradient, Not Discrete Phenotypes

Overall, I found no evidence of discrete cognitive phenotypes in this cohort of people with acquired brain injury (ABI); instead, I found a clear cognitive severity gradient. I identified patients as being in the ‘above average’, ‘near normal’ and ‘global impairment’ tiers based upon their performance across the battery. Importantly, these tiers differ by level, not by profile shape. As illustrated in Figure <a href="#fig:radar_profiles" data-reference-type="ref" data-reference="fig:radar_profiles">4.5</a>, each of the six domains are moving together. One principal component explained 56% of the variance in the domain scores and loaded positively across all six domains with a similar magnitude. Therefore, I interpret these results as demonstrating a severity stratification of the cognition of individuals with ABI, rather than an identification of a set of dissociable cognitive profiles. While I consider this clinically useful, because the axis is derived from performance across the cognitive tests themselves, and not from the injury-severity bands or diagnostic categories criticized in Chapter <a href="#Chapter1" data-reference-type="ref" data-reference="Chapter1">1</a>, I also note that it demonstrates an association with clinical-unit placement that extends beyond diagnostic category (§<a href="#sec:h3_results" data-reference-type="ref" data-reference="sec:h3_results">4.7</a>).

Moreover, my results inform a broader question in neuropsychology: whether variability across test batteries is primarily domain-specific or dominated by a general factor. I found that in this routinely collected cohort, the general severity axis accounted for most of the recoverable structure. Secondary domain-specific variation was present; however, I did not find that it determined the clustering. I interpret this pattern as consistent with both clinical experience, where global impairment often separates patients before they are differentiated further through narrow dissociations \[e.g., (Maas et al. 2017)\], and the positive manifold of inter-test correlations found in neuropsychology (Lezak et al. 2012). Therefore, the phenotyping result I report here is more conservative than suggested by some other accounts. Specifically, when I analyzed the data under imputation-robust, sensitivity-tested conditions, overall severity emerged before specific patterns of profiles. I do not over-read this null result: domain aggregation and density clustering on a manifold dominated by a general factor have limited sensitivity to recover narrow dissociations, including an attention-specific subgroup, if such dissociations are small or orthogonal to the principal severity gradient.

My findings do not refute studies that report multiple dissociable cognitive profiles after brain injury (e.g., (García-Rudolph et al. 2021)). Rather, they qualify their interpretations. Unlike those studies, my pipeline differed in several ways. For example, UMAP+HDBSCAN allows for processing of non-convex structures and low-density noise; the bootstrap analysis provided an evaluation of the replicability of the clusters; and each variable was standardized and winsorized in addition to being direction-aligned before forming aggregates. Each of these steps made a difference. High variance raw measures (i.e., a timed Trail making score) can dominate an unstandardized composite; non-cognitive variables can establish artificial axes; nearly empty records can disrupt density estimates. Thus apparent phenotypes may represent artifacts of preprocessing rather than true neuropsychological structure. Chapter <a href="#Chapter6" data-reference-type="ref" data-reference="Chapter6">6</a> will examine this relationship further.

I treat the stability analyses (§<a href="#sec:h1_results" data-reference-type="ref" data-reference="sec:h1_results">4.5</a>) as additional support for my characterization of the cognitive gradients as a severity gradient. All ten imputation methods met the pre-registered H1 criterion in terms of the stability analyses. The Jaccard analysis showed greater stability for the two extremes (the ’above average’ and ’global impairment’ tiers) compared to the central tier (’near normal’), which I interpret as having been cut from a continuum. Patients at the boundary between two tiers can move between them without disrupting the underlying order.

Therefore, I argue that the three-tier solution developed from the primary MICE pipeline should be viewed as an interpretable discretization of a continuum rather than as evidence of natural kinds. Other clustering techniques produce between 3 and 5 tiers depending on how they are configured. Rubin pooling and sensitivity to thresholds show that while cluster counts may vary, the ordering by severity remains constant. The clinically useful entity is thus the continuum; the tiers represent a convenient way to describe aspects of it.

## Imputation Sensitivity Under a Fixed Partition

I regard Hypothesis 2 as the major methodological contribution, but I define its scope deliberately narrowly. I discovered the primary clusters with UMAP+HDBSCAN. For the H2 analysis, I then used a separate fixed-reference diagnostic, fitting $`k`$-means once on the MICE embedding and projecting the other imputation methods into that same structure. Under that diagnostic, point assignments changed very little with regard to imputation methods: on average, the 45 method pairs yielded a mean pairwise ARI $`> 0.70`$, with 100% yielding an ARI $`> 0.50`$ (§<a href="#sec:h2_results" data-reference-type="ref" data-reference="sec:h2_results">4.6</a>). Therefore, I interpret the easily recoverable structure as a strong severity gradient, whereas a fragile multi-dimensional profile structure is less readily recovered. This distinction likely explains the robustness while still allowing for method-specific variability (Rubin 1987).

Although the imputation process influenced the number of identified tiers and the quality of those tiers, I found that the location of patients along the severity signal did not appear to depend on a particular imputation strategy. I interpret the broad implication as follows: most clinical interpretations of a patient’s relative position on the severity gradient are unlikely to change solely because one defensible imputation method is substituted for another. I do not take this to mean that missing data can be handled casually. Rather, I argue that researchers should treat missingness systematically and report the method clearly, while clinicians should interpret tier labels as aids to judgement rather than as rules that replace medical training or professional experience.

As depicted in Figure <a href="#fig:h2_dendrogram" data-reference-type="ref" data-reference="fig:h2_dendrogram">4.8</a>, I found a strong separation between two families of imputation methods: smooth, model-based methods (EM, DAE, and VAE) that tend to smooth towards a model based conditional mean; local donor-methods (KNN) that rely on a few local donors to plug in missing values. Although many studies use classification criteria related to whether or not an imputation method uses statistical/machine learning/deep learning families, I found the more salient divide to be between smooth and local.

At the assessment level, I found that instability correlates moderately with the fraction of imputed data ($`r = 0.47`$; §<a href="#sec:h2_results" data-reference-type="ref" data-reference="sec:h2_results">4.6</a>). As such, I argue that downstream applications should treat assessments with heavy amounts of missing data differently from assessments that contain almost no missing data. This could be achieved by reporting decreased confidence or by comparing more than one imputation strategy.

I view consensus clustering as a practical means of addressing this issue. The ten imputation strategies align their votes regarding label assignments for individual assessments, and the resulting confidence score estimates agreement among strategies. Overall confidence is high (mean confidence 0.93; 86.2% of assessments have high confidence). However, as I discussed previously, I interpret the lower-confidence assessments as clinically meaningful rather than merely inconvenient. Most notably, these assessments represent patients who are located near tier boundaries and should prompt caution/re-assessment.

In the literature, MICE is commonly used prior to clustering neuropsychological data. MissForest (Stekhoven and Bühlmann 2012) is often preferred when non-linear relationships are expected. After applying Holm-Bonferroni correction across the 45 pairs of comparison (see Section <a href="#sec:robustness" data-reference-type="ref" data-reference="sec:robustness">4.10</a>), I found that 44 of the 45 pairs reject the null hypothesis that ARI $`\leq 0.50`$. Only the KNN-SoftImpute pair remains at or near threshold levels. I interpret the broader result, within the fixed-reference H2 design, as clear: the location of patients along the severity signal does not depend upon a single imputation strategy. The number of density-based tiers remains more sensitive when UMAP+HDBSCAN is refitted independently.

I also provided a listwise deletion baseline in Section <a href="#sec:robustness" data-reference-type="ref" data-reference="sec:robustness">4.10</a> to illustrate why imputation is necessary. Restricting analysis to only complete cases results in a different number of clusters and silhouette (0.257) compared to the MICE solution for shared patients (ARI 0.625). Thus, while removing the 46.9% of assessments with missing data changes recovered structure, imputation was not merely cosmetic.

## Clinical Unit Association

To determine whether the severity tiers observed in the current study were associated with clinical unit assignment, I tested the relationship between tier membership and clinical unit, then examined whether this association remained after controlling for diagnostic category. Because patients in the Global Impairment tier generally require more intensive and structured forms of treatment than patients in higher-functioning tiers, I expected this tier to be overrepresented in rehabilitation settings. The results supported that interpretation: severity tiers were associated with clinical units, although the effect size was small by Cohen’s standards. I found, using the Cochran-Mantel-Haenszel test, that this association was not reducible to diagnostic category. Therefore, I interpret severity tier as placement information beyond diagnostic category.

I interpret this association as clinically plausible. Diagnosis is frequently used as a proxy for mechanism of injury and expected recovery when patients are referred to rehabilitation units (Saatman et al. 2008). However, patients in the Global Impairment tier generally require more intensive and structured rehabilitation than do patients in the Above-Average tier regardless of overlap between diagnostic categories. The persistence of the tier-unit association after controlling for diagnosis suggests to me that rehabilitation services may already be routing patients, at least in part, according to impairment level. By explicitly incorporating severity tiers into decision-making frameworks, clinical units could become more closely aligned with functional ability levels. Making this stratification explicit would also allow decisions about triage to be audited and improved (Corrigan, Selassie, and Orman 2010).

## Feature Engineering

There are many ways to define cognitive features. Two broad options are variable-level features and aggregate features. Variable-level features treat each individual test separately, whereas aggregate features represent averaged or summed versions of tests that are intended to measure a shared cognitive domain. I tested whether domain-aggregate features would be better conditioned than variable-level features. In this context, better conditioned means lower multicollinearity, indexed by smaller variance inflation factors (VIFs), and a smaller condition number.

The results supported H4. I found that domain-aggregate features were much better conditioned than variable-level features even though separation between clusters increased very little. The silhouette changed only slightly (0.481 vs. 0.473); however, mean VIF decreased from 2.77 to 1.88 and the condition number decreased from 61.7 to 11.8 (see §<a href="#sec:h4_results" data-reference-type="ref" data-reference="sec:h4_results">4.8</a>). While aggregation improved conditioning enough to reduce some distortion caused by correlated tests entering the distance computation, it did not substantially improve separation between clusters. Nevertheless, I interpret this improvement as quantitative support for the clinical practice of interpreting test batteries by domain rather than test by test (Lezak et al. 2012).

I emphasize one critical requirement for aggregation: preprocessing must occur before aggregation. Variables must be winsorized, direction-aligned, and standardized before they can be averaged into composites. Otherwise, differences in raw scale will produce artifacts. For example, if several memory tests are averaged without standardization, the resulting composite can be dominated by whichever test has the largest range rather than by the intended memory construct. If several highly correlated tests enter into an unstandardized composite, then UMAP and HDBSCAN can exaggerate distance computation using a common cognitive dimension. Aggregation provides one feature per construct, so each domain contributes more evenly.

## Feature Importance and What Drives Severity

I view the findings presented in §<a href="#sec:feature_importance" data-reference-type="ref" data-reference="sec:feature_importance">4.9</a> as descriptive rather than explanatory. The Random Forest surrogate produced 99.4% accuracy using the same domain scores used to generate the labels. Thus, I interpret the ranking as primarily recovering partition boundaries rather than explanatory structures underlying those partitions. The Random Forest ranked orientation, visuoperceptual abilities, and language above attention and executive function; however, I do not give this ordering strong interpretation because the domains are highly correlated. Gini importance is susceptible to variability under correlated predictors (Boulesteix et al. 2012).

I consider the principal component structure more reliable. One component explained 56% of total variance in overall cognitive severity and loaded positively with similar magnitude across all six domains. I interpret this finding as evidence that severity tiers represent general severity levels rather than domain-specific dissociations or attention-specific patterns within this particular domain-aggregated pipeline. Robustness checks presented in §<a href="#sec:robustness" data-reference-type="ref" data-reference="sec:robustness">4.10</a>, including subsampling and sensitivity to missingness thresholds, suggest that severity ordering remains stable, but exact tier count depends on resolution criteria and inclusion threshold. Data-driven studies examining phenotyping should report preprocessing choices clearly and include sensitivity analyses.

## Clinical Implications

I interpret the current results as consistent with a three-tier cognitive severity stratification system. However, I also identify several limits to this approach. The broad clinical implication is conservative: these tiers may help summarize relative cognitive severity, but they should not be used as stand-alone clinical rules. When patients move through the rehabilitation system, clinicians will continue to rely on medical training, local service knowledge, and professional experience when making placement decisions. At present, I do not think these results justify specific recommendations for direct clinical implementation beyond careful interpretation of cognitive severity and transparent handling of missing data.

Clinicians have long relied on visual inspection of patient distributions to identify unusual cases. I interpret the current results as supporting that practice alongside algorithmic clustering. Many assessments did not fall neatly into sharply separated clusters, and I view the central tier as especially consistent with a boundary region cut from a continuum. Because the majority of patients fall along a broad severity gradient rather than within highly separated natural categories, future tools should help identify difficult-to-cluster or boundary-near assessments rather than forcing every assessment into a definitive phenotype label.

Future researchers studying large datasets with missing cognitive data may benefit from additional diagnostics for clustering difficulty. One simple candidate is the proportion of points with very low silhouette values, for example less than 0.05, reported alongside overall silhouette and stability metrics. This would not replace substantive clinical interpretation, but it could help quantify how many assessments sit near ambiguous regions of the partition.

# Limitations and Future Work

## Limitations

Firstly, the study was based in a single centre. All data were obtained from one rehabilitation unit. Therefore, the possibility of selection bias exists and extrapolation to other clinical groups cannot be made. Although all tests used have been extensively studied and have international validity, the six cognitive domains provide a common framework for the description of post-injury cognition. However, the validation of this cognitive severity structure will require multi-centre studies prior to its acceptance as a general characteristic of ABI rather than as a specific characteristic of this unit.

Secondly, the recovered structure is a limitation on interpretation. The major finding is a continuum rather than distinct categories. Most of the cohort fall along a single dimension representing overall cognitive severity with PC1 accounting for 56% of the variance. The three tiers represent a discretization of this continuum. Therefore, the tiers should not be regarded as phenotypic entities with well defined boundaries. Tier count will be influenced by both the resolution of clustering and the proportion of missing data. Assessments located near tier boundaries should be viewed cautiously. Ultimately, a continuous severity score may be more representative than discrete tiers (Section <a href="#sec:future" data-reference-type="ref" data-reference="sec:future">6.2</a>).

Thirdly, the analytical approach has limited capacity to model temporal change. ABI recovery is typically rapid during the early stages and follows a slower rate thereafter (Ponsford et al. 2014; Maas et al. 2017). Therefore, a single assessment provides only a ’snapshot’ of a patient’s recovery status. For many patients in the dataset, the inclusion of multiple assessments allows for the examination of change within patients (below); however, the timing of follow-up assessments is still determined by clinical necessity rather than being standardized.

Of the 5,206 patients with longitudinal data (Section <a href="#sec:robustness" data-reference-type="ref" data-reference="sec:robustness">4.10</a>), the pattern described above is clinically plausible: 50.2% of patients remain in the same tier, while of those whose tier changed, 706 moved towards improved function whereas 206 moved towards worsened function. This 3:1 ratio represents the expected direction of recovery. However, the degree to which this reflects true recovery versus selection factors (e.g., patients being discharged when they demonstrate improvement) cannot be completely distinguished.

Future longitudinal designs with standardized assessment intervals will be necessary to determine this question.

Furthermore, the imputation strategy introduces another constraint on interpretation. The MAR assumption cannot be tested from observed data alone (Rubin 1976; Little and Rubin 2019). In clinical settings, a test may be incomplete due to the inability of a patient to complete it; therefore, the missing value may be informative and may represent impaired performance. If patterns of MNAR were prevalent in clinical settings, function might be overestimated. An upper bound on the impact of MNAR is provided by re-imputing every missing value to the lowest observed performance (the "tipping point" check; Section <a href="#sec:robustness" data-reference-type="ref" data-reference="sec:robustness">4.10</a>). Under that extreme assumption, the Global Impairment tier persisted and included 65% of its original membership; however, the finer partition degraded. A formally-specified delta-shifted sensitivity analysis would further refine this bound.

Additionally, a structured co-occurrence of missingness may provide some reassurance regarding test-battery protocol-driven dropout rather than solely outcome-driven dropout. The comparison of 10 imputation methods also serves as a sensitivity analysis. High-confidence consensus labels were assigned to 86.2% of assessments across methods, indicating that plausible imputation differences did not substantially affect the primary cognitive-severity structure for most of the cohort.

Another related caveat concerns the Tier-1 filter that removes assessments where more than half of their values are missing. Upon review (Section <a href="#sec:robustness" data-reference-type="ref" data-reference="sec:robustness">4.10</a>), removed records averaged only 0.8 out of 14 completed tests and were highly similar demographically to retained records. Therefore, the Tier-1 filter likely removed primarily empty administrative records rather than an undetected severely impaired group. Still, due to missing data issues, the cognitive severity of removed records cannot be assessed directly, and only the 30-70% threshold sensitivity analysis bounds the potential effect of this decision.

Finally, the pipeline imputes and then clusters, whereas model-based alternatives exist, including latent profile analysis via full-information maximum likelihood (FIML). The Gaussian-mixture baseline in Section <a href="#sec:robustness" data-reference-type="ref" data-reference="sec:robustness">4.10</a> provides only an approximate model-based comparison because it is fitted after imputation rather than directly estimating profiles from incomplete data. It nevertheless demonstrated that BIC decreased monotonically with increasing numbers of classes, providing support for a continuum rather than a discrete optimum. Thus, developing a formal latent profile analysis that uses FIML instead of the present impute-then-cluster strategy is another viable area of future development.

Feature-engineering remains relevant. Non-cognitive features are eliminated and every feature is standardized (direction aligned), and winsorized prior to summarizing them as composites and generating potentially artificial profile differences. More generally, the methodological lesson is clear: unsupervised phenotyping relies on preprocessing. Any distinctive phenotype identified in an exploratory fashion should be examined relative to choices about scaling, variable selection and cohort definition before it receives a clinical label.

Finally, HDBSCAN introduces sensitivity to hyperparameters. I conducted an extensive search ($`9 \times 120`$ configurations) and selected optimal parameters \[`min_cluster_size`$`=1000`$ and `epsilon`$`=0.0`$\], maximizing the composite quality metric $`Q`$. Because $`Q`$ contains the silhouette score, and because the UMAP seed was also selected partly on silhouette performance, the reported absolute silhouette is optimistic by construction. It is best treated as a selected internal validation statistic rather than an unbiased estimate of cluster quality. Because the underlying structure is unidimensional, however, there is a relationship between cluster size and number of tiers. In addition to examining UMAP + HDBSCAN stochastically and potentially sensitively to random initialization and imperfect preservation of global structure, I applied ten random seeds per configuration/bootstrap sample/variable subset/subsampling rate combination, and PCA as an additional form of comparison. The main conclusion does not rely on UMAP alone; PCA also demonstrates that there is a strong cognitive-severity gradient (PC1 $`=56\%`$) represented by the first principal component. Re-running the entire pipeline with ten random seeds resulted in nearly identical labels (mean pairwise $`\mathrm{ARI}=0.957`$; Section <a href="#sec:robustness" data-reference-type="ref" data-reference="sec:robustness">4.10</a>). While the exact number of tiers can vary slightly depending upon these checks, the overall order of severity is robust.

Lastly, computational cost presents a fourth practical limit. Running UMAP + HDBSCAN fifty times per method is computationally intensive; however, due to modularity allowing for parallel processing, runtime costs were manageable on a typical consumer-grade laptop.

## Future Directions

Four potential areas for future work arise from the findings and limitations described above.

Firstly, modeling the continuum directly. The most obvious implication of the findings regarding cognitive-severity gradients is that continuous cognitive-severity indices - either derived from PCA or supervised learning models trained on functional-outcome measures - may provide more accurate representations and may be more useful summaries than tier-based classifications. Future research should investigate comparing continuous cognitive-severity indexes to tier classification schemes for predicting prognosis and for assigning rehabilitation intensity according to need by treating tier classification as an interpretable discretization of a continuous measure rather than as natural categories.

Secondly, longitudinal clustering represents an obvious next step. Applying the developed pipeline to assessments collected at regular time points would allow researchers to describe how individual patients’ positions on the cognitive-severity gradient evolve over time as part of their recovery trajectories: i.e., whether patients’ initial levels predict longer-term outcomes and whether recovery rates differ depending on severity level (Ponsford et al. 2014). Severity-based models describing recovery trajectories would represent much more valuable inputs to clinicians determining prognosis and rehabilitation-intensity decisions than cross-sectionally-derived assessments.

Thirdly, multi-center validation represents an essential requirement for considering cognitive-severity stratification as a feature of acquired-brain injury rather than as a feature of this specific service. A multi-center study across different health care systems would assess whether the one-dimensional cognitive-severity gradient found here survives changes in catchment population, test batteries, and assessment schedules (Maas et al. 2017).

Fourthly, integrating neuroimaging will help link cognitive-severity gradings with neural mechanisms. By correlating an individual’s position on the cognitive-severity gradient to structural-functional imaging metrics, researchers may identify the neural correlates of global cognitive impairments following ABI; this type of evidence may assist in targeting interventions (Saatman et al. 2008; Maas et al. 2017).

# Conclusions

## Summary of Key Findings

The purpose of this study was to find out if data-driven clustering of neuropsychological testing could show a cognitive pattern in acquired brain injury (ABI) that would be reliable, understandable and useful to clinicians. Four hypotheses were tested using a pipeline that consisted of UMAP dimensionality reduction, HDBSCAN density-based clustering, and multiple imputation methods for missing clinical data.

Overall, the major finding of this research was that the cognitive structure found through the clustering process represents a cognitive severity gradient, not a distinct number of phenotypes. The cohort represents a single dimension of overall cognitive severity. The first principal component accounts for approximately 56% of the total variability among the six cognitive domains, with almost identical positive weights. The pipeline takes this continuum and divides it into three tiers: Above Average (38.6%, $`n = 6{,}725`$), Near Normal (36.4%, $`n = 6{,}328`$), and Globally Impaired (25.0%, $`n = 4{,}353`$). The level determines which tier a participant falls into. Within the present domain-aggregated clustering framework, there is no evidence that profile shape drives this outcome.

Hypothesis 1 is supported with an important caveat. There are identifiable clusters that are relatively stable. However, these are best viewed as severity bands. Each of the ten imputation methods meets the pre-specified silhouette and noise thresholds, and the two extreme tiers remained fairly consistent under Hennig per-cluster matching (Core Jaccard 0.63 and 0.62, respectively; §<a href="#sec:h1_results" data-reference-type="ref" data-reference="sec:h1_results">4.5</a>). Because silhouette was evaluated in the selected UMAP embedding, the absolute value is optimistic and should be read alongside the PCA, seed-stability, and sensitivity analyses.

Hypothesis 2 is also supported, with a defined scope. The primary tier solution was obtained with UMAP+HDBSCAN, but the imputation-sensitivity test used a secondary fixed-reference diagnostic: a common StandardScaler, UMAP embedding, and $`k`$-means partition fitted on MICE with $`k=3`$. Under that fixed labelling rule, the average Adjusted Rand Index across all forty-five pairwise method comparisons is 0.710 (95% bootstrap CI \[0.704, 0.716\]), greater than the 0.500 threshold. This establishes that point assignments are robust to imputation under a fixed embedding and partition. It does not imply that independently refitted HDBSCAN pipelines recover an identical density hierarchy or tier count; the full UMAP+HDBSCAN runs vary from $`k=3`$ to $`k=5`$, and the Rubin-pooled multiple-imputation draws vary from $`k=3`$ to $`k=7`$, consistent with discretising a continuum. Following Holm-Bonferroni adjustment, forty-four of forty-five pairwise combinations reject $`H_0: \mathrm{ARI} \leq 0.5`$ at $`\alpha = 0.05`$. Only KNN-SoftImpute is borderline. Consensus clustering achieves a mean confidence of 0.929, with 86.2 percent of assessments receiving high-confidence assignment. The baseline comparison with listwise deletion verifies that imputation is analytically required: removing missing values from 46.9 percent of the assessments alters the number of clusters and lowers the silhouette value to 0.257.

Hypothesis 3 is supported as well. Clinical Unit is significantly correlated with cognitive severity tier ($`\chi^2 = 911.3`$, $`p \approx 4 \times 10^{-156}`$); however, the magnitude of the correlation is small (Cramér’s $`V = 0.162`$). The Cochran-Mantel-Haenszel statistic demonstrates that clinical unit is not solely determined by diagnosis group (Cochran 1954). Thus, cognitive severity appears to contribute to clinical unit designation independently of diagnostic category.

Lastly, Hypothesis 4 is supported. Domain-level aggregation generates cluster separation comparable to variable-level features (silhouette 0.481 vs. 0.473), and domain-level aggregation also decreases multivariate collinearity (mean VIF 1.88 vs. 2.77) and increases numerical stability (11.8 vs. 61.7). These results provide empirical support for conceptualizing cognitive performance at the domain level.

## Methodological Contribution

There are two methodological contributions made within this dissertation. First, an imputation-robustness framework is presented. The combination of ARI/NMI comparison and consensus confidence measures provides a systematic means to evaluate whether differences in assignments arise due to differing missing-value algorithms under a fixed reference embedding and partition. Due to its domain-agnostic nature, the framework may be employed with other types of partially observed clinical or biomedical data, including genomic data or survey responses, provided that users do not conflate this fixed-reference diagnostic with refitting the primary clustering algorithm.

Second, a cautionary note is provided regarding feature engineering. As demonstrated in this dissertation, unsupervised cognitive phenotyping is very susceptible to how features are constructed. For example, inclusion of an unintended demographic variable or failure to include any cognitive test information in the assessment record can create an artifact representing what appears to be a phenotypic grouping that in reality arises from poor construction of features. The pipeline developed in this dissertation reduces this potential source of error by excluding non-cognitive variables, ensuring that at least one cognitive variable exists for each assessment record, and performing Winsorisation, direction-alignment, and standardization on each variable prior to aggregation. Clinical labeling should occur only after these processing steps have taken place and evaluation for sensitivity.

## Clinical Recommendations

Based upon these findings, I recommend the following:

- Use a global severity index to supplement a diagnosis. The global severity index provides a reproducible summary description of overall cognitive function at time of assessment, regardless of the type of assessment (including imputed values for uncompleted tests). Rehabilitation teams can use both the diagnosis and a global severity index to inform their determination of appropriate treatment intensity for each patient.

<!-- -->

- Label uncertain cases instead of discarding them. Consensus clustering provides high confidence labels for 86.2 percent of assessments but about 2,400 assessments lie close to a tier boundary and thus will vary depending on choice of algorithm. Decision-support systems should report the confidence with which labels were generated instead of artificially confining label certainty uniformly.

<!-- -->

- Choose model-based imputation for practical use. Although MICE, EM, MissForest, and autoencoder imputation produce similarly robust results (pairwise ARI values as large as 0.88) compared to each other, KNN tends to behave differently from the others and Mean Imputation loses variance relative to the others. Therefore, MICE seems like a reasonable choice for practical application purposes whereas MissForest may prove useful for nonparametric modeling applications where nonlinear relationships are expected.

<!-- -->

- Develop treatment objectives at the domain level. Clustering at the domain level produces separations among clusters similar to variable-level aggregation while simultaneously reducing multivariate collinearity (mean VIF 1.88 vs. 2.77) and increasing numerical conditioning (11.8 vs. 61.7). This lends further support to the long-established neuropsychological practice of evaluating batteries according to domain of cognitive functioning (Lezak et al. 2012).

## Final Remarks

Using a dimensional reduction technique called UMAP and clustering technique called HDBSCAN on reduced data with imputation algorithms that handle missing values, this study demonstrates that unsupervised clustering can uncover a continuous cognitive severity gradient in ABI that is robust to different imputation strategies and clinical groups and interpretable at the domain level. Furthermore, this research shows that there are no separate phenotypes in this cohort but rather a single dimension of overall cognitive severity.

Therefore, this dissertation provides empirical support for developing rehabilitation planning guidelines using severity levels for patients who have suffered an acquired brain injury. Future studies will be needed to validate the usefulness of using cognitive severity levels for rehabilitation planning purposes:

- Does cognitive severity levels predict future outcomes better than diagnosis and current measures?

<!-- -->

- Would using a severity system improve resource allocation in controlled environments or is it just a formalization of what was discovered in CMH analyses?

<!-- -->

- Are there additional subgroups present in independent cohorts across multiple centers that were not evident in this sample or do they emerge due to varying characteristics of the populations sampled and/or assessment times?

# Imputation Hyperparameters

This appendix lists the hyperparameters used for each of the ten imputation methods evaluated in this thesis. Settings followed published defaults where defaults exist; remaining choices were selected by cross-validation or grid search as noted. The methods themselves are described in Chapter <a href="#Chapter3" data-reference-type="ref" data-reference="Chapter3">3</a>, §<a href="#sec:imputation" data-reference-type="ref" data-reference="sec:imputation">3.3</a>.

<div id="tab:imputation_hyperparams">

| **Method** | **Hyperparameters** |
|:---|:---|
| Mean | Single-pass arithmetic mean per variable. |
| EM | Multivariate normal model; convergence $`10^{-6}`$; max 500 iterations. |
| MICE | Linear regression per variable; 10 iterations; single imputed dataset for clustering. |
| KNN | $`k = 5`$; inverse-distance weighting; Euclidean distance. |
| MissForest | 100 trees per forest; up to 10 iterations; variables imputed in order of increasing missingness. |
| PMM | 5 donors; 10 iterations; implemented within the MICE framework. |
| SoftImpute | Regularisation chosen by cross-validation over 20 log-spaced values from $`10^{-3}`$ to $`10^{2}`$; convergence $`10^{-5}`$; max 200 iterations. |
| NMF | Rank $`r = 5`$ selected by grid search over $`\{2, 3, 5, 7, 10\}`$; multiplicative updates; max 500 iterations. |
| DAE | Architecture $`15 \to 128 \to 64 \to 32 \to 64 \to 128 \to 15`$; ReLU + batch normalisation; dropout $`(0.5, 0.3)`$; corruption rate 20% with pattern-aware masking; MSE loss on observed entries; Adam optimiser ($`\text{lr} = 10^{-3}`$); ReduceLROnPlateau + early stopping (patience 20); 5 runs averaged. |
| VAE | Same layer dimensions as DAE; latent dim 32; loss $`=`$ MSE $`+`$ $`\beta`$-weighted KL divergence; cyclical annealing with $`\beta_{\max} = 0.1`$ over 40-epoch cycles; $`K = 20`$ latent samples averaged for final imputation. |

Hyperparameters for the ten imputation methods.

</div>

# List of Abbreviations

The abbreviations and acronyms used throughout this thesis are listed below.

|  |  |
|:---|:---|
| **ABI** | Acquired Brain Injury |
| **ANOVA** | Analysis of Variance |
| **ARI** | Adjusted Rand Index (chance-corrected cluster agreement, $`-1`$ to $`+1`$) |
| **BH** | Benjamini–Hochberg (false-discovery-rate correction) |
| **BIC** | Bayesian Information Criterion (model-selection criterion) |
| **CI** | Confidence interval (95% unless otherwise stated) |
| **CMH** | Cochran-Mantel-Haenszel (stratified association test) |
| **DAE** | Denoising Autoencoder (deep-learning imputation) |
| **DBSCAN** | Density-Based Spatial Clustering of Applications with Noise |
| **ELBO** | Evidence Lower Bound (VAE training objective) |
| **EM** | Expectation–Maximisation (maximum-likelihood imputation) |
| **FDR** | False discovery rate (controlled by Benjamini–Hochberg) |
| **FWER** | Family-wise error rate (controlled by Holm–Bonferroni) |
| **GAIN** | Generative Adversarial Imputation Networks |
| **GAN** | Generative Adversarial Network |
| **GMM** | Gaussian Mixture Model |
| **HDBSCAN** | Hierarchical Density-Based Spatial Clustering of Applications with Noise |
| **IQR** | Interquartile Range (spread used by the robust scaler) |
| **KL** | Kullback–Leibler (divergence term in the VAE loss) |
| **KNN** | K-Nearest Neighbours |
| **KW** | Kruskal-Wallis (non-parametric extension of one-way ANOVA) |
| **MAE** | Mean Absolute Error |
| **MAR** | Missing At Random |
| **MCAR** | Missing Completely At Random |
| **MICE** | Multiple Imputation by Chained Equations |
| **MIDA** | Multiple Imputation using Denoising Autoencoders |
| **MLE** | Maximum Likelihood Estimation |
| **MNAR** | Missing Not At Random |
| **MSE** | Mean Squared Error |
| **NMF** | Non-Negative Matrix Factorisation |
| **NMI** | Normalised Mutual Information (information-theoretic cluster agreement, $`0`$ to $`1`$) |
| **NN** | Near-Normal (the middle cognitive severity tier in the MICE solution) |
| **PCA** | Principal Component Analysis |
| **PMM** | Predictive Mean Matching (semi-parametric imputation, runs inside MICE) |
| **RAVLT** | Rey Auditory Verbal Learning Test |
| **RMSE** | Root Mean Squared Error |
| **TBI** | Traumatic Brain Injury |
| **TMT** | Trail Making Test |
| **TSI** | Time Since Injury (days at assessment) |
| **t-SNE** | t-distributed Stochastic Neighbour Embedding |
| **UMAP** | Uniform Manifold Approximation and Projection |
| **VAE** | Variational Autoencoder (deep-learning imputation with latent sampling) |
| **VIF** | Variance Inflation Factor (multicollinearity diagnostic) |

<div id="refs" class="references csl-bib-body hanging-indent" entry-spacing="0">

<div id="ref-afkanpour2024identify" class="csl-entry">

Afkanpour, Mitra et al. 2024. “Identify the Most Appropriate Imputation Method for Handling Missing Values in Clinical Structured Datasets: A Systematic Review.” *BMC Medical Research Methodology* 24 (1): 188.

</div>

<div id="ref-bellio2020analyzing" class="csl-entry">

Bellio, Marco, Neil P. Oxtoby, Zuzana Walker, Susie M. D. Henley, Annemie Ribbens, Ann Blandford, Daniel C. Alexander, and Keir X. X. Yong. 2020. “Analyzing Large <span class="nocase">Alzheimer’s</span> Disease Cognitive Datasets: Considerations and Challenges.” *Alzheimer’s & Dementia: Diagnosis, Assessment & Disease Monitoring* 12 (1). <https://doi.org/10.1002/dad2.12135>.

</div>

<div id="ref-boulesteix2012overview" class="csl-entry">

Boulesteix, Anne-Laure, Silke Janitza, Jochen Kruppa, and Inke R. König. 2012. “Overview of Random Forest Methodology and Practical Guidance with Emphasis on Computational Biology and Bioinformatics.” *WIREs Data Mining and Knowledge Discovery* 2 (6): 493–507. <https://doi.org/10.1002/widm.1072>.

</div>

<div id="ref-brazinova2021epidemiology" class="csl-entry">

Brazinova, Alexandra, Veronika Rehorcikova, Mark S Taylor, Veronika Buckova, Marek Majdan, Marek Psota, Wouter Peeters, et al. 2021. “Epidemiology of Traumatic Brain Injury in Europe: A Living Systematic Review.” *Journal of Neurotrauma* 38 (10): 1411–40. <https://doi.org/10.1089/neu.2015.4126>.

</div>

<div id="ref-vanbuuren2011mice" class="csl-entry">

Buuren, Stef van, and Karin Groothuis-Oudshoorn. 2011. “Mice: Multivariate Imputation by Chained Equations in R.” *Journal of Statistical Software* 45 (3): 1–67. <https://doi.org/10.18637/jss.v045.i03>.

</div>

<div id="ref-cochran1954some" class="csl-entry">

Cochran, William G. 1954. “Some Methods for Strengthening the Common Chi-Squared Tests.” *Biometrics* 10 (4): 417–51.

</div>

<div id="ref-corrigan2010epidemiology" class="csl-entry">

Corrigan, John D, Anbesaw W Selassie, and Jean A Orman. 2010. “The Epidemiology of Traumatic Brain Injury.” *The Journal of Head Trauma Rehabilitation* 25 (2): 72–80. <https://doi.org/10.1097/HTR.0b013e3181ccc8b4>.

</div>

<div id="ref-dempster1977maximum" class="csl-entry">

Dempster, Arthur P, Nan M Laird, and Donald B Rubin. 1977. “Maximum Likelihood from Incomplete Data via the EM Algorithm.” *Journal of the Royal Statistical Society: Series B* 39 (1): 1–38.

</div>

<div id="ref-garcia2020data" class="csl-entry">

García-Rudolph, Alejandro, Alberto García-Molina, Eloy Opisso, Josep María Tormos, Vince I Madai, Dietmar Frey, and Montserrat Bernabeu. 2021. “Neuropsychological Assessments of Patients with Acquired Brain Injury: A Cluster Analysis Approach to Address Heterogeneity in Web-Based Cognitive Rehabilitation.” *Frontiers in Neurology* 12: 701946.

</div>

<div id="ref-gondara2018mida" class="csl-entry">

Gondara, Lovedeep, and Ke Wang. 2018. “MIDA: Multiple Imputation Using Denoising Autoencoders.” In *Advances in Knowledge Discovery and Data Mining (PAKDD)*, 260–72. Springer.

</div>

<div id="ref-gravesteijn2021missing" class="csl-entry">

Gravesteijn, Benjamin Y., Charlie A. Sewalt, Esmee Venema, Daan Nieboer, Ewout W. Steyerberg, et al. 2021. “Missing Data in Prediction Research: A Five-Step Approach for Multiple Imputation, Illustrated in the CENTER-TBI Study.” *Journal of Neurotrauma* 38 (13): 1842–57. <https://doi.org/10.1089/neu.2020.7218>.

</div>

<div id="ref-hennig2007cluster" class="csl-entry">

Hennig, Christian. 2007. “Cluster-Wise Assessment of Cluster Stability.” *Computational Statistics & Data Analysis* 52 (1): 258–71.

</div>

<div id="ref-hubert1985comparing" class="csl-entry">

Hubert, Lawrence, and Phipps Arabie. 1985. “Comparing Partitions.” *Journal of Classification* 2 (1): 193–218.

</div>

<div id="ref-kingma2014auto" class="csl-entry">

Kingma, Diederik P, and Max Welling. 2014. “Auto-Encoding Variational Bayes.” *arXiv Preprint arXiv:1312.6114*.

</div>

<div id="ref-lee1999learning" class="csl-entry">

Lee, Daniel D, and H Sebastian Seung. 1999. “Learning the Parts of Objects by Non-Negative Matrix Factorization.” *Nature* 401 (6755): 788–91.

</div>

<div id="ref-lezak2012neuropsychological" class="csl-entry">

Lezak, Muriel D, Diane B Howieson, Erin D Bigler, and Daniel Tranel. 2012. *Neuropsychological Assessment*. 5th ed. New York: Oxford University Press.

</div>

<div id="ref-little2019statistical" class="csl-entry">

Little, Roderick JA, and Donald B Rubin. 2019. *Statistical Analysis with Missing Data*. 3rd ed. Hoboken, NJ: John Wiley & Sons. <https://doi.org/10.1002/9781119482260>.

</div>

<div id="ref-maas2017traumatic" class="csl-entry">

Maas, Andrew IR et al. 2017. “Traumatic Brain Injury: Integrated Approaches to Improve Prevention, Clinical Care, and Research.” *The Lancet Neurology* 16 (12): 987–1048. <https://doi.org/10.1016/S1474-4422(17)30371-X>.

</div>

<div id="ref-mattei2019miwae" class="csl-entry">

Mattei, Pierre-Alexandre, and Jes Frellsen. 2019. “MIWAE: Deep Generative Modelling and Imputation of Incomplete Data Sets.” In *Proceedings of the 36th International Conference on Machine Learning (ICML)*, 97:4413–23.

</div>

<div id="ref-mazumder2010spectral" class="csl-entry">

Mazumder, Rahul, Trevor Hastie, and Robert Tibshirani. 2010. “Spectral Regularization Algorithms for Learning Large Incomplete Matrices.” *Journal of Machine Learning Research* 11: 2287–2322.

</div>

<div id="ref-mccoy2018variational" class="csl-entry">

McCoy, John T, Steve Kroon, and Lidia Auret. 2018. “Variational Autoencoders for Missing Data Imputation with Application to a Simulated Milling Circuit.” *IFAC-PapersOnLine* 51 (21): 141–46. <https://doi.org/10.1016/j.ifacol.2018.09.406>.

</div>

<div id="ref-mcinnes2018umap" class="csl-entry">

McInnes, Leland, John Healy, and James Melville. 2018. “UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction.” *arXiv Preprint arXiv:1802.03426*. <https://doi.org/10.48550/arXiv.1802.03426>.

</div>

<div id="ref-pinsky2023mad" class="csl-entry">

Pinsky, Eugene, and Sidney Klawansky. 2023. “MAD (about Median) Vs. Quantile-Based Alternatives for Classical Standard Deviation, Skewness, and Kurtosis.” *Frontiers in Applied Mathematics and Statistics* 9. <https://doi.org/10.3389/fams.2023.1206537>.

</div>

<div id="ref-ponsford2014longitudinal" class="csl-entry">

Ponsford, Jennie L et al. 2014. “Longitudinal Follow-up of Patients with Traumatic Brain Injury: Outcome at Two, Five, and Ten Years Post-Injury.” *Journal of Neurotrauma* 31 (1): 64–77. <https://doi.org/10.1089/neu.2013.2997>.

</div>

<div id="ref-prakash2024benchmarking" class="csl-entry">

Prakash, Prabhat, Kelsey Street, Sanjay Narayanan, Bryan A. Fernandez, Yiqing Shen, and Catherine Shu. 2024. “Benchmarking Machine Learning Missing Data Imputation Methods in Large-Scale Mental Health Survey Databases.” *medRxiv*. <https://doi.org/10.1101/2024.05.13.24307231>.

</div>

<div id="ref-rabinowitz2014neuropsychological" class="csl-entry">

Rabinowitz, Amanda R, and Harvey S Levin. 2014. “Neuropsychological Recovery Trajectories in Moderate to Severe Traumatic Brain Injury: Influence of Patient Characteristics and Diffuse Axonal Injury.” *Journal of the International Neuropsychological Society* 20 (1): 82–92.

</div>

<div id="ref-robert2020comparing" class="csl-entry">

Robert, Valérie, Yann Vasseur, and Vincent Brault. 2020. “Comparing High-Dimensional Partitions with the Co-Clustering Adjusted Rand Index.” *Journal of Classification* 38 (1): 158–86. <https://doi.org/10.1007/s00357-020-09379-w>.

</div>

<div id="ref-rousseeuw1987silhouettes" class="csl-entry">

Rousseeuw, Peter J. 1987. “Silhouettes: A Graphical Aid to the Interpretation and Validation of Cluster Analysis.” *Journal of Computational and Applied Mathematics* 20: 53–65.

</div>

<div id="ref-rubin1976inference" class="csl-entry">

Rubin, Donald B. 1976. “Inference and Missing Data.” *Biometrika* 63 (3): 581–92. <https://doi.org/10.1093/biomet/63.3.581>.

</div>

<div id="ref-rubin1987multiple" class="csl-entry">

———. 1987. *Multiple Imputation for Nonresponse in Surveys*. New York: John Wiley & Sons. <https://doi.org/10.1002/9780470316696>.

</div>

<div id="ref-saatman2008classification" class="csl-entry">

Saatman, Kathryn E et al. 2008. “Classification of Traumatic Brain Injury for Targeted Therapies.” *Journal of Neurotrauma* 25 (7): 719–38. <https://doi.org/10.1089/neu.2008.0586>.

</div>

<div id="ref-shannon1948mathematical" class="csl-entry">

Shannon, Claude E. 1948. “A Mathematical Theory of Communication.” *Bell System Technical Journal* 27 (3): 379–423. <https://doi.org/10.1002/j.1538-7305.1948.tb01338.x>.

</div>

<div id="ref-stekhoven2012missforest" class="csl-entry">

Stekhoven, Daniel J, and Peter Bühlmann. 2012. “MissForest—Non-Parametric Missing Value Imputation for Mixed-Type Data.” *Bioinformatics* 28 (1): 112–18. <https://doi.org/10.1093/bioinformatics/btr597>.

</div>

<div id="ref-troyanskaya2001missing" class="csl-entry">

Troyanskaya, Olga et al. 2001. “Missing Value Estimation Methods for DNA Microarrays.” *Bioinformatics* 17 (6): 520–25.

</div>

<div id="ref-vinh2010information" class="csl-entry">

Vinh, Nguyen Xuan, Julien Epps, and James Bailey. 2010. “Information Theoretic Measures for Clusterings Comparison: Variants, Properties, Normalization and Correction for Chance.” *Journal of Machine Learning Research* 11: 2837–54.

</div>

<div id="ref-yoon2018gain" class="csl-entry">

Yoon, Jinsung, James Jordon, and Mihaela van der Schaar. 2018. “GAIN: Missing Data Imputation Using Generative Adversarial Nets.” In *Proceedings of the 35th International Conference on Machine Learning (ICML)*, 80:5689–98.

</div>

</div>
