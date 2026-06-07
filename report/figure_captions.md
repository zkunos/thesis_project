# Figure Captions

## fig:pipeline_diagram

End-to-end clustering pipeline. After imputed data are run through a robust scaler, they go into a UMAP hyperparameter grid (10 random seeds for each of 9 configurations) and the embedding with the best silhouette is kept. HDBSCAN then does the clustering in a 120-configuration sweep, scored by the composite quality criterion $Q = \text{silhouette} \times (1 - \text{noise fraction})$, with any boundary noise points re-assigned via $k$-nearest-neighbour. The whole thing runs on each of the 10 imputation outputs.

## fig:missingness_barplot

Proportion of missing values for each cognitive variable, ordered by missingness rate. Specialised assessments show higher missingness than the routinely administered screening measures.

## fig:imputation_comparison

Distribution comparison across ten imputation methods for ATMTA and VPIMATGES. Mean Imputation compresses variance; model-based methods preserve distributional shape.

## fig:imputation_comparison_b

Distribution comparison for MRAVLT015R and MRAVLT015. Deep learning methods (DAE, VAE) closely match model-based methods.

## fig:tsne_umap

Two-dimensional projections using t-SNE (left) and UMAP (right) with HDBSCAN cluster assignments colour-coded. UMAP reveals more clearly separated cluster regions.

## fig:radar_profiles

Left: mean cognitive domain score per tier, expressed as a $z$-score from the cohort mean (dotted ring = cohort average). The three polygons are roughly concentric (every domain moves together), so the tiers differ in overall level rather than in profile *shape*. Right: Gini importance from a random-forest surrogate that recovers the tier labels from the domain scores (accuracy 0.994). As the labels derive from those same scores, this panel re-describes the partition's decision boundaries rather than measuring independent importance, and the ordering is sensitive to inter-domain correlation (Section~\ref{sec:feature_importance}); it should not be read as evidence that attention is clinically unimportant.

## fig:h2_ari_nmi

Pairwise Adjusted Rand Index (top) and Normalised Mutual Information (bottom) across the ten imputation methods. Agreement is high throughout; KNN shows the lowest agreement with the smoother model-based methods.

## fig:h2_consensus

Distribution of consensus confidence scores (proportion of methods agreeing on assignment). Higher values indicate assessments whose assignment is robust across imputation methods.

## fig:h2_dendrogram

Dendrogram of imputation methods using average-linkage clustering on ARI-based distances. KNN forms the most distinct branch, while the smoother model-based methods group tightly together.

## fig:h3_heatmap

Heatmap of cluster membership (columns) by clinical unit (rows). Cell colours indicate observed frequency. Certain severity tiers are concentrated within specific units.

## fig:h4_comparison

Domain-aggregated versus variable-level features on silhouette (0.481 vs 0.473), mean VIF (1.88 vs 2.77), and condition number (11.8 vs 61.7). Domain aggregation produces comparably separated but far less collinear, better-conditioned features.

## fig:feature_importance

Random Forest surrogate trained to recover the tier labels from the domain scores. Left: Gini importance. Right: permutation importance with error bars. Because the labels derive from the same scores, this re-describes the clustering's decision boundaries rather than measuring independent importance; the ranking is also sensitive to the strong inter-domain correlation (see text) and should not be read as evidence that attention is clinically unimportant.

## fig:sensitivity

Sensitivity to the Tier~1 missingness threshold across five values (30--70%). Top row: (a)~number of eligible variables and (b)~number of clusters recovered. Bottom row: (c)~silhouette score and (d)~noise proportion. Dashed line marks the 50% threshold used in the primary analysis.

--REWORK

# Figure Captions

## fig:pipeline_diagram

This is an end-to-end clustering pipeline. Once the data have been imputed, they first pass through a robust scaler. Next, after being scaled, the imputed data will pass into a UMAP hyperparameter grid with (10 random seed for every one of nine configuration) and the resulting embeddings which yield the highest silhouette value are retained. HDBSCAN then does the clustering in a 120-configuration sweep, based upon the composite quality measure \( Q = \text{silhouette} \times (1 - \text{noise fraction}) \) , where all boundary noise points are assigned back to their respective cluster(s) via k-nearest neighbour. This entire process is run over each of the 10 possible imputation outcomes.

## fig:missingness_barplot

Missingness bar plot for all cognitive variables, ordered by missingness rates. Missingness rates were higher among the specialised assessments compared to the routine screening assessments.

## fig:imputation_comparison

Comparison of distributions for each of the 10 different imputation methods for ATMTA and VPIMATGES. Mean imputation reduces variance whereas model-based methods maintain the distributional characteristics of the original data.

## fig:imputation_comparison_b

Comparison of distributions for MRAVLT015R and MRAVLT015. Deep learning models (DAE, VAE) closely approximate model-based methods.

## fig:tsne_umap

Two-dimensional representations of the data using t-SNE (left) and UMAP (right), with HDBSCAN cluster assignments coloured. UMAP reveals clearer separation of cluster areas.

## fig:radar_profiles

Left: Mean score for each cognitive domain in each tier, expressed as a z-score from the cohort mean (the dotted ring indicates the cohort average). Although the three polygons are approximately circular (each domain moves collectively), therefore the tiers differ in terms of global levels rather than shapes. Right: Gini importance from a random forest surrogate that recovers tier labels from domain scores (accuracy = 0.994). Since these labels are derived from those same scores, this panel describes the decision boundaries of the partitions instead of providing independent importance measurements, and the ordering depends on inter-domain correlation (see Section~\ref{sec:feature_importance}). It should not be interpreted as suggesting that attention has no clinical significance.

## fig:h2_ari_nmi

Adjusted Rand Index (ARI) at top and normalised mutual information (NMI) at bottom for pairwise comparisons across the 10 different imputation methods. High agreement was found throughout, although KNN showed lower agreement with the smoother model-based methods.

## fig:h2_consensus

Histogram of consensus confidence values (proportions of methods assigning to the same class). Assessments whose assignment is highly confident across multiple imputation methods have higher consensus confidence values.

## fig:h2_dendrogram

Dendogram of imputation methods using average linkage clustering on ARI-based distance metrics. KNN separates itself from other branches, and tighter grouping occurs among the smoother model-based methods.

## fig:h3_heatmap

Heatmap of cluster assignments (columns) by clinical unit (rows). Cell colors represent frequencies. Specific tiers occur more frequently in certain units.

## fig:h4_comparison

Comparison of aggregated by domains and individual features at the variable level: silhouette (0.481 vs 0.473), mean VIF (1.88 vs 2.77), and condition number (11.8 vs 61.7). Aggregation at the domain level produces similar separations but much less correlated, well-conditioned features.

## fig:feature_importance

Random Forest surrogate trained to recover tier labels from domain scores. Left: Gini importance. Right: Permutation importance with error bars. Since labels are derived from the same scores, this panel describes the decision boundaries of the clustering partitions rather than independently evaluating their relative importance; further, since there is significant inter-domain correlation, see text, rankings should not be taken as implying clinical insignificance of attention.

## fig:sensitivity

Effect of varying Tier~1 missingness threshold across five values (30 -- 70%). Upper row: (a) Number of available variables and (b) Number of clusters identified. Lower row: (c) Silhouette score and (d) Proportion of noise. Vertical dashed lines indicate Tier~1 missingness threshold used in primary analyses.
