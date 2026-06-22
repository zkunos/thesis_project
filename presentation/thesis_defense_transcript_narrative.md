# Thesis Defense Transcript — Narrative Edition

**Data-Driven Cognitive Phenotyping in Acquired Brain Injury**
Zoltan Kunos · MSc Fundamental Principles of Data Science · Universitat de Barcelona
Supervisor: Dr. Alejandro García-Rudolph
**Target duration:** ~20 minutes (main deck, slides 1–21). Appendix A–G are backup.

---

## Narrative spine (say it to yourself before you start)

1. **Clinical heterogeneity creates the question.**
2. **Structured missingness creates the methodological problem.**
3. **The pipeline tests the structure.**
4. **The results identify three tiers.**
5. **PCA and profile evidence show those tiers discretize a continuum.**
6. **Clinical association gives them practical relevance.**

Every slide should hand off to the next beat. If you ever lose your place, return to the spine.

---

## Slide 1 — Title  *(~40 s)*

Good morning, and thank you for being here. The title of my dissertation is *Data-Driven Cognitive Phenotyping in Acquired Brain Injury*.

The question behind it is simple to state. After a brain injury, two patients can carry the same diagnosis and still need very different rehabilitation. So I asked: do routinely collected neuropsychological data contain a consistent cognitive structure — and if they do, is it a set of distinct subtypes, or something else?

The answer I'll defend is that the structure is real, but it is **not** a catalogue of subtypes. It is a **cognitive severity gradient**, which clustering divides into three usable tiers. The rest of the talk is how I got there, and why I trust it.

---

## Slide 2 — Roadmap  *(~30 s)*

Here is the path. I'll start with the clinical problem, because the clinical problem is what creates the research question. Then the cohort and the missingness, because the missingness is what creates the methodological problem. Then the pipeline and the four pre-registered tests. Then the results, their interpretation, and their practical utility — and I'll close with limitations and conclusions. There's an appendix of backup slides if you want to go deeper in questions.

---

## Slide 3 — Clinical Problem  *(~70 s)*

**[Beat 1: clinical heterogeneity creates the question.]**

Start with the clinic. Acquired brain injury can disrupt attention, memory, language, executive function, orientation, and visuospatial cognition — and it does not do so in the same way in any two patients. That is the core fact: cognitive impairment after ABI is **heterogeneous**.

Clinicians manage that heterogeneity with broad categories — diagnosis, injury severity. Those categories are useful, but they describe the scope of the problem, not the individual cognitive profile or its degree. Two patients who both "have memory problems" can need completely different programmes.

So the question writes itself: *can a data-driven method recover a cognitive organisation that is actually meaningful — one that captures more than the diagnostic label?* And there's a catch built into the data, which is the next slide: these assessments are very often incomplete, and they're most incomplete exactly where the impairment is greatest. So the full question is — can we recover that organisation, and can we trust it when missing data are handled honestly rather than ignored?

---

## Slide 4 — Research Gap  *(~55 s)*

Before the method, where does this sit relative to prior work? Earlier cognitive-phenotyping studies tend to share a set of limitations. Samples are often small — frequently under two hundred participants. They usually rely on complete-case analysis, dropping anyone with a gap. They rarely stress-test the algorithm. They often fix the number of clusters in advance. And they seldom validate against anything clinical.

This dissertation pushes on each of those. It works at scale — over seventeen thousand assessments. It compares ten imputation strategies instead of deleting incomplete rows. It runs hyperparameter, seed, and missingness sensitivity checks. It uses density-based clustering that does **not** fix the number of clusters in advance. And it validates the result against clinical-unit assignment. Those five moves are the contribution.

---

## Slide 5 — Pre-Registered Hypotheses  *(~60 s)*

To keep myself honest, I pre-registered four hypotheses, each with an objective threshold — so the examiners are not taking my word for anything.

**H1**: are stable clusters even recoverable? Silhouette above 0.40, under thirty percent noise, at least two clusters.
**H2**: are the assignments robust to which imputation I choose? Mean pairwise adjusted Rand index above 0.50, under a fixed-reference design.
**H3**: are the tiers clinically relevant? A chi-square association with clinical unit, Cramér's V above 0.10, holding up after adjusting for diagnosis.
**H4**: does aggregating variables into cognitive domains actually help? Better separation and better numerical conditioning.

I won't dwell on the formulas. The point is that every claim I make today has a number it had to clear, set before I saw the result.

---

## Slide 6 — Cohort and Missingness  *(~70 s)*

**[Beat 2: structured missingness creates the methodological problem.]**

Now the data. After filtering and removing assessments with no cognitive testing at all, I have **17,406 assessments from 7,285 patients**, across **14 neuropsychological variables** that map onto **6 cognitive domains**. That's a large, real, routine clinical database — which is exactly why it's messy.

Here is the number that drove the whole methodology: only **53.1 percent** of rows are complete across all fourteen variables. So a complete-case analysis would throw away nearly **47 percent** of the data.

And this is the key move of the talk — that missingness is **not random**. The bar chart shows it's concentrated in the long, demanding tests, and it tracks the testing process. So I can't just delete it. If I do, I don't get a cleaner version of the same cohort; I get a different cohort. That's the methodological problem, and the next slide says why it matters clinically.

---

## Slide 7 — Why Imputation Is Necessary  *(~60 s)*

**[Beat 2, continued.]**

Why is the missingness structured? Because a missing value here usually means something clinical. It can mean fatigue or low motivation. It can mean cognitive overload or task aversion. It can mean disorientation or a motor limitation. It can mean the patient simply couldn't tolerate a long battery. Or it can mean the clinician judged a different test more appropriate.

Notice what all of those have in common: they correlate with **impairment**. So when you drop incomplete rows, you don't remove a random sample — you preferentially remove the most impaired patients, the very people rehabilitation is built around. That's why missingness has to be **managed and tested**, not hidden. The heatmap makes the structure visible. The methodological response is imputation, plus a way to check whether the imputation choice changes the answer — which is what the pipeline is for.

---

## Slide 8 — Analysis Pipeline  *(~80 s)*

**[Beat 3: the pipeline tests the structure.]**

Here is the pipeline. I impute with **ten strategies**, ranging from simple mean and median, through model- and donor-based methods, matrix completion, and deep learning. I then standardise and orient the scores so that higher always means better. I aggregate the fourteen variables into the six cognitive domains. I embed with **UMAP**, and I cluster with **HDBSCAN**, with sensitivity analyses around the whole thing.

The part I want you to hold onto is the **fixed-reference design** at the bottom, because it's how H2 is tested. I take one solution — from MICE — and I freeze it: the scaler, the UMAP embedding, and the HDBSCAN partition all become a fixed reference. Then I push every other imputation's values **through** that frozen structure. That asks a precise question: do the imputed values land in the same place under a fixed structure? It deliberately does **not** ask whether re-fitting the entire pipeline from scratch reproduces the hierarchy — that's a stronger claim, and I'm careful not to make it.

---

## Slide 9 — Why UMAP and HDBSCAN  *(~55 s)*

Two design choices worth defending. **UMAP**, because it represents nonlinear neighbourhood structure, balances local and global geometry, and gives HDBSCAN a clean low-dimensional space to work in. **HDBSCAN**, because — and this matters given my whole argument — it does **not** require me to fix the number of clusters in advance. It finds dense regions that persist across density levels, and it can label uncertain points as noise instead of forcing them into a group.

And the honest caveat, which I keep on the slide: separation measured in UMAP space can look better than it really is. So I never lean on it alone — it has to be backed by the sensitivity analyses and by the structural evidence I'll show in a moment.

---

## Slide 10 — H1: Three Severity Tiers  *(~60 s)*

**[Beat 4: the results identify three tiers.]**

Here is the first result. The pipeline recovers **three tiers**. I've labelled them **Above-Average** — 6,725 assessments scoring above the cohort mean; **Near-Normal** — 6,328 sitting close to the average; and **Global Impairment** — 4,353 below the mean across domains.

All ten imputation methods cleared the pre-registered H1 thresholds. In the MICE reference, the full-coverage silhouette was about **0.53**, with three tiers recovered.

So the numerical criteria are met — stable clusters exist. But notice the labels already tell a story: Above-Average, Near-Normal, Global Impairment. Those aren't three different *kinds* of cognition. They're three *levels*. I'm flagging that deliberately, because the next two slides are where I argue that these tiers are bands cut from a continuum, not natural kinds.

---

## Slide 11 — Continuum Evidence  *(~60 s)*

**[Beat 5: PCA and profile evidence show the tiers discretize a continuum.]**

This is the conceptual heart of the thesis. If these were genuine subtypes, the tiers would have different *shapes* — strong here, weak there, different patterns of strength and weakness. They don't.

Look at the radar profiles on the left: they're roughly **concentric**. The tiers differ in overall size, not in shape — every domain moves in the same direction together. And the PCA on the right confirms it quantitatively: the first principal component alone explains nearly **56 percent** of the variance, and **every domain loads positively** on it. That is the signature of a single dominant axis — overall cognitive severity.

So the dominant signal in this dataset is **global severity**, not a symptom-specific dissociation. The three tiers are bands along that one axis. They discretize a continuum; they are not a catalogue of phenotypes.

---

## Slide 12 — H2: Robustness to Imputation  *(~70 s)*

**[Beat 3, paid off: the structure survives the methodological problem.]**

Now back to the missingness, because a structure is only worth interpreting if it isn't an artefact of one preprocessing choice. This is H2.

Across the imputation methods, the mean pairwise adjusted Rand index is **0.71**, with a bootstrap 95 percent confidence interval of 0.70 to 0.72 — substantial agreement. Of the **45** method-pair comparisons, **44** survived Holm correction; the single exception was KNN versus SoftImpute, just under threshold. And at the level of individual assessments, more than **86 percent** received high-confidence consensus labels.

So the tiers are not a quirk of how I filled in the gaps. I'll state the scope precisely: this shows point assignments are robust under a **fixed** scaler, embedding, and partition. It does not claim that independently re-fit pipelines reproduce identical density hierarchies. Within that scope, the structure holds.

---

## Slide 13 — Complete-Case Analysis Changes the Answer  *(~60 s)*

**[Beat 2 and Beat 3 collide — the punchline of the methodological argument.]**

And here is why the imputation wasn't optional. Suppose I'd done what most studies do and just used complete cases. I keep 53.1 percent of the data — and I get a **different result**.

The complete-case baseline recovers **two** clusters, not three. Its silhouette drops to about **0.26**, roughly half of the 0.53 from the MICE reference. And even on the assessments the two analyses share, the agreement between them is only about **0.63** — far from identical.

So deleting incomplete cases is not a weaker version of the same analysis. It **changes the partition**. That's the methodological thesis in one slide: how you handle missing data isn't preprocessing hygiene — it's part of the model's substantive output.

---

## Slide 14 — H3: Clinical Relevance  *(~65 s)*

**[Beat 6: clinical association gives the tiers practical relevance.]**

A structure can be robust and still be clinically useless. So H3 asks whether the tiers connect to anything in the real clinical world — specifically, to which **clinical unit** a patient is assigned.

They do. The chi-square statistic is **911**, with a p-value below ten-to-the-minus-156, and a Cramér's V of **0.16** — above my pre-registered threshold of 0.10. More importantly, I checked whether this is just diagnosis in disguise: a Cochran–Mantel–Haenszel test shows the association **survives adjustment for diagnosis**. So the severity tier carries information **beyond** the diagnostic label.

Let me be careful about the claim. I am not saying tier should determine placement. I'm saying tier is informative about routing — it adds something, on top of diagnosis, to a conversation about rehabilitation intensity.

---

## Slide 15 — H4: Domain Aggregation  *(~55 s)*

The last hypothesis is methodological housekeeping with real consequences. H4 asks whether aggregating the fourteen variables into six domains was the right call, versus clustering raw variables.

It was — on two fronts. Separation is marginally better: silhouette 0.48 versus 0.47. But the bigger win is numerical stability: mean variance inflation factor drops from about **2.80 to 1.90**, and the condition number from about **62 to 12**. That matters because UMAP and HDBSCAN are distance-based, and distance-based methods are fragile when features are redundant and highly correlated. Aggregating into clinically meaningful domains removes that redundancy while keeping interpretable constructs. So domains win on stability and on interpretability.

---

## Slide 16 — Interpretation  *(~70 s)*

**[Beat 5, stated as a thesis.]**

Let me pull the interpretation together, because the distinction is the whole point. A **subtype** account says patients differ qualitatively — different cognitive profiles, different kinds. A **gradient** account says patients differ mostly along one shared axis of severity, and the tiers are practical bands cut from that axis.

Everything points to the gradient. The radar profiles are concentric. The first component explains over half the variance. All domains load positively. The tiers behave like ordered bands, not distinct kinds.

I'm not claiming domain-specific dissociations never exist after brain injury — they can. I'm claiming that in this dataset, with an imputation-robust, domain-level pipeline, **overall severity dominates**. And there's a warning embedded here: poor scaling, redundant or non-cognitive features, or complete-case selection can all manufacture patterns that *look* like subtypes but aren't. A lot of apparent phenotyping may be that.

---

## Slide 17 — Clinical and Analytic Utility  *(~55 s)*

So what is this good for? Two audiences.

For **clinical users**, the tiers offer a shared vocabulary for discussing rehabilitation intensity, a confidence score for the borderline cases, and a piece of information that sits alongside diagnosis and clinical judgement — not above it.

For **analytic users**, the contribution is the pipeline itself: reproducible, missingness-aware, with the imputation decisions made explicit and testable, and adaptable to studying how cognition links to outcomes.

And the long-term point is cultural. Rather than hiding missingness or quietly deleting incomplete cases, you make the missing-data decision visible and you measure its influence. That's the habit I'd like this work to encourage.

---

## Slide 18 — CogDash  *(~45 s)*

To make all of this usable rather than just publishable, I built **CogDash** — a Streamlit application that turns the analysis into an interactive tool. It has a cluster explorer, a patient lookup, a new-patient classifier, and summaries of the hypothesis tests.

The design principle is **auditability**. A clinician can see what data feed the model and can see when the model's confidence is low. That's deliberate: CogDash is built to support a conversation between clinicians and analysts, not to automate a clinical decision.

---

## Slide 19 — Limitations  *(~70 s)*

I want to be the first to state the limits.

First, the data are **single-site**, so external replication is needed before anyone treats this structure as general. Second, this is **not** a full longitudinal recovery model — repeated assessments hint at trajectories, but modelling recovery directly needs a longitudinal design. Third, the imputation rests on a **missing-at-random** working assumption; I can't rule out MNAR from observed values alone, though my extreme-MNAR checks suggest the Global Impairment tier is robust while the finer boundaries are more fragile. Fourth, I had **no functional outcomes** — return-to-work, length-of-stay, independence — which would be the strongest external validators. Fifth, some of the validation is **embedding-based**, and UMAP-space silhouette can flatter separation. And sixth, the pipeline itself, through aggregation and density clustering, may bias toward finding a general severity axis. I think the convergent evidence holds — but those are the honest caveats.

---

## Slide 20 — Conclusions  *(~60 s)*

Three conclusions, mapping to the three things this thesis contributes.

**Empirically**: routine post-ABI neuropsychological data carry a strong cognitive-**severity gradient** — three ordered tiers, not discrete phenotypes.

**Methodologically**: **imputation is a modelling decision**, not preprocessing. Treat missing data as trivial and you can change the answer, as the complete-case comparison showed.

**Practically**: **domain-level severity tiers** are interpretable and numerically stable, and they're preferable to raw-variable clustering for identifying distinctive patient groups.

Taken together, this dissertation doesn't prove, and doesn't need to prove, that discrete cognitive phenotypes exist. It supports something more conservative and, I think, more useful: an imputation-robust, severity-stratification framework that can be interpreted clinically and tested analytically.

---

## Slide 21 — Thank You  *(~30 s)*

Thank you for your attention. I'm glad to take questions — on the codebase and the dashboard, on the technical choices behind the imputation and clustering, or on what this might mean for rehabilitation-planning research. And if it's useful, I have backup slides on the imputation set, the fixed-reference design, HDBSCAN, the silhouette caveats, the MNAR analysis, and the clinical boundary.

*Optional closing line if the room is quiet:* My hope is simply that this found something genuinely useful — best understood, conservatively, as a cognitive-severity continuum after acquired brain injury rather than as a set of discrete subtypes.

---

## Appendix A–G — Backup (not spoken unless asked)

- **A — Ten imputation strategies:** "The ten span simple, model-based, donor-based, matrix-completion, and deep methods. Agreement across that range is what makes the result credible."
- **B — H2 fixed-reference design:** "Freeze the MICE scaler, embedding, and partition; push every other imputation through it; compare with ARI. Tests robustness of assignments, not invariance of independently discovered structure."
- **C — HDBSCAN logic:** "Core distance, mutual reachability, MST, hierarchy of dense components, stability-based selection, noise labelling. Unlike DBSCAN it doesn't reduce to a single fixed-ε solution."
- **D — Silhouette caveats:** "UMAP emphasises neighbourhood structure, so embedded silhouette can overstate separation. Read it as an internal quality metric, not proof of natural categories."
- **E — MNAR sensitivity:** "MAR is the working assumption; under extreme-MNAR stress tests, Global Impairment is robust and the finer boundaries are more sensitive."
- **F — Clinical interpretation boundary:** "Tier supplements diagnosis and supports discussion; it does not diagnose, prescribe, place, or replace judgement."
- **G — Future work:** "External replication, longitudinal recovery modelling, validation against functional outcomes, alternative model-based phenotyping, prospective CogDash evaluation, and sensitivity to domain-specific dissociations."

---

### Timing summary

| Section | Slides | Time |
|---|---|---|
| Frame the question (Beat 1) | 1–4 | ~3.5 min |
| Pre-registration | 5 | ~1 min |
| Missingness problem (Beat 2) | 6–7 | ~2 min |
| Pipeline / structure test (Beat 3) | 8–9 | ~2.5 min |
| Three tiers (Beat 4) | 10 | ~1 min |
| Continuum evidence (Beat 5) | 11 | ~1 min |
| Robustness + complete-case (Beat 3 payoff) | 12–13 | ~2 min |
| Clinical relevance (Beat 6) | 14 | ~1 min |
| H4 + interpretation | 15–16 | ~2 min |
| Utility, CogDash | 17–18 | ~1.5 min |
| Limitations, conclusions, close | 19–21 | ~2.5 min |
| **Total (main deck)** | **1–21** | **~20 min** |
