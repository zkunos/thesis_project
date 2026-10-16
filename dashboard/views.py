"""Views of saved assessment-level and patient-level findings."""
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from dashboard.data import (DOMAINS, COLORS, METHODS, REPRESENTATIONS, RESULTS,
                            table, saved, metadata, names, group_colors, legacy_profiles,
                            cohort_z, hypothesis_rows, research_summary,
                            profile_model, assign_profile)


def heading(title, description, scope="ASSESSMENT-LEVEL ANALYSIS"):
    st.markdown(f'<div class="eyebrow">{scope}</div>', unsafe_allow_html=True)
    st.title(title)
    st.markdown(f'<p class="lead">{description}</p>', unsafe_allow_html=True)


def metrics(items):
    for column, (label, value) in zip(st.columns(len(items)), items):
        column.metric(label, value)


def chart(fig, height=350, key=None):
    fig.update_layout(template="plotly_white", height=height,
                      font=dict(family="Arial", size=12, color="#182b49"),
                      margin=dict(l=15, r=15, t=35, b=30),
                      colorway=COLORS, legend_title_text="")
    st.plotly_chart(fig, width="stretch", config={"displaylogo": False}, key=key)


def grid(frame, height=None):
    # Semantic HTML keeps local tables portable without Arrow's native runtime.
    def number(value):
        return f"{value:.3g}" if value != 0 and abs(value) < .001 else f"{value:,.3f}"
    markup = frame.to_html(index=False, escape=True, border=0, classes="cog-table", float_format=number)
    st.markdown(f'<div style="max-height:{height or 360}px;overflow:auto">{markup}</div>', unsafe_allow_html=True)


def method_select():
    methods = saved("shared_infrastructure")["METHODS"]
    return st.selectbox("Imputation method", methods, index=methods.index("MICE"))


def profile_lines(frame, value, group, title=None, color_map=None):
    return px.line(frame, x="domain", y=value, color=group, markers=True,
                   category_orders={"domain": DOMAINS}, color_discrete_sequence=COLORS,
                   color_discrete_map=color_map,
                   labels={"domain": "", value: "Domain composite", group: ""}, title=title)


def home():
    heading("Cognitive groups, with context", "Explore reproducible score groupings and the choices that change their membership.", "COGDASH / FINDINGS")
    summary = research_summary()
    metrics([("Index patients", f"{summary['discovery'] + summary['validation']:,}"),
             ("Discovery / validation", f"{summary['discovery']:,} / {summary['validation']:,}"),
             ("Two-group repeatability", f"ARI {summary['ari2']:.3f}"),
             ("Agreement across scaling", f"ARI {summary['scaling_ari']:.3f}")])
    st.info("Reproducible partitions were found. Their membership depends on scaling and missing-data assumptions; distinct clinical phenotypes remain unconfirmed.")
    left, right = st.columns([1, 1.15])
    with left:
        st.subheader("Assessment-level severity bands")
        counts = table("Cluster_Names.csv").rename(columns={"clinical_name": "Band", "n_patients": "Assessments"})
        band_colors = {r.Band: group_colors()[names()[r.cluster_id]] for r in counts.itertuples()}
        chart(px.bar(counts, x="Assessments", y="Band", orientation="h", text="Assessments",
                     color="Band", color_discrete_map=band_colors).update_layout(showlegend=False), 270)
        st.caption("17,406 assessments · 7,285 patients · 14 tests · 6 domains. Names describe the historical MICE partition.")
    with right:
        st.subheader("What the patient-level analysis adds")
        st.markdown("**Independent refitting.** Twenty stochastic imputations give three-group agreement of ARI 0.935.\n\n"
                    "**Representation sensitivity.** Equal-domain scaling changes membership substantially.\n\n"
                    "**Longitudinal comparison.** The minimum-size rule retains one trajectory class among 2,013 patients.")
        st.markdown("[Explore patient-level evidence →](./research)")
    with st.expander("Hypothesis interpretation"):
        grid(pd.DataFrame(hypothesis_rows(), columns=["Hypothesis", "Conclusion", "Interpretation"]))


def research():
    heading("Patient-level research", "One index assessment per patient. Preprocessing and selection use discovery data; validation uses the fitted rules.", "PATIENT-LEVEL ANALYSIS / 15 OCTOBER 2026")
    summary = research_summary()
    metrics([("Discovery patients", f"{summary['discovery']:,}"), ("Validation patients", f"{summary['validation']:,}"),
             ("Imputation draws", "20"), ("Patient subsamples", "50")])
    stability, models, scaling, trajectories = st.tabs(["Repeatability", "Model comparison", "Scaling sensitivity", "Trajectories"])
    with stability:
        st.subheader("Repeatable within a specified representation")
        data = table("refit_agreement.csv", True)
        draws = data[data.source == "imputation_draw"].copy()
        draws["Method"] = draws.method.map(METHODS)
        draws["Groups"] = draws.k.astype(str)
        fig = px.bar(draws, x="Groups", y="mean_ari", color="Method", barmode="group",
                     error_y=draws.ari_p95 - draws.mean_ari, error_y_minus=draws.mean_ari - draws.ari_p05,
                     color_discrete_sequence=COLORS, labels={"mean_ari": "Mean pairwise validation ARI"})
        fig.update_yaxes(range=[0, 1.02])
        chart(fig, 300)
        st.caption("Bars show mean agreement across independently refitted imputations. Whiskers are descriptive 5th–95th percentiles of dependent partition pairs, not confidence intervals.")
        st.info("Two groups were selected in all 20 k-means screens over 2–8 groups. This search does not test a one-population alternative.")
        with st.expander("Methods and additional stability results"):
            st.write("Earliest eligible assessment; fixed 80/20 patient split, seed 20261015. Discovery-fitted clipping, direction alignment, test standardization, bounded Bayesian imputation, domain aggregation and robust scaling.")
            grid(data.rename(columns={"mean_ari": "Mean ARI", "n_repeats": "Repeats"}))
    with models:
        st.subheader("Evaluate separation in measured feature space")
        rep = st.selectbox("Representation", list(REPRESENTATIONS), format_func=REPRESENTATIONS.get)
        selected_only = st.checkbox("Show discovery-selected models only", True)
        data = table("model_comparison.csv", True)
        subset = data[data.representation == rep].copy()
        if selected_only:
            subset = subset[subset.selected_by_training]
        subset["Method"] = subset.method.map(METHODS)
        grid(subset[["Method", "train_k_observed", "train_silhouette", "validation_silhouette", "validation_coverage"]].rename(
            columns={"train_k_observed": "Groups", "train_silhouette": "Discovery silhouette", "validation_silhouette": "Validation silhouette", "validation_coverage": "Validation coverage"}))
        st.caption("Discovery selection: silhouette for partition/density methods; BIC for Gaussian mixtures. Scores across different representations are not a shared performance scale. Noise is excluded from silhouette.")
        st.subheader("Observed-data mixtures: fit improves, count remains open")
        mixture = table("robust_selected_models.csv", True).copy()
        mixture["Family"] = mixture.family.map({"normal": "Gaussian", "contaminated": "Contaminated Gaussian", "t4": "Student t (df=4)", "t10": "Student t (df=10)"})
        grid(mixture[["Family", "selected_k", "bic", "validation_loglik", "validation_silhouette"]].rename(columns={"selected_k": "Components", "bic": "BIC", "validation_loglik": "Validation log likelihood", "validation_silhouette": "Domain silhouette"}))
        st.info("Both t families select eight components at the upper search limit. Components may approximate score ceilings, skewness or tails; eight clinical phenotypes are not established.")
    with scaling:
        st.subheader("The same scores, different group assignments")
        geometry = table("common_geometry_comparison.csv", True).iloc[0]
        metrics([("Robust vs equal-domain groups", f"ARI {geometry.ari_robust_vs_equal:.3f}"),
                 ("Robust-space PC1 variance", f"{metadata()['pc_explained_variance'][0]:.1%}"),
                 ("Equal-domain PC1 variance", f"{geometry.equal_domain_pc1_variance:.1%}")])
        profiles_data = pd.concat([table("scaling_profiles.csv", True),
                                  pd.read_csv(RESULTS / "dashboard/robust_profiles.csv")], ignore_index=True)
        profiles_data["Group"] = profiles_data.apply(lambda row: f"Group {row.cluster + 1} (n={row.n})", axis=1)
        for col, (model, title) in zip(st.columns(2), [("domains:kmeans:3", "Robust scaling"), ("equal_domain:kmeans:3", "Equal-domain scaling")]):
            with col:
                part = profiles_data[profiles_data.model == model]
                fig = profile_lines(part, "mean", "Group", title)
                fig.update_yaxes(range=[-3.6, 1.1])
                fig.update_layout(legend=dict(orientation="h", y=-.3))
                chart(fig, 340)
        st.caption("Both panels show the same direction-aligned domain composites on a common vertical scale. Group numbers are local to each solution; matching numbers do not identify the same patients.")
        with st.expander("Domain weighting and missingness"):
            grid(table("scaling_audit.csv", True))
            grid(table("cluster_missingness_association.csv", True))
            st.write("Missingness is associated with group membership. These associations do not establish causation, but repeatability under one imputation model does not remove administration effects.")
    with trajectories:
        st.subheader("Continuous variation remains an adequate selected model")
        trajectories_data = table("trajectory_model_comparison.csv", True).copy()
        metrics([("Eligible patients", f"{summary['trajectory_n']:,}"), ("Discovery / validation", "1,590 / 423"),
                 ("Selected classes", str(summary["trajectory_k"])), ("Minimum expected class", "5%")])
        trajectories_data["Smallest class (%)"] = trajectories_data.minimum_train_class_fraction * 100
        fig = px.bar(trajectories_data, x="k", y="Smallest class (%)", text="Smallest class (%)", color_discrete_sequence=COLORS)
        fig.update_traces(texttemplate="%{y:.1f}%")
        fig.add_hline(y=5, line_dash="dash")
        fig.update_xaxes(title="Requested trajectory classes", dtick=1)
        chart(fig, 270)
        grid(trajectories_data[["k", "bic", "validation_loglik", "Smallest class (%)"]].rename(columns={"k": "Classes", "bic": "BIC", "validation_loglik": "Validation log likelihood"}))
        st.caption("At least three sufficiently measured visits over 0.25–5 years. Linear random-intercept/slope mixtures; every multi-class fit falls below the minimum-size rule. Small subgroups and nonlinear change remain unresolved.")


def explorer():
    heading("Cluster explorer", "Inspect assessment-level embeddings across imputations. Visual separation depends on the projection.")
    method = method_select()
    infra = saved("shared_infrastructure")
    labels = np.asarray(infra["cluster_labels"][method])
    ids = np.linspace(0, len(labels)-1, min(5000, len(labels)), dtype=int)
    label_names = names(method)
    color = [label_names.get(int(v), "Noise") for v in labels[ids]]
    color_options = dict(color_discrete_map=group_colors(method),
                         category_orders={"color": list(label_names.values()) + ["Noise"]})
    metrics([("Assessments", f"{len(labels):,}"), ("Groups", str(len(np.unique(labels[labels >= 0])))),
             ("Noise", f"{np.mean(labels < 0):.1%}"), ("Points displayed", f"{len(ids):,}")])
    left, right = st.columns(2)
    with left:
        embedding = infra["tsne_2d"][ids]
        fig = px.scatter(x=embedding[:, 0], y=embedding[:, 1], color=color, opacity=.65,
                         labels={"x": "t-SNE 1", "y": "t-SNE 2"}, title="Fixed MICE t-SNE coordinates", **color_options)
        fig.update_layout(legend=dict(orientation="h", y=-.2))
        chart(fig, 350)
    with right:
        embedding = infra["umap_embeddings"][method][ids]
        fig = px.scatter_3d(x=embedding[:, 0], y=embedding[:, 1], z=embedding[:, 2], color=color, opacity=.55,
                            title=f"{method} UMAP coordinates", labels={"x": "UMAP 1", "y": "UMAP 2", "z": "UMAP 3"}, **color_options)
        fig.update_traces(marker_size=2)
        fig.update_layout(legend=dict(orientation="h", y=-.2))
        chart(fig, 350)
    st.caption("Each point is an assessment; repeated observations from a patient remain separate. The fixed t-SNE coordinates are recolored by the selected partition. UMAP coordinates change with the method. A deterministic 5,000-row display sample keeps interaction responsive.")


def profiles():
    heading("Cognitive profiles", "Compare group means relative to the assessment cohort. The original named groups describe broad severity bands.")
    method = method_select()
    frame = legacy_profiles(method)
    labels = saved("shared_infrastructure")["cluster_labels"][method]
    label_names = names(method)
    selected = st.multiselect("Groups", list(label_names), default=list(label_names), format_func=label_names.get)
    if not selected:
        st.info("Select at least one group to compare.")
        return
    standardized = cohort_z(frame)
    all_means = standardized.assign(group=labels).groupby("group").mean()
    color_limit = float(np.abs(all_means.to_numpy()).max())
    means = all_means.loc[selected]
    long = means.rename_axis("Group").reset_index().melt(id_vars="Group", var_name="domain", value_name="z")
    long["Group"] = long.Group.map(label_names)
    left, right = st.columns([1, 1.15])
    with left:
        fig = profile_lines(long, "z", "Group", "Cluster means in cohort z-score units",
                            color_map=group_colors(method)).update_yaxes(title="Cohort z-score")
        fig.update_layout(legend=dict(orientation="h", y=-.4, font_size=10))
        fig.update_xaxes(tickangle=-30)
        chart(fig, 350)
    with right:
        fig = px.imshow(means.rename(index=label_names), text_auto=".2f", color_continuous_scale="RdBu_r",
                        zmin=-color_limit, zmax=color_limit, aspect="auto", title="Domain heatmap")
        fig.update_xaxes(tickvals=DOMAINS, ticktext=["Orient.", "Attn.", "Visuo.", "Lang.", "Memory", "Exec."], tickangle=-30)
        fig.update_yaxes(title="", ticktext=[label_names[k].replace("Global Impairment", "Global<br>Impairment").replace("Above-Average", "Above-<br>Average").replace("Near-Normal", "Near-<br>Normal") for k in selected],
                         tickvals=[label_names[k] for k in selected])
        fig.update_traces(textfont_size=10)
        fig.update_layout(coloraxis_colorbar=dict(thickness=12, title="z"))
        chart(fig, 350)
    grid(means.rename(index=label_names).reset_index().rename(columns={"group": "Group"}).round(3))
    st.caption("Z-scores reference this cohort, not external normative values. Names and colors are local to each model; they are not transferable clinical categories.")


def lookup():
    heading("Patient lookup", "Review one assessment profile. A row is an assessment, so several rows may belong to the same patient.")
    demo = st.checkbox("Use an illustrative synthetic profile", value=True)
    frame = legacy_profiles("MICE")
    z = cohort_z(frame)
    if demo:
        profile = pd.Series([-.4, -.2, .2, -.1, -.8, -.5], index=DOMAINS)
        st.info("Illustrative synthetic profile · no patient record is displayed.")
        label = "Illustrative example"
    else:
        row = st.number_input("Assessment row", min_value=0, max_value=len(frame)-1, value=0, step=1)
        profile = z.iloc[row]
        cluster = int(saved("shared_infrastructure")["cluster_labels"]["MICE"][row])
        label = names().get(cluster, "Noise")
        st.write(f"**Assessment row {row:,} · {label}**")
    left, right = st.columns([1, 1.25])
    with left:
        grid(pd.DataFrame({"Domain": profile.index, "Cohort z-score": profile.values}).round(3))
    with right:
        fig = px.bar(x=profile.values, y=profile.index, orientation="h", labels={"x": "Cohort z-score", "y": ""}, color_discrete_sequence=COLORS)
        fig.add_vline(x=0, line_color="#999999")
        chart(fig, 340)
    st.caption("Displayed scores are standardized domain composites. They are not raw test units or diagnostic scores. The synthetic example is used in the manual.")


def imputation():
    heading("Imputation comparison", "Compare assignment agreement when a common MICE-fitted transformation and partition are applied across imputations.")
    h2 = saved("h2_results")
    metrics([("Mean pairwise ARI", f"{h2['mean_ari']:.3f}"), ("Median ARI", f"{h2['median_ari']:.3f}"),
             ("Consensus agreement", f"{h2['consensus_confidence']:.3f}"), ("At least 80% agreement", f"{h2['high_confidence_pct']:.1f}%")])
    for col, (file, title) in zip(st.columns(2), [("ARI_Matrix.csv", "Adjusted Rand index"), ("NMI_Matrix.csv", "Normalized mutual information")]):
        with col:
            matrix = table(file, index_col=0)
            chart(px.imshow(matrix, zmin=0, zmax=1, text_auto=".2f", color_continuous_scale="Blues", title=title), 400)
    st.caption("These matrices assess a fixed assignment rule. They do not test whether independently refitted density models discover the same groups. Patient-Level Research reports independent refitting.")
    with st.expander("Method metrics and domain divergence"):
        grid(table("Clustering_Metrics_Summary.csv"))
        grid(pd.DataFrame(h2["domain_divergence"].items(), columns=["Domain", "Divergence"]))


def clinical():
    heading("Clinical units", "Describe the association between the assessment-level bands and service organization.")
    h3 = saved("h3_results")
    grouped = table("H3_Grouped_Multinomial_Summary.csv").iloc[0]
    metrics([("Chi-square", f"{h3['chi2']:.1f}"), ("Cramér’s V", f"{h3['cramers_v']:.3f}"),
             ("Patient-grouped log-loss gain", f"{grouped.log_loss_improvement:.4f}"),
             ("Gain interval includes zero", "Yes")])
    st.info("The association is small. Adding tier to diagnosis does not clearly improve patient-grouped predictive log loss.")
    view = st.radio("Cross-tabulation", ["Clinical unit", "Diagnosis group"], horizontal=True)
    filename = "clinical_units.csv" if view == "Clinical unit" else "diagnosis_groups.csv"
    counts = pd.read_csv(RESULTS / "dashboard" / filename, index_col=0)
    proportions = counts.div(counts.sum(axis=1), axis=0)
    chart(px.imshow(proportions.rename(index=names()), aspect="auto", color_continuous_scale="Blues",
                    labels={"color": "Within-band proportion"}, title="Distribution within each cognitive band"), 330)
    with st.expander("Counts and grouped-validation results"):
        grid(counts.reset_index())
        grid(pd.DataFrame([grouped]))
    st.caption("Diagnosis-stratified association does not establish absence of other confounding, appropriate placement, or treatment benefit.")


def hypotheses():
    heading("Hypothesis summary", "Interpret the four original hypotheses within their actual analysis and validation designs.")
    for title, verdict, interpretation in hypothesis_rows():
        with st.container(border=True):
            left, right = st.columns([1, 2])
            with left:
                st.subheader(title)
                st.markdown(f"**{verdict}**")
            with right:
                st.write(interpretation)
    st.caption("The patient-level extension adds separate exploratory evidence. Its results do not retroactively change the original hypothesis designs.")


def new_profile():
    heading("New profile", "Apply the saved discovery-fitted transformation to available test scores and compare with a research partition.", "PATIENT-LEVEL MODEL / EXPLORATORY ASSIGNMENT")
    st.info("Research use. Assignments and distances have no established diagnostic or treatment-planning validity.")
    bundle = profile_model()
    pp = bundle["preprocessor"]
    groups = st.radio("Reference partition", [2, 3], format_func=lambda x: f"{x} groups", horizontal=True)
    st.caption("Enter original test scores in the source measurement units. Leave unobserved tests blank. The model handles direction, clipping, scaling and imputation.")
    with st.form("profile_inputs"):
        values = {}
        for col, (domain, tests) in zip(st.columns(3) * 2, pp.domains.items()):
            with col:
                st.markdown(f"**{domain}**")
                for test in tests:
                    values[test] = st.number_input(test, value=None, step=1.0, format="%.2f")
        submit = st.form_submit_button("Compare profile", type="primary")
    if not submit:
        return
    try:
        result = assign_profile(values, groups)
    except ValueError as error:
        st.error(str(error))
        return
    metrics([("Assigned research group", str(result["cluster"]+1)), ("Observed tests", f"{result['observed']} / 14"),
             ("Imputed tests", str(len(result["imputed"]))), ("Tests clipped", str(len(result["clipped"])))])
    if result["observed"] < 7:
        st.warning("Fewer than seven tests were observed. This profile relies heavily on imputation; the stricter completeness analysis does not cover it.")
    if result["clipped"]:
        st.caption("Scores outside discovery clipping bounds: " + ", ".join(result["clipped"]))
    frame = pd.DataFrame({"domain": DOMAINS, "Entered profile": result["domains"], "Assigned group center": result["center"]})
    chart(profile_lines(frame.melt(id_vars="domain", var_name="Profile", value_name="Score"), "Score", "Profile"), 300)
    grid(pd.DataFrame({"Group": np.arange(1, groups+1), "Distance in robust domain space": result["distances"]}))
    st.caption("Distances are not probabilities. Group numbers apply only to this fitted model. All transformations are held fixed at discovery estimates.")


def advanced():
    heading("Advanced analytics", "Examine what drives the assessment-level partition and how its structure changes under resampling.")
    importance, stability, sensitivity = st.tabs(["Feature importance", "Resampling stability", "Variable availability"])
    with importance:
        fi = saved("feature_importance")
        metrics([("Surrogate accuracy", f"{fi['cv_accuracy_mean']:.1%}"), ("Trees", str(fi['n_estimators'])),
                 ("Assessments", f"{fi['n_samples']:,}"), ("Target groups", str(fi['n_clusters']))])
        for col, (key, title) in zip(st.columns(2), [("gini_importance", "Gini importance"), ("permutation_importance_mean", "Permutation importance")]):
            with col:
                series = pd.Series(fi[key]).sort_values()
                chart(px.bar(x=series.values, y=series.index, orientation="h", title=title,
                             labels={"x": "Importance", "y": ""}, color_discrete_sequence=COLORS), 340)
        st.caption("The surrogate predicts existing cluster labels. Its accuracy describes label reproduction and does not measure clinical outcome prediction.")
    with stability:
        cv = saved("cross_validation_stability")
        metrics([("Mean pairwise ARI", f"{cv['mean_ari']:.3f}"), ("Median ARI", f"{cv['median_ari']:.3f}"),
                 ("Resamples", str(cv['n_iterations'])), ("Sampling fraction", f"{cv['subsample_fraction']:.0%}")])
        chart(px.histogram(x=cv["pairwise_ari_values"], nbins=25, labels={"x": "Pairwise ARI"}, color_discrete_sequence=COLORS), 330)
        st.caption("This assessment-level analysis samples rows and does not account for repeated visits within patients. Patient-level resampling is reported separately.")
    with sensitivity:
        frame = table("Sensitivity_Analysis.csv")
        plotted = frame.copy()
        plotted.loc[plotted.n_clusters < 2, "silhouette"] = np.nan
        fig = px.line(plotted, x="threshold", y="silhouette", markers=True,
                      labels={"threshold": "Maximum variable missingness (%)", "silhouette": "Silhouette"}, color_discrete_sequence=COLORS)
        fig.update_xaxes(range=[28, 72], dtick=10)
        fig.add_annotation(x=30, y=0, yref="paper", text="No clusters", showarrow=False, yshift=15)
        chart(fig, 320)
        grid(frame)
        st.caption("The threshold selects variables. Assessment eligibility requires at least one retained test. At 30%, no clusters are recovered: silhouette is undefined and is omitted from the plot. The saved table uses −1 as a sentinel for that failed fit.")


def robustness():
    heading("Robustness", "Read supplementary uncertainty estimates alongside their sampling and preprocessing assumptions.")
    st.info("Earlier multiple-imputation and complete-case comparisons used raw-test aggregation. They do not validate the standardized patient-level pipeline.")
    bootstrap, correction, missingness, followup = st.tabs(["Bootstrap intervals", "Pairwise comparisons", "Missing-data sensitivity", "Follow-up"])
    with bootstrap:
        frame = table("Backlog_Bootstrap_CIs.csv").copy()
        selected = frame[frame.metric.isin(["H2_mean_ARI", "H3_cramers_v", "H4_silhouette_gap"])].copy()
        metric_names = {"H1_silhouette": "H1 · Silhouette", "H2_mean_ARI": "H2 · Mean ARI",
                        "H3_chi2": "H3 · Chi-square", "H3_cramers_v": "H3 · Cramér's V",
                        "H4_silhouette_gap": "H4 · Silhouette gap"}
        selected["metric"] = selected.metric.map(metric_names)
        fig = px.scatter(selected, x="point", y="metric", error_x=selected.ci_hi-selected.point,
                         error_x_minus=selected.point-selected.ci_lo, labels={"point": "Estimate and 95% bootstrap interval", "metric": ""}, color_discrete_sequence=COLORS)
        fig.add_vline(x=0, line_dash="dot", line_color="#8A8F98")
        chart(fig, 240)
        frame["metric"] = frame.metric.map(metric_names)
        grid(frame.rename(columns={"metric": "Statistic", "point": "Estimate", "ci_lo": "95% lower", "ci_hi": "95% upper"}))
        st.caption("Assessment-level resampling ignores within-patient dependence. These intervals should not be read as patient-grouped uncertainty.")
    with correction:
        frame = table("Backlog_H2_Holm.csv")
        grid(frame, height=390)
        st.caption("Pairwise comparisons use the fixed-reference assignment design with multiplicity adjustment. Repeated partition comparisons do not establish discrete phenotypes.")
    with missingness:
        st.subheader("Across-imputation descriptive summaries")
        grid(table("Backlog_Rubin_Pooled.csv"))
        st.caption("Five MICE draws. Within-imputation variances were not estimated, so the intervals are not Rubin-rule confidence intervals.")
        st.subheader("Complete-assessment comparison")
        grid(table("Backlog_Listwise_Comparison.csv"))
    with followup:
        grid(table("Backlog_TSI_Phenotype.csv"))
        grid(table("Backlog_Within_Patient_Transitions.csv"))
        st.caption("Time since injury and repeated cognitive assessments provide follow-up descriptions, without an independent functional endpoint. They do not establish causal recovery or treatment benefit.")


PAGES = {"Home": home, "Patient-Level Research": research, "Cluster Explorer": explorer,
         "Cognitive Profiles": profiles, "Patient Lookup": lookup, "Imputation Compare": imputation,
         "Clinical Units": clinical, "Hypothesis Summary": hypotheses, "New Profile": new_profile,
         "Advanced Analytics": advanced, "Robustness": robustness}
