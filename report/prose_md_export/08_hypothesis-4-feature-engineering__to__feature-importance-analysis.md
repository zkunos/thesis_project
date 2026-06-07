<!-- Exported prose chunk 8. Word count: 503. -->


## Hypothesis 4: Feature Engineering

_Source: `report/Chapters_short/Chapter4.tex`_

The central prediction was that aggregating features at the domain level would yield more robust clustering than operating on individual variables. I evaluated both representations across three metrics: silhouette scores, the condition number, and the Variance Inflation Factor (VIF).

Domain-level aggregation produced a slightly higher mean silhouette score than the variable-level representation (0.481 vs. 0.473; Figure fig:h4_comparison). The more important change occurred in feature-space conditioning. Mean VIF fell from 2.77 to 1.88, and the condition number fell from 61.7 to 11.8. Because high VIF values indicate multicollinearity, and high condition numbers can distort distance computations used by UMAP and HDBSCAN, this reduction is methodologically consequential. Aggregation reduces redundancy while preserving the latent cognitive constructs represented by the tests [@lezak2012neuropsychological].

Caption: Domain-aggregated versus variable-level features on silhouette (0.481 vs 0.473), mean VIF (1.88 vs 2.77), and condition number (11.8 vs 61.7). Domain aggregation produces comparably separated but far less collinear, better-conditioned features.

Hypothesis 4 is therefore supported. Domain-level feature engineering improves numerical stability without sacrificing cluster separation.



## Feature Importance Analysis

_Source: `report/Chapters_short/Chapter4.tex`_

For this analysis, I trained a Random Forest surrogate on the MICE-imputed domain scores, using the tier labels as the target. It achieved 99.4% accuracy in 5-fold cross-validation. This result describes the separability of the tiers in domain space; it does not independently validate the clustering. Because the tier labels were generated from the same domain scores through UMAP+HDBSCAN, a classifier that recovers them is effectively reconstructing the clustering boundaries. The near-perfect accuracy therefore shows that the ordered severity tiers are highly separable in domain space.

As an interpretability aid, the Gini and permutation rankings placed orientation first (Gini 0.49), followed by visuoperception (0.24) and language (0.17), with attention (0.03) and executive function (0.02) lower in the ranking (Figure fig:feature_importance). This ordering should be interpreted cautiously. It is internal to the clustering procedure and is partly circular. In addition, Gini importance is biased when predictors are correlated [@boulesteix2012overview]. The six domains are strongly positively correlated, consistent with the cognitive positive manifold and with the first principal component described in §sec:cluster_profiles. Once a tree has split on a highly correlated domain such as orientation, attention can appear redundant. Its low importance score should therefore not be interpreted as evidence that attention is clinically unimportant. The concentric profiles and principal-component loadings in Figure fig:radar_profiles, rather than the surrogate importance ranking, determine whether the tiers represent overall severity or a domain-specific dissociation.

Caption: Random Forest surrogate trained to recover the tier labels from the domain scores. Left: Gini importance. Right: permutation importance with error bars. Because the labels derive from the same scores, this re-describes the clustering's decision boundaries rather than measuring independent importance; the ranking is also sensitive to the strong inter-domain correlation (see text) and should not be read as evidence that attention is clinically unimportant.

---REWORK


## hypothesis 4: feature engineering

_source: `report/chapters_short/Chapter4.tex`_

The main hypothesis was that aggregate measures of features based on Domain would produce more stable clusters than separate feature-level data. To test these hypotheses, i compared two different sets of measures for all three features across the three previously mentioned criteria: silhouette scores, condition number, and variance inflation factors (vif).

Aggregate measures produced a marginally greater average silhouette score than did the individual variable-based measure (.481 vs .473; Figure fig:h4_comparison). More importantly, there was significant change in terms of how each set of measures conditioned the feature space. The average vif decreased significantly, from 2.77 to 1.88, and the condition number decreased similarly, from 61.7 to 11.8. High vifs indicate multi-collinearity, which distorts computation of distances needed to perform the UMAP and HDBSCAN algorithms. Therefore, the decrease in vifs indicates that the aggregation process reduced redundancy while maintaining the underlying cognitive constructs measured by the tests [@lezak2012neuropsychological].

Caption: comparison of the performance of aggregate versus separate feature-based measures on silhouette (.481 vs .473), mean vif (1.88 vs 2.77), and condition number (11.8 vs 61.7). Aggregate measures provided similar levels of cluster separation with much less multi-collinearity and distortion of distances due to conditioning.

Therefore, hypothesis 4 is supported and aggregate measures provide improved numerical stability without losing cluster separation.

## feature importance analysis

_source: `report/chapters_short/Chapter4.tex`_

To conduct this analysis, i trained a Random Forest surrogate model on the mice imputed Domain scores and used the tier labels as targets. It obtained an accuracy rate of 99.4 % in 5 fold cross-validation. The accuracy of this surrogate model measures how well the tier labels can be predicted from the Domain scores. However, because the tier labels were created from the same Domain scores used in the clustering algorithm (UMAP + HDBSCAN), the surrogate model is essentially creating its own versions of the clustering boundaries. Therefore, since the surrogate model performs so well (i.e., nearly perfect accuracy), the tier labels demonstrate high degrees of separability in Domain space.

I employed Gini and permutation rankings to help illustrate the relative importance of each Domain. Orientation ranked highest (Gini = .49), followed closely by visuoperceptual (Gini = .24) and language (Gini = .17), with attention (Gini = .03) and executive function (Gini = .02) last among the six domains (Figure fig:feature_importance). Although this order may provide some useful information about the importance of each Domain in terms of their relationships to one another, this ordering should be interpreted cautiously. It represents only what is internal to the clustering methodology and has been influenced partially by circularity. Additionally, Gini importance is biased when predictors are highly correlated [@boulesteix2012overview]. As stated earlier, the six domains are highly positively correlated (both theoretically as part of the cognitive positive manifold and empirically as indicated by the first principal component in §sec:cluster_profiles). Once a tree splits on a highly correlated Domain like orientation, attention appears redundant. Thus, even though attention ranks lowest, it is incorrect to infer that attention is clinically irrelevant. Rather, attention's position is best understood within the context of Figure fig:radar_profiles where the concentric profiles and principal component loadings determine whether the tiers represent total clinical severity or a Domain-specific dissociation.

Caption: a Random Forest surrogate model trained to predict the tier labels from the Domain scores. Left: Gini importance. Right: permutation importance with error bars. Since the tier labels were derived from the same scores that formed the basis of the surrogate models predictions, this simply re-creates the decision boundaries defined by the clustering rather than providing an assessment of the independent contributions made by each Domain. Furthermore, because each of the domains are very highly inter-correlated (as described above), both Gini and permutation ranking will be affected by this relationship and should not be taken as evidence that attention is clinically insignificant.