<!-- Exported prose chunk 3. Word count: 1257. -->


## Imputation Methods

_Source: `report/Chapters_short/Chapter2.tex`_

The ten methods used in this thesis are introduced below in order of increasing complexity. Let mathbf{X}inmathbb{R}^{ntimes p} be the data matrix containing n assessments and p variables, with entries x_{ij}. The observed entries are indexed by Omega={(i,j):x_{ij}text{ is observed}}, and Omega_j={i:(i,j)inOmega} denotes the observed rows for variable j. The operator P_Omega keeps observed entries unchanged and sets unobserved entries to zero. The goal is to estimate hat{x}_{ij} for entries not in Omega.

Mean imputation. Mean imputation replaces each missing value with the arithmetic mean of the observed values for that variable. This method is fast and requires no iteration. Its simplicity is also its main weakness: it reduces variances and covariances, distorts marginal distributions, and leads to underestimated standard errors. It is therefore used here only as a baseline.

K-Nearest Neighbours (KNN). KNN imputation identifies the k most similar donor cases and fills the missing value with a weighted average of their observed values, using Euclidean distance as the similarity measure [@troyanskaya2001missing]. where mathcal{N}_i is the set of k nearest donors and d(i,k) is the distance between observations on the jointly observed variables. Because it is non-parametric, KNN can capture local structure more flexibly than mean imputation. Its main limitation is the choice of k: small values may fit noise, while large values may over-smooth meaningful patterns. It can also become computationally expensive as the dataset grows.

MICE. Multiple Imputation by Chained Equations imputes each variable conditional on the others and repeats this process over several iterations [@vanbuuren2011mice]. In iteration t, each variable is redrawn from its conditional model: where mathbf{x}_{i,-j} denotes all variables except j for case i. The conditional model can be adapted to the data type, for example linear for continuous variables and logistic for binary variables. MICE preserves multivariate relationships and can generate multiple imputations to quantify uncertainty. Its limitations are the need to specify a model for each variable and the possibility of convergence problems.

Predictive Mean Matching (PMM). PMM is a semi-parametric method often used within MICE. A regression model first generates predictions hat{x}_{ij}=mathbf{x}_{i,-j}hat{boldsymbolbeta}_j. The imputed value is then sampled from observed cases with similar predicted values: This keeps imputed values within the range of observed data and avoids impossible values, such as negative scores on tests with a floor. The main limitation is that a small donor pool can lead to repeated use of the same observed cases.

MissForest. MissForest is an iterative random-forest imputation method [@stekhoven2012missforest]. For each variable j, a forest f_j is trained on the available data using the remaining variables as predictors. Missing values are then updated, and the process repeats until the changes become small: Because it is non-parametric, MissForest can model non-linear relationships and mixed data types. It often performs well in benchmark studies, but it is computationally demanding and scales poorly when the number of rows or trees is large.

Expectation-Maximisation (EM). EM alternates between an E-step, which estimates expected sufficient statistics, and an M-step, which updates the parameters by maximum likelihood [@dempster1977maximum]. Under multivariate normality, it converges to the maximum-likelihood estimate and imputes missing blocks using their conditional mean: with boldsymbolmu and Sigma re-estimated at each step. If variables are strongly skewed or bounded, however, the normality assumption may be unrealistic.

SoftImpute. SoftImpute uses a soft-thresholded singular value decomposition to estimate a low-rank version of the data matrix [@mazumder2010spectral]. It solves where the singular values are soft-thresholded, S_lambda(Z)=Uoperatorname{diag}bigl((d_i-lambda)_+bigr)V^top. The lambda parameter controls the effective rank of the approximation. SoftImpute is efficient for large sparse matrices, but it may miss structure that cannot be represented well by a low-rank model.

Non-Negative Matrix Factorisation (NMF). This factors the data into two non-negative, lower-rank matrices [@lee1999learning]: The non-negativity constraint is suitable for neuropsychological scores that cannot fall below zero, and the resulting factors can sometimes be interpreted as additive cognitive components. Like SoftImpute, NMF works best when the data can be summarised by a small number of non-negative factors. The selected rank r is therefore important.

Denoising Autoencoder (DAE). A DAE trains a neural network to reconstruct complete data from deliberately corrupted inputs, following the MIDA framework [@gondara2018mida]. With encoder f_theta, decoder g_theta, and corrupted input tilde{mathbf{x}}, training minimises the reconstruction loss: Multiple imputations are obtained by training several networks with different random seeds and averaging their reconstructions. DAEs can outperform classical methods in settings where variables have strong non-linear relationships.

Variational Autoencoder (VAE). A VAE builds a generative latent-space model by mapping observations to probability distributions [@kingma2014auto, mccoy2018variational]. Training maximises the evidence lower bound (ELBO): where the prior is p(z)=mathcal{N}(mathbf{0},mathbf{I}) and beta weights the regularisation term. [@mattei2019miwae] proposed importance-weighted bounds for missing data, while [@yoon2018gain] proposed a GAN-based alternative. In VAEs, imputations are generated by sampling from the latent distribution and decoding each draw, which provides a principled way to represent uncertainty if the model is trained carefully.

Deep-learning methods require more computation than simpler methods, but they offer two potential advantages. They can capture non-linear structure without an explicit parametric model, and their stochastic components, such as dropout in a DAE or latent sampling in a VAE, can naturally generate multiple imputations. Their disadvantages are sensitivity to overfitting and to architectural choices. This thesis evaluates how well they perform on the small-to-moderate, low-dimensional data typical of clinical neuropsychology [@prakash2024benchmarking].

[@afkanpour2024identify] classify imputation methods for clinical research into four groups: conventional methods (mean, EM, MICE), machine learning methods (KNN, MissForest), hybrids such as PMM, and matrix completion methods (SoftImpute, NMF). I add a fifth group, deep learning, for DAE and VAE. Comparing methods across these categories allows the thesis to test whether the recovered cognitive structure is robust to the assumptions of the imputation method.



## Clustering in Neuropsychology

_Source: `report/Chapters_short/Chapter2.tex`_

Cluster analysis has a substantial history in neuropsychological research. Across cohorts such as stroke, TBI, and mild cognitive impairment, data-driven groupings often fail to align with the diagnostic or severity categories used in referral and triage. That mismatch is clinically informative: it suggests that medical categories do not fully encode cognitive heterogeneity.

Reviewing data-driven cognitive phenotyping after brain injury, [@garcia2020data] identify several recurrent patterns. Studies often recover two to four subgroups; these groups are usually described through relative cognitive strengths and weaknesses rather than through a single severity level; and, when external outcomes are available, subgroup membership can relate to clinically meaningful endpoints such as return to work.

The evidential base remains constrained. Samples are frequently small, often below 200 participants. Complete-case analysis is common, even though excluding patients with any missing value can bias the sample when missingness is informative. Algorithmic sensitivity is rarely examined systematically, and the routine use of k-means requires the number of clusters to be fixed before the data are inspected.

This thesis addresses those limitations through four design choices. It uses a larger clinical dataset (Chapter Chapter3), compares ten imputation methods against complete-case analysis, evaluates sensitivity to hyperparameters and missingness thresholds, and applies HDBSCAN, allowing low-density observations to be treated as noise rather than forced into pre-specified centroids.



## UMAP and HDBSCAN

_Source: `report/Chapters_short/Chapter2.tex`_

The clustering pipeline has two main steps. First, UMAP reduces the dimensionality of the data. Second, HDBSCAN identifies dense regions of observations as clusters.

---REWORK


## Methods of Imputation

_Source: `report/Chapters_short/Chapter2.tex`_

Each of the ten methods used in this dissertation will be presented in order of increasing complexity. Consider the data matrix X in R^n × p, which contains n assessments and p variables. Assume the ith assessment includes p variables x_{ij}, and let Ω = {(i, j): x_{ij} is observed}. Then Ω_j = {i : (i, j) ∈ Ω} represents the observed rows for the jth variable. Define the operator P_Omega as follows: for any entry x_ij of the matrix X, P_Omega(x_{ij}) = x_{ij}, if x_{ij} ∈ Ω; otherwise, P_Omega(x_{ij}) = 0. The objective is to estimate x̂_ij for entries not in Ω.

### Mean Imputation Method

The mean imputation method substitutes each missing value with the arithmetic mean of the observed values for that variable. The mean imputation method is fast and does not require any iteration. However, it reduces variance and covariance, creates distorted marginal distributions, and results in underestimated standard errors. Therefore, it was only used in this study as a baseline.

### K-Nearest Neighbors (KNN)

The KNN imputation method finds the k most similar donor cases and assigns the missing value a weighted average of their observed values based on the Euclidean distance as the similarity measure. We can define the KNN imputation method as follows:

where ∣∣∣mathcal{N}_id(k)∣∣∣=k and d(i,k)=∑_(j∈Ω_j)(x_{jk}-x_{ik}), where d(i,k) is the distance between observations on the jointly observed variables. Since KNN is a non-parametric method, it can better capture the local structure than mean imputation. There are some limitations for KNN. Small values of k may fit the noise, while large values of k may smooth too much meaningful pattern. As the size of the dataset increases, the computational cost of KNN becomes greater.

### Multiple Imputation by Chained Equations (MICE)

Multiple Imputation by Chained Equations imputes each variable conditionally on all other variables and iteratively repeats this process over several iterations [@vanbuuren2011mice]. In each iteration t, each variable is drawn anew from its conditional model:

We can adapt the form of the conditional model to the type of data; e.g., we can use linear models for continuous variables and logistic models for binary variables. MICE retains multivariate relationships and can produce multiple imputations to quantify uncertainty. One of its limitations is that we must specify a model for every variable, and there are possibilities for problems during convergence.

### Predictive Mean Matching (PMM)

PMM is a semi-parametric method that is commonly employed within MICE. The predictive mean matching algorithm first predicts new values for each missing value using a regression model. The imputed value is then randomly selected from among all previously observed values with similarly predicted values:

In doing so, imputed values will always lie within the range of observed data, thus avoiding impossible values (e.g., negative scores on tests that include floors). However, one limitation is that a limited donor pool can cause repeated usage of the same observed values.

### MissForest

MissForest is an iterative random-forest imputation method [@stekhoven2012missforest]. For each variable j, we train a forest f_j using all available data with the remaining variables as predictors. Afterward, we update missing values using the newly created forest and repeat this procedure until little change occurs:

Because MissForest is a non-parametric method, it can model complex non-linear relationships and accommodate both continuous and discrete variables. Often MissForest performs well on benchmark datasets; however, it is computationally intensive and scales poorly when either the number of rows or trees is large.

### Expectation-Maximization (EM)

EM is another method that iterates between an E-step, which computes the expected sufficient statistic, and an M-step, which adjusts the parameters by maximizing the log-likelihood [@dempster1977maximum]. When assuming multivariate normality, EM converges to the maximum likelihood estimator, and missing blocks are filled-in using their conditional mean:

with the parameters mu and Sigma being re-computed at each step. However, if many of the variables are severely skewed or bounded, then the multivariate normality assumption may be unreasonable.

### SoftImpute

SoftImpute employs a soft-thresholded singular-value decomposition to estimate a low-rank representation of the original data matrix [@mazumder2010spectral]. It solves:

where S_lambda(Z)=Uoperatorname{diag}bigl((d_i-lambda)_+bigr)V^top. Thus, lambda determines what percentage of the variation in Z can be captured. Although SoftImpute is highly efficient for large sparse matrices, it could potentially ignore structure that does not fit within a low-rank model.

### Non-Negative Matrix Factorization (NMF)

Similarly to SoftImpute, NMF factorizes the data into two non-negative lower-rank matrices [21]:

The non-negative constraints make sense in terms of neuropsychological scores since they cannot be less than zero. Additionally, the factors derived from NMF can sometimes be interpreted as additive contributions to cognition. Similar to SoftImpute, NMF works best when the data can be summarized by a small number of non-negative factors. Thus, choosing the correct rank r is critical.

### Denoising Autoencoder (DAE)

A denoising autoencoder (DAE) trains a neural network to predict complete data given intentionally degraded versions of that data under the MIDA framework [@gondara2018mida]. Using encoder f_theta , decoder g_theta , and corrupted input ~{\mathbf{x}} , the goal is to minimize the reconstruction error:

Thus, imputations are made by training multiple networks with varying random seed numbers and taking averages of their reconstructions. DAEs may outperform traditional methods when there are strong non-linear relationships among variables.

### Variational Autoencoder (VAE)

A variational autoencoder (VAE) constructs a probabilistic generative latent space model by mapping observations onto probability distributions [22], [23]. To maximize the evidence lower bound (ELBO):

the prior is assumed to follow p(z)=\mathcal{N}(mathbf{0},mathbf{I}). Recently [@mattei2019miwae] proposed importance-weighted bounds for missing data while [@yoon2018gain] proposed a GAN-based approach. In VAEs, imputed values are produced via samples from the latent distribution followed by decodings of each sample, providing a natural mechanism for representing uncertainty if trained properly.

Deep learning methods typically require more computation than simple methods; however, they provide two potential benefits. They allow capturing non-linear structures without an explicit parametric model; additionally their stochastic elements — e.g., dropout in DAEs or latent sampling in VAEs — provide a natural mechanism for generating multiple imputations. Two disadvantages of deep learning methods are: sensitivity to overfitting and dependency upon architecture choices. This dissertation examines how well they function on the relatively small-to-medium sized low dimensional data characteristic of clinical neuropsychology [@prakash2024benchmarking]

[@afkanpour2024identify] categorize imputation methods for clinical research into four classes: traditional methods (mean, EM, MICE); machine learning methods (KNN, MissForest); hybrid methods like PMM; and matrix completion methods like SoftImpute and NMF. I add a fifth class to these: Deep Learning — specifically for DAEs and VAEs. By comparing methods across these classes we can determine whether the recovered cognitive structure is stable across assumptions of the imputation method.

## Cluster Analysis in Neuropsychology

_Source: `report/Chapters_short/Chapter2.tex`_

Cluster analysis has been extensively applied to neuropsychological research. Clinical diagnoses or levels of severity are typically established through diagnostic or severity categories; yet cluster analyses conducted across various cohorts including stroke, traumatic brain injury (TBI), mild cognitive impairment (MCI) — often result in data-driven groupings that do not correspond with clinical categories or severity classifications. Clinically speaking this disparity indicates that medical classifications do not effectively reflect cognitive heterogeneity.

Data-driven cognitive phenotyping following brain injury were reviewed in [@garcia2020data]; several consistent trends emerged throughout reviews. Data-driven grouping methods typically yield two to four subgroups; subgroups are often identified based on relative strengths and weaknesses in cognition compared to overall levels of severity; and, when relevant outcome measures are provided, subgroup classification can correlate with clinically significant endpoints — such as return to work.

However, as discussed above, there remain significant gaps in evidence regarding data-driven cognitive phenotyping following brain injury. Sample sizes are generally very small — often <200 participants; missing values are frequently excluded using complete-case analysis — although exclusion of missing values could introduce biases in samples when missingness is informative; and algorithmic sensitivities are seldom evaluated systemically in previous studies; furthermore k-means — a widely used clustering algorithm — requires users to fix k prior to examining their data.

Therefore this dissertation proposes four design features to address these issues. It utilizes a larger clinical database (Chapter Chapter3); compares ten imputation methods against complete-case analysis; evaluates sensitivity to hyperparameters and missingness thresholds; and utilizes HDBSCAN — which treats low-density observations as outliers instead of forcing them into pre-determined centroids — to identify dense regions of observation as clusters.

## UMAP and HDBSCAN

_Source: `report/Chapters_short/Chapter2.tex`_

There are two primary components to our clustering pipeline. First UMAP reduces the dimensionality of our data. Second HDBSCAN identifies dense regions of observations as clusters.