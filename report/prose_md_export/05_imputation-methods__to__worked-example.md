<!-- Exported prose chunk 5. Word count: 1391. -->


## Imputation Methods

_Source: `report/Chapters_short/Chapter3.tex`_

I implemented a comparative framework with ten imputation methods across five categories, extending the taxonomy of [@afkanpour2024identify] to include deep learning. Chapter Chapter2, §sec:lit_imputation, explains the rationale for each method. Table tab:method_summary summarises each method's category, year, main trade-offs, and downstream clustering performance. Hyperparameters are listed in Appendix AppendixA, Table tab:imputation_hyperparams. The two deep-learning methods are described in more detail here because their training schedules require additional design choices.

noindent DAE. As a denoising autoencoder, this model is designed to reconstruct complete data from deliberately corrupted inputs. Under a missingness-pattern-aware corruption scheme, the input is masked via tilde{x}_{ij}=m_{ij},x_{ij}. To ensure a diversity of regularisation, half the training samples are given uniform corruption, while for the other half the mask mathbf{m}_i is drawn from the empirical co-occurrence distribution of missing-data patterns: Here P_{mathrm{miss}} is the observed missingness pattern in the data and rho is the rate of uniform corruption. This matters because missingness in clinical data has structure: some tests are absent together because they belong to the same sub-battery or place similar demands on the patient. By training the DAE on corruption patterns that resemble clinical missingness, the model is encouraged to learn inter-variable dependencies relevant to the latent cognitive structure.

noindent VAE. I use a variational autoencoder with an ELBO (Eq. eq:vae) that combines MSE on the observed entries with a Kullback-Leibler divergence term, weighted by beta, to regularise the latent distribution toward a standard Gaussian prior. Keeping beta fixed can lead to posterior collapse, where the model ignores the latent variables and relies mainly on the decoder. To reduce this risk, I use cyclical annealing, which increases beta up to beta_{max} over a cycle of T epochs before resetting it: This schedule alternates between emphasising reconstruction (low beta) and regularising the latent space (high beta).

To evaluate the two deep-learning methods, I performed a held-out evaluation across three folds. In each case I set aside 10 per cent of the observed values in a set H, retrained, and then computed the RMSE and MAE between the imputed and actual figures:

Caption: A summary of the ten imputation methods broken down by the five-category taxonomy. For clustering performance (silhouette score and number of clusters k) I took the best UMAP+HDBSCAN solution on the domain-level features. Note that the silhouette is on the high-density core that HDBSCAN clusters directly (before the k-nearest-neighbour noise-reassignment step), so it runs slightly above the final full-coverage silhouette quoted in the text (for instance MICE scores 0.598 on the core and 0.526 once every assessment is assigned; see §sec:h1_results).



## Domain Score Computation

_Source: `report/Chapters_short/Chapter3.tex`_

Domain-level features were constructed by aggregating variables within each cognitive domain while retaining the 14 individual neuropsychological variables for comparison. Because the original measures combine standardised scores, scaled scores, and raw timed variables such as the Trail Making Test, aggregation without scale harmonisation would be inappropriate. A timed measure with a wide numerical range could otherwise dominate a composite for purely metric reasons.

Three preprocessing operations were applied before aggregation. Each variable was winsorised to the 1st-99th percentile to limit the influence of implausible imputed extremes or sentinel codes. Timed tests were sign-reversed so that higher values consistently denoted better performance. All variables were then z-standardised to zero mean and unit variance. Domain scores were computed as reliability-weighted averages, with each variable assigned weight w_j = 1 - r_j, where r_j is its missingness rate; weights were normalised within domain. Tests administered more frequently therefore contribute more strongly to the corresponding composite. The resulting representation reduces the 14-variable space to six domain scores: orientation, attention, visuoperception, language, memory, and executive function.

This aggregation is methodologically useful but not cost-free. Composite scores tend to be more reliable than single tests because averaging reduces random measurement error, and reducing dimensionality from 14 variables to 6 domains improves the geometry available to distance-based algorithms. Domain-level profiles are also closer to clinical interpretation, since neuropsychologists usually reason about cognitive domains rather than isolated variables. Detail is inevitably lost. Two patients may share the same average memory score while differing in immediate versus delayed recall. Hypothesis H4 tests whether the gains in stability and interpretability justify that compression.



## UMAP + HDBSCAN Pipeline

_Source: `report/Chapters_short/Chapter3.tex`_

Figure fig:pipeline_diagram summarises the pipeline from imputed data to final cluster assignment.

Caption: End-to-end clustering pipeline. After imputed data are run through a robust scaler, they go into a UMAP hyperparameter grid (10 random seeds for each of 9 configurations) and the embedding with the best silhouette is kept. HDBSCAN then does the clustering in a 120-configuration sweep, scored by the composite quality criterion Q = text{silhouette} times (1 - text{noise fraction}), with any boundary noise points re-assigned via k-nearest-neighbour. The whole thing runs on each of the 10 imputation outputs.

Before dimensionality reduction, features are scaled with the median and interquartile range. Robust scaling is appropriate here because neuropsychological data often exhibit floor and ceiling effects [@bellio2020analyzing]. Severely impaired patients may accumulate at the minimum, while intact patients may accumulate near the maximum; both patterns can distort means and standard deviations [@pinsky2023mad]. Median and interquartile-range scaling reduce this influence.

For each of the 20 imputed datasets (10 methods across 2 feature representations), UMAP is applied before HDBSCAN. UMAP is stochastic, so a single embedding can reflect random initialisation as well as data geometry. I therefore run 10 seeds for each hyperparameter set and retain the embedding with the highest silhouette score under an initial HDBSCAN evaluation. This repeated-seed procedure constrains seed-specific variation without changing the downstream clustering logic.



### UMAP Parameter Grid

_Source: `report/Chapters_short/Chapter3.tex`_

Caption: UMAP hyperparameter grid. All combinations of these values were put through their paces, for a total of 9 configurations.

The Euclidean metric was used, and min_dist was set to 0.0 to encourage separation between dense regions in the embedding.



### HDBSCAN Parameter Grid

_Source: `report/Chapters_short/Chapter3.tex`_

Caption: HDBSCAN hyperparameter grid. All listed value combinations were evaluated, giving me 120 configurations for each UMAP embedding.

All 120 HDBSCAN configurations were evaluated for every UMAP configuration, giving 9 times 120 = 1{,}080 candidate solutions per dataset. To select the best configuration, I used a composite quality score that penalises solutions that achieve a high silhouette by assigning too many observations to noise:



### Sweep Procedure

_Source: `report/Chapters_short/Chapter3.tex`_

For each imputed dataset, the procedure was as follows. First, I standardised the features with the robust scaler. Second, I generated ten embeddings for each of the nine UMAP configurations and retained the best embedding as the reference UMAP representation. Third, I applied all 120 HDBSCAN configurations and selected the one with the highest Q score. Finally, I reassigned any observations labelled as noise.

During reassignment, HDBSCAN noise points are allocated to the nearest substantive cluster using k-nearest neighbours (k=10) in UMAP space. Because residual noise is minimal on these features, this step produces 100% coverage, so every assessment receives a cluster label. Reassignment is accepted only if the silhouette score does not fall by more than 10%, preserving the separation of the clusters.



### Worked Example

_Source: `report/Chapters_short/Chapter3.tex`_

Consider a hypothetical patient who completed the orientation and digit span tasks but did not complete the Trail Making Test because of motor impairment or the Rey Auditory Verbal Learning delayed recall because of fatigue. After Tier 1 filtering, the patient remains in the dataset with the eligible variables, and MICE imputes the two missing scores from the observed information.

The 14 variable-level scores are then winsorised, direction-aligned, standardised, and reliability-weighted as described in Section sec:domain_scores, producing six domain composites. The robust scaler is applied to reduce the impact of floor and ceiling effects. The resulting six-dimensional vector is mapped into the cohort's UMAP embedding. HDBSCAN assigns the patient to one of three cognitive-severity tiers: Above-Average, Near-Normal, or Global Impairment. If the patient lies in a low-density boundary region and is labelled as noise, the KNN reassignment step uses the ten closest assessments in the embedding to assign the nearest substantive tier. The final output is a tier label and, under the H2 consensus procedure, a confidence score showing how often the imputation methods agree.


---REWORK

I have reformatted the text to make it easier to read.
**Imputation Methods**_Source:_ report/Chapters\_short/Chapter3.texI developed a comparative framework of ten imputation methods across five categories to extend the taxonomy of Afkanpour et al. (2024). The rationale for each method is provided in Chapter Chapter2, §sec:lit\_imputation. The methods' respective categories, years, trade-offs, and downstream clustering performance are summarised in Table tab:method\_summary. The hyperparameters for the ten methods are shown in Appendix AppendixA, Table tab:imputation\_hyperparams. The two deep learning methods were chosen due to their training schedules requiring further design decisions.noindent DAEPrior to applying any form of missing data handling techniques, a Denoising Autoencoder (DAE) is trained on the entire dataset. The DAE learns to reconstruct the original complete data from noisy versions of those data. Using a missingness-pattern-aware corruption mechanism, the input is first masked according to m_ij, x_ij ~ tilde{x}_ij. Since there will always be some level of uncertainty when modelling real-world data, this ensures that the DAE has been trained with a variety of levels of regularisation. Therefore, in addition to being corrupted uniformly at random (with probability ρ) for half of the training samples, the mask m_i for the remaining half of the training samples is randomly sampled from the empirical co-occurrence distribution of missing-data patterns P_miss. It should be noted that missingness in clinical data often exhibits structure. Some tests are typically absent together because they are part of the same battery, or they require a similar amount of time from the patient. Therefore, by training the DAE on corruption mechanisms that mimic clinical missingness, the DAE will learn inter-variable relationships that relate to the latent cognitive structure.noindent VAELike the previous method, a Variational Autoencoder (VAE) is trained on the entire dataset. However, unlike the DAE, instead of training solely to minimise the loss between the reconstructed and true values of the input data (the ELBO in Eq. eq:vae), the VAE trains to minimise this loss as well as the KL-divergence between the latent distribution (qφ(z|x)) and a prior distribution (typically standard normal) on the latent variables z. The KL-divergence is weighted by β to control the degree to which the latent distribution is constrained towards this prior. Training a VAE without controlling β can result in posterior collapse, i.e., ignoring latent variables and relying primarily on the decoder. Cyclical annealing is employed to reduce this risk. Specifically, β is cycled from its lower bound (β_{min}) up to its upper bound (β_{max}) over a cycle of T epochs, and then reset after each cycle:To compare the performance of the two deep learning models, I used a holdout test across three folds. In each fold, I reserved 10% of the non-missing data in H for testing, trained the models on the remainder of H, and computed RMSE and MAE between the predicted and true values:
Caption: Summary of the ten imputation methods based on Afkanpour’s taxonomy. Clustering results (number of clusters k and silhouette score) are reported based on optimal UMAP+HDBSCAN configuration.
## **Domain Level Feature Construction**
_Source:_ report/Chapters\_short/Chapter3.tex
Cognitive-domain-level features were created by taking aggregated versions of variables associated with each cognitive domain while retaining the 14 individual neuropsychological variables for comparison purposes. Due to differences in scales among the original measures (e.g., standardised scores vs. scaled scores), direct aggregation would be problematic unless scale harmonization occurred.
Therefore, three processing steps were taken prior to aggregation. First, each variable was winsorized to a 1st–99th percentile interval to avoid extreme imputed values caused by outliers or sentinel codes. Next, all timed tests had their signs reversed (i.e., all tests now had positive values indicating better performance). Finally, all variables were standardized to zero mean and unit variance. Reliability-weighted averages of variables representing each domain were used as domain scores. Specifically, each variable j is assigned a weight wj = 1 – rj , where rj represents its missingness rate. Weights are normalized within domain. Variables with greater frequency of administration therefore receive greater weighting in their respective composite scores. Reducing dimensionality from 14 individual variables to six domain-level scores provides fewer variables for distance-based algorithms to operate upon, improving geometry. Additionally, creating domain-level profiles allows clinicians to conceptualize cognitive deficits in terms of cognitive domains—rather than individual variables—making interpretation more clinically relevant. However, detail is lost. For example, two patients might have identical average memory scores yet differ in immediate versus delayed recall. Hypothesis H4 assesses whether the benefits of increased stability and interpretability provide sufficient justification for losing detail.
## **UMAP+HDBSCAN Pipeline**
_Source:_ report/Chapters\_short/Chapter3.tex
Fig.fig:pipeline_diagram shows the end-to-end process from imputed data to final cluster assignment.
Caption: End-to-end clustering pipeline. Following robust scaling of imputed data, the data enter into a hyperparameter grid search of UMAP with 10 random seeds for each of 9 configurations. The best-silhouette UMAP embedding is stored for subsequent analysis. HDBSCAN performs clustering on each of 120 configurations and stores the configuration with the highest composite quality criterion Q = {silhouette} * (1 − {noise fraction}). Any boundary noise points are then re-assigned using k-nearest neighbors (k = 10) in UMAP space.
Prior to performing dimensional reduction using UMAP/HDBSCAN, we apply robust scaling using the median and interquartile range to reduce influence of floor and ceiling effects common in neuropsychological assessment [Bellio & Fuentemilla 2020; Pinsky 2023]. Floor effects occur when severely impaired patients accumulate at minimum values for an assessment tool [Pinsky 2023], whereas ceiling effects occur when patients with no impairments accumulate at maximum values [Pinsky 2023]. Scale-free metrics like median and inter-quartile ranges help mitigate these effects.
For each of the twenty imputed datasets (ten methods × two feature representations), we perform UMAP followed by HDBSCAN. Like other machine learning algorithms that rely heavily on initial conditions (in this case, random initialization), UMAP is stochastic. Therefore, a single embedding could capture variability due to either random initialization or geometric properties of the data. Therefore, we repeat each hyperparameter combination ten times and choose the embedding with highest silhouette score (based on initial HDBSCAN clustering).
### **Hyperparameter Search Space for UMAP**
_Source:_ report/Chapters\_short/Chapter3.tex
Caption: Hyperparameter search space for UMAP. All possible combinations of hyperparameters were searched.
We utilized Euclidean distance as our distance metric and min_dist = 0.0 to encourage separation between dense areas in our embedding.
### **Hyperparameter Search Space for HDBSCAN**
_Source:_ report/Chapters\_short/Chapter3.tex
Caption: Hyperparameter search space for HDBSCAN. All possible combinations of hyperparameters were searched.
Each UMAP embedding produced 120 possible candidate solutions (due to 120 different possible HDBSCAN configurations). To determine which configuration was "best," we employed a composite quality score that punished solutions with high silhouettes by allocating many assignments to noise:
### **Sweep Process**
_Source:_ report/Chapters\_short/Chapter3.tex
The following procedures were employed for each imputed dataset:
First, we preprocessed each dataset using a robust scaler. Second, we conducted a ten-fold cross-validation on each UMAP hyperparameter combination (yielding ten embeddings per combination). From these ten embeddings, we chose the best embedding based on silhouette score. Third, we conducted a 120-fold cross-validation on each HDBSCAN configuration and selected the configuration yielding the best-quality score Q. Fourth, we re-labeled any observations previously labeled as noise.
In doing so, noise points assigned by HDBSCAN are relocated to the nearest substantively clustered group based on k-nearest neighbor (k = 10) similarity in UMAP-space. Given that residual noise is negligible on these features, this process yields 100% coverage and thus assigns labels to every assessment. Re-labeling is only allowed if silhouettes decrease by less than 10%, maintaining separations between clusters.
### **Worked Example**
_Source:_ report/Chapters\_short/Chapter3.tex
Assume a hypothetical patient completes only those neuropsychological assessments related to orientation and digit span but fails to complete those related to Trail Making Test due to physical limitations or failed completion of delayed recall portion of the Rey Auditory Verbal Learning Test due to exhaustion. Upon application of Tier 1 filtering, however, the patient remains in the dataset with eligible variables only. The two missing scores are subsequently filled-in by MICE based on observed information.
The 14 variable-level scores are then subjected to winosurizing; aligned for direction; standardized; and weighted as defined in section sec:domain\_scores to produce six domain-composite scores. The robust scaler is applied to minimize the effect that floor and ceiling effects may have on aggregate measures.
The resulting six-dimensional vector is then mapped into the cohort's UMAP representation space. The patient is then classified into one of three cognitive-severity tiers: Above Average, Near Normal, or Globally Impaired. If a patient falls into a sparse area of low density and was classified as noise, KNN reassignment utilizes neighboring assessments in UMAP-space (k = 10) and assigns them to the most closely located substantively-clustered tier. The final output includes a tier label and confidence score based on how often each imputation method agrees under hypothesis H2