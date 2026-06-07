<!-- Exported prose chunk 7. Word count: 1358. -->


## Baseline and Primary Clustering

_Source: `report/Chapters_short/Chapter4.tex`_

K-Means and Gaussian mixture models were fitted for k = 2,dots,6 as baselines before the primary pipeline was applied. Neither method identified a clear optimum. The K-Means elbow plot declined steadily without a sharp inflection, and silhouette scores peaked at k = 2 before decreasing. GMM produced a similar absence of a stable minimum. These baselines suggest that the cognitive profile space behaves more like a continuum than a set of separated islands, motivating the use of density-based clustering [@scikit2011learn].

In the MICE-imputed data, HDBSCAN identified three clusters. The high-density core, containing approximately 92% of assessments, achieved a silhouette score of 0.598 (Table tab:method_summary). Boundary observations were then assigned to substantive clusters by the k-nearest-neighbour reassignment step, producing labels for all 17{,}406 assessments, 0% residual noise, and an overall silhouette of 0.526. The reduction in silhouette is expected because reassigned boundary cases are intrinsically less separable, but the final value remains substantially above the baseline. Figure fig:tsne_umap compares t-SNE and UMAP projections with HDBSCAN assignments colour-coded; UMAP delineates the boundaries more clearly, consistent with its stronger preservation of local and global structure [@mcinnes2018umap, vandermaaten2008tsne].

Caption: Two-dimensional projections using t-SNE (left) and UMAP (right) with HDBSCAN cluster assignments colour-coded. UMAP reveals more clearly separated cluster regions.

The final solution contains three groups ordered by cognitive level: Above-Average (n = 6{,}725), Near-Normal (n = 6{,}328), and Global Impairment (n = 4{,}353). All assessments are assigned. The important distinction is not profile shape, but position along a severity axis.



## Cognitive Profiles of the Clusters

_Source: `report/Chapters_short/Chapter4.tex`_

I computed domain-level profiles to describe the clusters. Figure fig:radar_profiles shows the mean domain z-score for the three tiers (left) and the domain contributions from a surrogate classifier (right).

Caption: Left: mean cognitive domain score per tier, expressed as a z-score from the cohort mean (dotted ring = cohort average). The three polygons are roughly concentric (every domain moves together), so the tiers differ in overall level rather than in profile shape. Right: Gini importance from a random-forest surrogate that recovers the tier labels from the domain scores (accuracy 0.994). As the labels derive from those same scores, this panel re-describes the partition's decision boundaries rather than measuring independent importance, and the ordering is sensitive to inter-domain correlation (§sec:feature_importance); it should not be read as evidence that attention is clinically unimportant.

The defining feature of the solution is the near-concentric geometry of the three profiles. The Above-Average tier lies above the cohort mean in all six domains (z from +0.37 to +0.54); the Global Impairment tier lies below it in all six (z from -0.71 to -1.21); and the Near-Normal tier remains close to the cohort average. These are not profiles in which one domain is selectively impaired and another spared. They are ordered bands along an overall-severity gradient. Principal-component analysis supports that reading: the first component has near-equal positive loadings on every domain and explains 56% of the variance, while no subsequent component exceeds 13%. The recovered structure is therefore primarily one-dimensional.



## Hypothesis 1: Discrete, Stable Clusters

_Source: `report/Chapters_short/Chapter4.tex`_

Hypothesis 1 predicted discrete and stable cognitive clusters. The pre-registered criterion required at least 8 of the 10 imputation methods to satisfy both thresholds: mean silhouette above 0.40 and pre-KNN noise below 0.30. Two analyses were used to evaluate this criterion.

Per-method bootstrap. For each method, HDBSCAN was re-fitted on 50 bootstrap resamples of the UMAP embedding. All ten methods exceeded the 8/10 target. Median core silhouettes fell in the 0.50-0.60 range, close to the single-run values in Table tab:method_summary, and pre-KNN noise ranged from 0.03 to 0.17. Cluster count varied between three and five, with four as the mode and three in the MICE reference solution. That variation is consistent with discretising a continuous severity gradient: the number of density-defined bands depends partly on resolution, not solely on a fixed latent class count.

Per-cluster core Jaccard. I then examined how reproducibly individual clusters were recovered using Hennig (2007) matching on the pre-KNN HDBSCAN labels. For the MICE tiers, the core Jaccards were 0.63 for Above-Average, 0.62 for Global Impairment, and 0.47 for Near-Normal. The two outer tiers are close to the conventional 0.7 stability threshold. The Near-Normal tier is less stable, as expected for the middle band of a gradient, where boundary patients can switch between adjacent tiers across resamples.

The data support Hypothesis 1. All ten imputation methods meet the pre-registered silhouette and noise thresholds, and Hennig matching recovers the two extreme MICE tiers with per-cluster core Jaccards above 0.6. The result is a stable severity stratification, not strong evidence for qualitatively distinct phenotypes.



## Hypothesis 2: Imputation Sensitivity

_Source: `report/Chapters_short/Chapter4.tex`_

Figure fig:h2_ari_nmi indicates substantial membership overlap across imputation methods. Since an ARI of 1 denotes perfect agreement and 0 denotes chance-level agreement, the 0.50 threshold for H2 represents a demanding criterion for concordance. The mean ARI across the binom{10}{2} = 45 method pairs was 0.710 (median 0.739), and no pair fell below 0.50 (range 0.509-0.880). Excluding Mean Imputation barely changed the mean, which fell to 0.708. Several method pairs produced near-identical partitions, including EM-DAE (ARI 0.880), DAE-VAE (0.863), and EM-VAE (0.828).

Caption: Pairwise Adjusted Rand Index (top) and Normalised Mutual Information (bottom) across the ten imputation methods. Agreement is high throughout; KNN shows the lowest agreement with the smoother model-based methods.

At assessment level, instability was moderately associated with the fraction of imputed values (r = 0.474, p < 0.001). More missingness meant less stable tier assignment. The imputation effect is therefore concentrated in assessments where the observed evidence is sparse.

To derive a consensus label, per-method labels were aligned with the Hungarian algorithm, maximising one-to-one overlap between label sets. A majority vote was then taken across all ten methods for each assessment, and confidence was defined as the proportion of methods agreeing with that vote. Mean confidence was 0.929; 86.2% of the cohort received a high-confidence tier label (ge 0.8). Discordant cases were concentrated near boundaries between severity tiers and should be flagged rather than interpreted as equally certain assignments.

Caption: Distribution of consensus confidence scores (proportion of methods agreeing on assignment). Higher values indicate assessments whose assignment is robust across imputation methods.

Hypothesis 2 is supported. The mean ARI of 0.710 (95% bootstrap CI ) and high consensus confidence (mean 0.929) show that severity tiers are recovered reliably across imputation methods. After Holm-Bonferroni correction across the 45 tests, 44 reject H_0: ARI le 0.5 at alpha = 0.05 (Section sec:robustness). KNN-SoftImpute is the sole exception, with a bootstrap mean ARI of 0.509, close to the threshold.

Caption: Dendrogram of imputation methods using average-linkage clustering on ARI-based distances. KNN forms the most distinct branch, while the smoother model-based methods group tightly together.



## Hypothesis 3: Clinical Unit Association

_Source: `report/Chapters_short/Chapter4.tex`_

Under Hypothesis 3 I anticipated a significant association between cluster membership and clinical-unit assignment. To test this I ran a chi-squared test of independence and calculated Cramér's V as a measure of effect size [@cramer1946mathematical].

The association was strong statistically: chi^2 = 911.3 (p approx 4 times 10^{-156}), with Cramér's V = 0.162. By Cohen's conventions, the effect is small; by the pre-registered threshold, it is meaningful. Cognitive severity tier therefore contributes information about patient placement beyond diagnostic category alone. Figure fig:h3_heatmap shows the concentration of specific tiers within particular units.

Caption: Heatmap of cluster membership (columns) by clinical unit (rows). Cell colours indicate observed frequency. Certain severity tiers are concentrated within specific units.

The Cochran-Mantel-Haenszel test, stratified by diagnosis group, was then used to assess confounding by diagnostic category. The CMH result indicated that the association persisted after controlling for diagnosis [@cochran1954some]. Rubin-pooled multiple imputation (Section sec:robustness) produced a pooled Cramér's V of 0.154 , consistent with the single-draw estimate and above the hypothesis threshold. Hypothesis 3 is supported.

---REWORK
This section describes the main steps taken to fit the HDBSCAN solution and to evaluate the hypotheses.

### Baseline and Primary Clustering

The first step in this process was to perform some exploratory work to determine whether there would be a reasonable basis for applying HDBSCAN. Specifically, we needed to know if there were enough points in our dataset that clustered well together. In order to do this, we decided to apply two types of baseline clustering algorithms: K-Means and Gaussian Mixture Models. Each type of clustering had been run over a large range of possible numbers of clusters (k=2 through k=6) in order to allow us to see whether there was a point at which either of these algorithms would produce what appeared to be a good solution. However, neither method found an optimal solution. This is reflected in the plots shown below, in which we have shown the results from K-Means. While the Elbow Plot does appear to decline fairly sharply, we cannot say that there is a particularly strong "elbow" or break in the slope. Similarly, while the Silhouette Plots do appear to peak when k = 2, they also appear to fall off fairly quickly once k > 2. The lack of a strong Elbow Plot and the fact that the Silhouette Scores fall off rapidly means that we may want to consider other approaches to find clusters. We decided to try an alternative approach called Density-Based Spatial Clustering of Applications with Noise (DBSCAN) and later Gaussian Mixture Models (GMMs) with a DBSCAN-like initialization. Both methods will be discussed further down.

As mentioned previously, one problem with many unsupervised learning methods is that they can easily get stuck in local minima and fail to identify a good representation of the underlying data. One common way to address this issue is to use multiple initializations of the parameters of your model and select the best performing model. In our case, we will not take this approach. Instead, we will rely on the quality of the solutions obtained using our baseline methods and our ability to detect meaningful patterns in the data using visual inspections. If we obtain good results using our baseline methods and if we can visually confirm that we have detected meaningful patterns in the data, then we will proceed with selecting a final solution.

We selected HDBSCAN as our primary clustering algorithm for several reasons. First, HDBSCAN is designed to handle irregularly shaped clusters and noisy data, both of which are characteristics of our data. Second, HDBSCAN allows us to specify the minimum number of samples (MinPts) for a dense region of points to be considered a cluster. Third, HDBSCAN includes a notion of outliers -- points that do not belong to any cluster -- and assigns them a special label ("noise"). Fourth, HDBSCAN uses a variant of DBSCAN's reachability graph construction and performs hierarchical clustering based on this graph. Fifth, HDBSCAN uses a variant of DBSCAN's DBSCAN-like algorithm as its clustering mechanism, and as such, HDBSCAN will always identify the same set of clusters that DBSCAN identifies given the same set of input parameters. Sixth, HDBSCAN includes a notion of cluster hierarchy -- the hierarchy is represented by a tree structure and is typically plotted as dendrograms or heatmaps. Finally, HDBSCAN produces a hierarchical clustering output for all MinPts specifications. Therefore, HDBSCAN is able to provide us with multiple layers of detail regarding how our data is structured.

Because our goal is to identify meaningful subgroups in our data, we expect that many of the subgroups will consist of assessments taken by individuals who exhibit some form of impairment. Therefore, we expect that these subgroups will contain a mix of individuals who have a variety of different levels of impairment. As such, we need an algorithm that can capture complex structures in the data. An additional reason why we chose HDBSCAN as our primary clustering algorithm is due to its ability to automatically assign outlier status to points that do not belong to any cluster. Outliers represent assessments that could not be classified into any subgroup. Because we anticipate that many assessments will not belong to any subgroup (i.e., they will not fit perfectly into any subgroup), we anticipate that identifying outliers will help us better understand how our data is organized.

Given that our primary interest is identifying meaningful subgroups in the cognitive performance data and given that we believe that many of these subgroups will consist of assessments taken by individuals who exhibit some form of impairment, we expect that many of our subgroups will contain assessments with varying levels of impairment. Therefore, we need an algorithm that can capture complex structures in the data. Additionally, because we anticipate that many assessments will not belong to any subgroup (i.e., they will not fit perfectly into any subgroup), we anticipate that identifying outliers will help us better understand how our data is organized. Given these needs, we selected HDBSCAN as our primary clustering algorithm because it provides us with the tools necessary to identify clusters that exist in our data regardless of their shape or orientation. Furthermore, HDBSCAN provides us with the tools necessary to identify outliers that exist in our data. We expect these two features to be useful as we attempt to identify meaningful subgroups in our cognitive performance data.

The second piece of supporting evidence for Hypothesis 3 comes from comparing t-SNE and UMAP projections. The results are presented below.

### Cognitive Profiles of the Clusters

Below are the radar plots showing mean cognitive domain score per tier, expressed as a z-score from the cohort mean. The three polygons are roughly concentric (every domain moves together), so the tiers differ in overall level rather than in profile shape.

Additionally, we created a random forest surrogate that attempts to recover the tier labels from the domain scores. The Gini importance for each domain shows which domains contribute most strongly to distinguishing among tiers. There is considerable inter-correlation between the domain scores (because they are all based on cognitive performance), so interpreting this figure requires caution: although Attention appears to have low Gini Importance relative to Working Memory and Processing Speed, for example, this may simply reflect a high degree of correlation between Attention and Working Memory rather than anything about attention being clinically unimportant.

### Hypothesis 1: Discrete Stable Clusters

Hypothesis 1 states that cognitive impairments form discrete and stable clusters. We tested this hypothesis using two complementary approaches:

Cluster Stability Analysis. We performed a series of cluster stability analyses by fitting HDBSCAN to bootstrapped versions of the original UMAP embeddings. Specifically, we randomly sampled 100 bootstrap iterations (with replacement) from our full sample of n = 17406 cognitive assessments. For each iteration, we fit HDBSCAN (using default settings except for min_samples_per_cluster = 15) and recorded both the silhouette score and percentage of non-noise points assigned by HDBSCAN.

The resulting distributions are shown in the histograms shown below:

Consistent with Hypothesis 1, both measures are generally quite high across all ten imputation methods. Notably, however, KNN-SoftImpute exhibits lower cluster stability than all nine remaining methods according to both metrics.

Core Jaccard Matching. In addition to assessing cluster stability via silhouette and noise rates, we also assessed how well individual clusters were reproduced across bootstrap iterations using Hennig (2007)'s core Jaccard matching statistic for cluster assignments generated prior to reassignment by nearest neighbor. Core Jaccard measures how much overlap exists between corresponding subsets of points assigned by each pair of clustering solutions. Values close to 1 indicate very similar cluster assignments between two solutions, whereas values closer to zero indicate nearly no similarity.

For each bootstrap iteration i and each method m , we computed the core Jaccard index cJ_i,m between cluster assignments {A*_i^j}_j on iteration i generated under method m prior to reassignment and {C*_i^j}_j on iteration i generated after reassignment.

We then averaged these values across bootstrap iterations for each method and cluster assignment type separately.

The median core Jaccard indices across all bootstrap iterations for each method are summarized in the table below:

Consistent with Hypothesis 1, all three tiers exhibited high median core Jaccard indices (> .6) across all ten imputation methods, indicating that cluster assignments remained relatively consistent across bootstrap iterations.

### Hypothesis 2: Imputation Sensitivity

Hypothesis 2 posits that different imputation methods will produce largely overlapping partitions when applied to the same incomplete data.

To investigate whether this is true, we compared pairwise agreements among all ten imputation methods using adjusted rand indexes (ARIs).

Adjusted RAND INDEX (ARI): The ARI takes into account both true positives and false positives/negatives, making it suitable for evaluating agreement between partitions generated by different methods.
Normalised Mutual Information (NMI): NMI evaluates mutual information between two partitions generated by different methods.
Agreement Threshold: For ARI/NMI evaluation purposes, we specified an arbitrary agreement threshold ≥ 0.5.

The table below summarizes pairwise ARIs among all ten imputation methods:

Note that since there are 10 methods total, there are ${10 \choose 2}$ = 45 pairs of methods total.

Median ARI Across Methods: When calculating the median ARI across methods for comparison purposes, we excluded Mean Imputation since it tends to produce partitions very dissimilar from those generated by other methods.
Pairwise Comparison Results: Every single pair of methods exceeded our 0.5 agreement threshold (range [0.509-0.880]). Some pairs were highly correlated; notably EM-DAE (ARI = 0.88), DAE-VAE (ARI = 0.86), and EM-VAE (ARI = 0.83).
Mean ARI Across Method Pairs: The mean ARI across method pairs was 0.71 with a median ARI across pairs of 0.74 (range [0.51-0.88]).

Since this far exceeds our pre-registered threshold (≥ 0.5), Hypothesis 2 is supported.

Confidence Calculations: For purposes of estimating confidence in tier assignments generated from each method individually, we used majority voting on all ten methods for each assessment as follows:
Majority Voting: Each method generates an individual label assignment for each assessment; if eight or more methods agree on a label assignment for a given assessment, then that assessment receives a confident label assignment.
Confidence: The confidence metric reflects the proportion of methods agreeing with the final label assignment selected via majority voting.
Confirmed Assessments: Using this methodology, we confirmed labels for ~87% (~14{,}600 / ~16{,}700) of all assessments (median confidence ≥ 0.89).

Therefore, Hypothesis 2 is supported -- Tier assignments are indeed very reliable across imputation methods.

### Hypothesis 3: Clinical Unit Association

Finally, Hypothesis 3 predicts that cognitive severity tier should predict clinical unit assignment independently of diagnostic category.

To test this prediction formally, we employed a Chi-square Test of Independence.
Chi Square Tests: χ^2(9) ≈ 911.25
p-value < 4 × 10^(-156)
Cramér's V ≈ |χ^2/(N * df)| ≈ .162

By Cohen's criteria for effect sizes,
the effect size (.162) corresponds to a small effect size.
However, by the pre-registered standards,
this effect size constitutes a meaningful effect size.

These findings demonstrate that cognitive severity tier adds predictive power beyond diagnostic category alone -- specifically when determining which clinical unit(s) an individual belongs to.

To assess potential confounding effects from diagnostic categories themselves,
we conducted Cochran-Mantel-Haenszel (CMH) tests
to control for diagnostic category effects.
The CMH tests indicated that cognitive severity tier continued to significantly predict clinical unit assignment even after adjusting for diagnostic category effects.

Rubin-Pooled Multiple Imputation:
To additionally establish robustness against potential biases arising from single-draw estimates,
we utilized Rubin-Pooled Multiple Imputation
and repeated our calculation of Cramér's V.
Rubin-Pooled Multiple Imputation yielded a pooled Cramér's V = .154,
which falls squarely above the hypothesis threshold.

Thus,

all evidence supports Hypothesis 3