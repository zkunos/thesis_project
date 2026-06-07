<!-- Exported prose chunk 4. Word count: 1363. -->


### UMAP

_Source: `report/Chapters_short/Chapter2.tex`_

At its core, UMAP is a manifold-learning technique that projects high-dimensional data into a low-dimensional space while preserving the global topological structure of the original graph [@mcinnes2018umap]. Unlike linear techniques such as PCA, it captures non-linear relationships, and it is engineered to balance both local and global structure. The critical hyperparameters are n_neighbors (small for local detail, larger for a broader view), min_dist (which determines packing density within the embedding), and n_components.

In technical terms, UMAP starts with a weighted neighbour graph. For an edge from x_i to a neighbour x_j, the directed membership strength is: with rho_i as the distance to the nearest neighbour and sigma_i set so that sum_{j}p_{jmid i}=log_2 k (where k is the n_neighbors setting). These weights are then made symmetric: p_{ij}=p_{jmid i}+p_{imid j}-p_{jmid i},p_{imid j}. Over in the embedding, the equivalent is and the best {y_i} are found by minimising the cross-entropy between the two: with a and b coming from the min_dist setting.

I chose UMAP because it offers advantages over common alternatives. t-SNE is useful for visualisation, but it is computationally expensive and often weak at preserving global structure [@vandermaaten2008tsne]. PCA is efficient and interpretable, but it captures only linear projections and can miss non-linear cluster geometry. Because the next step is density-based clustering, the quality of the embedding is central: HDBSCAN identifies dense regions of the space rather than fitting centroids as k-means does.



### HDBSCAN

_Source: `report/Chapters_short/Chapter2.tex`_

HDBSCAN extends DBSCAN by constructing a hierarchy of clusterings across density levels and selecting stable structures from that hierarchy [@campello2013density]. It is useful for clinical data because the number of clusters does not need to be specified in advance, low-density observations can be labelled as noise, and clusters of different sizes and compactness can coexist. The key parameters are min_cluster_size, which sets the minimum cluster size; min_samples, which controls density estimation; and cluster_selection_epsilon, which influences cluster merging.

To be precise, HDBSCAN re-weights the distances based on local density. A point x has a core distance to its k-th nearest neighbour (k=min_samples), operatorname{core}_k(x)=d!left(x,N_k(x)right). From there the mutual reachability is defined: A minimum spanning tree based on these distances produces the hierarchy, from which the most stable clusters are selected: where lambda_{mathrm{birth}}(C) is the density level at which cluster C appears and lambda_{max}(x,C) is the level at which point x leaves it. Observations that do not belong to a stable cluster are labelled as noise.

The UMAP and HDBSCAN combination is widely used in computational biology and related fields, especially when high-dimensional data contain complex cluster structures.



## Cluster Validation

_Source: `report/Chapters_short/Chapter2.tex`_

When there is no ground truth, cluster quality can only be assessed indirectly. No single metric is sufficient, so this thesis combines internal validation, external agreement measures, and stability checks.



### Internal Validation

_Source: `report/Chapters_short/Chapter2.tex`_

For internal validation, the silhouette coefficient [@rousseeuw1987silhouettes] is the primary method. It compares the cohesion of each observation (its proximity to its assigned cluster) against its separation from the nearest neighbouring cluster, yielding a score from -1 to +1: positive values indicate a strong match, values near zero suggest boundary placement, and negative values imply misclassification. In formal terms, if a(i) is the mean distance of observation i to the rest of its cluster and b(i) the mean distance to the points of the next closest cluster, then These are averaged across all n observations to give bar{s}=frac{1}{n}sum_{i=1}^{n}s(i), the summary score for the solution. Mean silhouette bar{s} is the principal internal metric here; noise proportion serves as a secondary check on how much of the cohort is placed in substantive clusters.



### External Validation

_Source: `report/Chapters_short/Chapter2.tex`_

Comparing two cluster solutions, for example to measure agreement between imputation methods, requires external metrics. The adjusted Rand index (ARI) counts pairs of observations that are assigned consistently across two clusterings and corrects this count for chance [@hubert1985comparing]. Suppose there are two clusterings of n points, U={U_i} and V={V_j}, with contingency counts n_{ij}=|U_icap V_j| and marginals a_i=sum_j n_{ij}, b_j=sum_i n_{ij}. The ARI is defined as With +1 denoting perfect agreement and 0 what would be expected by chance, anything below zero is systematic disagreement [@robert2020comparing]. Then there is normalised mutual information (NMI), an information-theoretic way of measuring how much one clustering reveals about the other, normalised by entropy. Using mutual information I(U;V) and Shannon entropies H(cdot), where 1 is full agreement and 0 means they share nothing.

For a more detailed view of individual clusters, I use the Jaccard index. If A and B are the point sets for a cluster under two solutions, the index is the size of their intersection divided by the size of their union: Values range from 0 to 1, with higher values indicating more similar membership. I also use Hennig matching [@hennig2007cluster] as a bootstrap-stability method. Across R resamples, each original cluster C_k is paired with the resampled cluster that has the highest Jaccard overlap. The stability score is the mean of those maxima: By convention a per-cluster hat{S}_k in excess of 0.7 is stable.

Together, NMI and ARI indicate whether two cluster solutions are substantively similar. High agreement between imputation methods supports the interpretation that the recovered structure reflects the data rather than an artefact of the imputation procedure.



## Data Description

_Source: `report/Chapters_short/Chapter3.tex`_

This study draws on a clinical neuropsychological database maintained by a neurorehabilitation service. The raw extraction contains 22,075 records from 8,739 distinct patients, including longitudinal follow-up assessments. Each assessment comprises 31 variables spanning demographic and administrative information, injury characteristics, and neuropsychological measures across six cognitive domains: orientation, attention, visuoperception, language, memory, and executive function. After the Tier-1 filtering described in Section sec:filtering, the analysed dataset contains 17{,}406 assessments from 7{,}285 patients.

The data were generated in routine clinical care, not under a fixed research protocol. Test selection was determined by the neuropsychologist, the referral question, and the patient's capacity to engage with the battery. Missingness is therefore structured. Some measures are present in nearly every assessment; others appear only in particular clinical contexts. Unlike research-protocol missingness, which is often controlled by design, missingness in this dataset ranges from below 5% for screening measures to above 90% for specialised tests.

The measures also occupy different scales, including standardised z-scores, scaled scores, and raw timed variables. These scales were harmonised during domain aggregation (Section sec:domain_scores). Table tab:missing_descriptive reports the missingness pattern for the 14 eligible variables. Only 53.1% of the 17,406 records (9,245 assessments) are complete across all 14 variables; listwise deletion would remove 46.9% of the sample and risk substantial selection bias. The imputation strategy in Section sec:imputation is designed to avoid that loss of clinical information. All data were anonymised according to institutional governance standards.



## Tier 1 Filtering

_Source: `report/Chapters_short/Chapter3.tex`_

Because several variables contain substantial missingness, filtering was applied before imputation and clustering. The main analysis uses a 50% threshold. Variables missing in more than half of the observations are removed, and observations with more than 50% missingness across retained variables are also excluded.

The threshold balances coverage against reliability. A 70% threshold would preserve more records and variables, but at the cost of heavier imputation and greater risk of artefactual structure. A 30% threshold would yield a cleaner matrix but would discard clinically informative assessments and reduce statistical power. The 50% rule retains a broad cross-section of cognitive domains while constraining the burden placed on imputation. Sensitivity analyses across thresholds from 30% to 70% are reported in Section sec:robustness.

After applying this cut-off and removing assessments with no cognitive test on file, the final dataset contains 14 neuropsychological variables and 17,406 assessments from 7,285 patients.

Caption: Eligible neuropsychological variables after Tier 1 filtering, organised by cognitive domain.


---REWORK

### UMAP

Source: `report/Chapters_short/Chapter2.tex`

UMAP is a manifold learning algorithm that maps high dimensional data onto lower dimensions in order to maintain the overall topology of the data. This is a nonlinear approach to dimensionality reduction. Instead of using a linear approach like PCA, which will capture straight line patterns, UMAP attempts to find the underlying geometric structure of your data. The tradeoff of finding the right balance between maintaining the local and global structure of the data is addressed through tuning the hyperparameters. There are three major hyperparameters in UMAP:

* **min_dist** - The minimum distance between samples in the new space. 
* Larger values allow for a less dense representation.
* Smaller values result in a denser representation.
* **n_neighbors** - The number of neighbors to consider when creating the connections between data points in the original space. 
* Larger numbers provide a better understanding of the global structure.
* Smaller numbers focus more on the local structure.
* **n_components** - The desired dimension of the output.

Technically speaking, UMAP begins with a weighted neighbor graph. An edge exists from \( x_i \) to a neighboring node \( x_j \), and the directed membership strength is given by: with \( \rho_i \) being the distance to the nearest neighbor, and \( \sigma_i \) set so that sum_{j}p_{jmid i}=log_2 k (where k is the n\_neighbors setting). The weights are then symmetrized: p_{ij}=p_{jmid i}+p_{imid j}-p_{jmid i},p_{imid j}. When moving to the embedding side, we have and we want to minimize the cross-entropy between the two: with and b coming from the min\_dist setting.

### HDBSCAN

Source: `report/Chapters_short/Chapter2.tex`

HDBSCAN builds upon traditional DBSCAN, extending it by building hierarchical representations of clusterings at multiple densities, and identifying persistent structures. Traditional DBSCAN is limited in that you cannot identify overlapping or nested clusters without having a preconceived notion of how many groups exist. HDBSCAN solves these issues by automatically determining the number of clusters and providing a clear definition of noise. The key parameters include:

* **min\_samples**: Controls the density estimation
* **min\_cluster\_size**: Sets the minimum size of the identified clusters
* **cluster\_selection\_epsilon**: Determines how aggressively clusters are merged

Here’s a technical explanation: HDBSCAN adjusts distances based on local density. Given a point x, let be the k-th nearest neighbor (k=min\_samples), and be the core distance to . The mutual reachability is then defined: A minimum spanning tree (MST) is built on these distances to generate the hierarchy. We then select the most stable clusters: where lambda_{mathrm{birth}}(C) is the density at which cluster C first forms, and lambda_{max}(x,C) is the maximum level at which point x belongs to cluster C. Points not belonging to any persistent cluster are classified as noise.

The pairing of UMAP and HDBSCAN is commonly employed in computational biology and related disciplines due to their ability to identify complex structures in high-dimensional datasets.

## Cluster Validity Assessment

_Source:_ `report/Chapters_short/Chapter2.tex`

When a gold standard is absent, assessing the validity of discovered clusters is indirect. Henceforth, we employ a combination of internal validations, external consistency measurements and sensitivity analyses.

### Internal Validations

_Source:_ `report/Chapters_short/Chapter2.tex`

Internal validation involves comparing various attributes of different possible cluster solutions. Here we primarily rely on silhouette coefficients [rousseeuw1987silhouettes], which compare within-cluster cohesion (the average similarity of each data-point to the other data-points in its own cluster) and between-cluster separation (the average similarity between each data-point and data-points outside its cluster). The silhouette value for an individual item lies in the interval [-1,+1]: Positive values denote good fit, values close to zero signify poor fit (as either an item fits poorly into its own group or fits very well into adjacent group(s)), and negative values represent incorrect assignment. The formula for calculating an individual item's silhouette value is: with , where d_i denotes the mean intra-cluster dissimilarity (average distance from i to all members of its cluster), c_i denotes the mean inter-cluster dissimilarity (mean distance between i and all members of its second-nearest cluster), and s_(i) = (b_i-a_i)/max(a_i,b_i); and S_(avg) denotes the mean silhouette value of all items. As previously stated, we utilize the mean silhouette as our principal internal evaluation measure. Noise percentage is our second measure of evaluating how much of our total population is clustered in meaningful ways.

### External Validations

_Source:_ `report/Chapters_short/Chapter2.tex`

Measuring two different cluster solutions, e.g., when examining how consistent cluster assignments are between two different imputation methods, necessitates the employment of external validation measures. One common method is the Adjusted Rand Index (ARI) [hubert1985comparing]. The ARI examines how many pairs of cases have been assigned to identical clusters across two separate clusterings and then adjusts this count for chance. Let U = {U_i} and V = {V_j} be two clusterings of n objects with contingency counts n_ij = |U_i ∩ V_j|, marginal sums ai = ∑_j n_ij and bj = ∑_i n_ij. The ARI is calculated as With +1 representing perfect agreement and 0 representing random agreement, values < 0 demonstrate systematic disagreement [robert2020comparing]. Next, we calculate Normalized Mutual Information (NMI): a mutual-information-theoretic method of quantifying how much one clustering discloses regarding another clustering normalized by entropy. Specifically, using mutual information I(U;V) and Shannon entropies H(.) [shannon1948mathematical], we define full agreement as 1 and no agreement as 0.

For an additional insight into individual clusters' similarities/differences, we apply the Jaccard index. If A and B denote sets containing points that make up a specific cluster under two respective solutions, the Jaccard index is computed as the ratio of A ∩ B / A ∪ B; thus values lie in [0, 1], with larger values demonstrating closer membership. Finally, we use Hennig Matching [hennig2007cluster] as a bootstrapping method of assessing cluster stability. Across R bootstrap iterations, we pair each original cluster C_k with the resampled cluster whose Jaccard overlap with it is maximal. The stability score of each original cluster C_k is then taken as the mean of these maxima: By convention, a per-cluster score > 0.7 is considered stable.

Collectively, NMI and ARI evaluate whether two cluster solutions exhibit significant substantive agreement.

## Description of Dataset

_Source:_ `report/Chapters_short/Chapter3.tex`

Data originates from a clinical neuropsychology database managed by a rehabilitation center. Raw data includes 22,075 records from 8,739 unique individuals with repeated follow-up assessments. Each assessment consists of 31 features relating to demographics/administrative details/injury specifics/neuropsychological results across six cognitive domains: Orientation/Attention/Visuospatial Perception/Language/Memory/Executive Function. Following Tier-1 filtering (described in section sec:filtering), our analyzed dataset contains 17{,}406 assessments from 7{,}285 subjects.

Given that these data originate from routine clinical practice rather than a specifically constructed research protocol, test selection was influenced by both the neuropsychologist conducting testing/referral questions/patient engagement capabilities. Therefore, missingness in our dataset is structured. Certain measures appear in almost every assessment; however, some are only available in response to certain clinical circumstances. Unlike missingness originating from research protocols that may control missingness through design; missingness in this dataset varies greatly; ranging from approximately 5% for screening tools to over 90% for specialty assessments.

Additionally, measures fall along varying scales (standardized z-scores/scaled scores/raw timed measures). During domain aggregation (section sec:domain_scores), these scales were unified. In table tab:missing_descriptive, we display missingness distribution for our fourteen candidate variables. Only fifty-three percent (9,245 assessments) of our seventeen thousand four hundred-six records contained complete data across all fourteen variables; if we applied listwise deletion, nearly forty-seven percent (approximately nine thousand seven hundred twenty-nine assessments) of our sample could potentially be lost as a consequence of our inability to analyze this portion of our dataset. Our imputation strategy (section sec:imputation) is intended to avoid losing clinical information associated with this portion of our sample.

All data have undergone deidentification according to established standards for protecting patient privacy.

## Tier 1 Filtering

_Source:_ `report/Chapters_short/Chapter3.tex`

Since many variables in our dataset exhibit large amounts of missingness, we performed filtering prior to performing imputation/clustering. In general, our primary analysis employs a fifty-percent filter. Any variable that exhibits more than fifty percent missingness is eliminated; any record exhibiting more than fifty percent missingness among remaining variables is eliminated.

Our choice represents a compromise between maximizing data retention versus minimizing the amount of missingness placed on imputation models. While employing a seventy-percent filter would retain significantly more records/variables; this would increase the likelihood that artificial structure exists in our imputed data. Conversely, employing a thirty-percent filter would likely produce a clean matrix; however, it would eliminate substantially more clinically relevant records while reducing analytical capability.

We perform sensitivity analyses utilizing filters between thirty percent and seventy percent in section sec:robustness.

Following application of this filter and elimination of assessments without documented cognitive testing, our dataset contains thirteen neuropsychological variables; seventeen thousand four hundred-six assessments from seven thousand two-hundred-eighty-five patients.

Caption: Neuropsychological variables included post-filtering by cognitive domain