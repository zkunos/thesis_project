const pptx = require("pptxgenjs");
const path = require("path");

const FIG = "/Users/zoltankunos/Desktop/thesis_project_clean/report/Figures";
const f = (n) => path.join(FIG, n);

// ---- Modern-minimal palette (no # prefix) ----
const BG = "FFFFFF";
const INK = "1B2A30";   // titles
const BODY = "3C4A52";  // body text
const MUTED = "7C8A94"; // captions / footer
const RULE = "E3E9EC";  // hairlines / panels border
const PANEL = "F5F8F9"; // light panel fill
const ACCENT = "11707A";// primary deep teal
const ACCENT_D = "0C525A";
// tier semantic colors
const T_AA = "2E8B7F";  // Above-Average
const T_NN = "D49A4E";  // Near-Normal
const T_GI = "C25B57";  // Global Impairment

const FONT = "Arial";
const W = 13.333, H = 7.5, MX = 0.7;

const deck = new pptx();
deck.defineLayout({ name: "W", width: W, height: H });
deck.layout = "W";
deck.author = "Zoltan Kunos";
deck.title = "Data-Driven Cognitive Phenotyping in Acquired Brain Injury";

// image native sizes (px) for aspect ratios
const RATIO = {
  "tsne_umap_clusters.png": 5365/2060,
  "cognitive_radar_profiles.png": 3411/1511,
  "feature_importance.png": 4168/1851,
  "missingness_barplot.png": 3569/1770,
  "missingness_heatmap.png": 3874/2370,
  "dl_missingness_cooccurrence.png": 2772/2370,
  "h2_ari_nmi_heatmap.png": 5007/2162,
  "h2_consensus_confidence.png": 2370/1470,
  "h3_clinical_unit_heatmap.png": 1400/1000,
  "h3_diagnosis_distribution.png": 3556/1767,
  "h4_domain_vs_variable.png": 2700/800,
  "dashboard_home.png": 1920/945,
  "dashboard_cluster_explorer.png": 1920/945,
  "domain_heatmap_clusters.png": 3256/2369,
};

function bg(slide){ slide.background = { color: BG }; }

function header(slide, kicker, title){
  slide.addText(kicker.toUpperCase(), { x: MX, y: 0.46, w: W-2*MX, h: 0.3,
    fontFace: FONT, fontSize: 11.5, bold: true, color: ACCENT, charSpacing: 2 });
  slide.addText(title, { x: MX, y: 0.74, w: W-2*MX, h: 0.62,
    fontFace: FONT, fontSize: 27, bold: true, color: INK });
  slide.addShape(deck.ShapeType.rect, { x: MX, y: 1.42, w: 0.85, h: 0.07, fill: { color: ACCENT } });
}

let PAGE = 0;
function footer(slide){
  PAGE++;
  slide.addShape(deck.ShapeType.line, { x: MX, y: 6.98, w: W-2*MX, h: 0, line: { color: RULE, width: 1 } });
  slide.addText("Zoltan Kunos  ·  Data-Driven Cognitive Phenotyping in ABI", { x: MX, y: 7.04, w: 9, h: 0.3,
    fontFace: FONT, fontSize: 9, color: MUTED });
  slide.addText(String(PAGE), { x: W-MX-1, y: 7.04, w: 1, h: 0.3, align: "right",
    fontFace: FONT, fontSize: 9, color: MUTED });
}

// fit an image inside a box, centered
function fitImg(slide, name, bx, by, bw, bh, opts={}){
  const r = RATIO[name];
  let w = bw, h = w/r;
  if (h > bh){ h = bh; w = h*r; }
  const x = bx + (bw-w)/2, y = by + (bh-h)/2;
  slide.addImage({ path: f(name), x, y, w, h, ...opts });
  return { x, y, w, h };
}

function notes(slide, t){ slide.addNotes(t); }

// generic content slide
function content(kicker, title){
  const s = deck.addSlide(); bg(s); header(s, kicker, title); footer(s); return s;
}

// bullet list block
function bullets(slide, items, x, y, w, opts={}){
  slide.addText(items.map(it => ({ text: it, options: { bullet: { code: "2022", indent: 16 }, breakLine: true } })),
    { x, y, w, h: opts.h||4.2, fontFace: FONT, fontSize: opts.fontSize||15.5, color: BODY,
      lineSpacingMultiple: 1.22, paraSpaceAfter: opts.gap!=null?opts.gap:9, valign: "top" });
}

// stat chip
function stat(slide, x, y, w, num, label, col){
  slide.addText(num, { x, y, w, h: 0.62, fontFace: FONT, fontSize: 30, bold: true, color: col||ACCENT, align: "center" });
  slide.addText(label, { x, y: y+0.62, w, h: 0.5, fontFace: FONT, fontSize: 11.5, color: MUTED, align: "center" });
}

// rounded panel
function panel(slide, x, y, w, h, fill){
  slide.addShape(deck.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.08,
    fill: { color: fill||PANEL }, line: { color: RULE, width: 1 } });
}

// ============================================================ SLIDE 1 — TITLE
(function(){
  const s = deck.addSlide(); bg(s);
  // left accent band
  s.addShape(deck.ShapeType.rect, { x: 0, y: 0, w: 0.28, h: H, fill: { color: ACCENT } });
  s.addText("MSC THESIS DEFENSE", { x: 1.0, y: 1.5, w: 11, h: 0.4, fontFace: FONT, fontSize: 13, bold: true, color: ACCENT, charSpacing: 3 });
  s.addText("Data-Driven Cognitive Phenotyping\nin Acquired Brain Injury", { x: 1.0, y: 1.95, w: 11.4, h: 1.9,
    fontFace: FONT, fontSize: 40, bold: true, color: INK, lineSpacingMultiple: 1.04 });
  s.addText("Does unsupervised learning reveal hidden cognitive subtypes — or a single severity gradient?",
    { x: 1.0, y: 3.95, w: 10.6, h: 0.6, fontFace: FONT, fontSize: 16, italic: true, color: BODY });
  s.addShape(deck.ShapeType.line, { x: 1.0, y: 4.85, w: 5.5, h: 0, line: { color: RULE, width: 1.5 } });
  s.addText([
    { text: "Zoltan Kunos", options: { bold: true, color: INK, fontSize: 16 } },
    { text: "\nMSc Fundamental Principles of Data Science · Universitat de Barcelona", options: { color: BODY, fontSize: 13 } },
    { text: "\nSupervisor: Dr. Alejandro García-Rudolph", options: { color: BODY, fontSize: 13 } },
  ], { x: 1.0, y: 5.05, w: 10, h: 1.2, fontFace: FONT, lineSpacingMultiple: 1.18 });
  s.addText("14 June 2026", { x: W-MX-3, y: 6.55, w: 3, h: 0.3, align: "right", fontFace: FONT, fontSize: 11, color: MUTED });
  notes(s, "The title of my dissertation is 'Data-Driven Cognitive Phenotyping in Acquired Brain Injury.' The central question is whether routinely recorded neuropsychological data can provide a consistent, reliable form of cognitive organisation after ABI — even though these datasets are far messier than clinical trial data. The short answer is yes: but the structure is not sharp lines between subtypes. The dominant signal is a cognitive severity gradient, which clustering divides into three clinically meaningful tiers.");
})();

// ============================================================ SLIDE 2 — THESIS
(function(){
  const s = content("The argument in one sentence", "Thesis");
  panel(s, MX, 1.75, W-2*MX, 1.55, PANEL);
  s.addText([
    { text: "In incomplete routine neuropsychological data, unsupervised learning identifies a robust cognitive ", options: {} },
    { text: "severity gradient", options: { bold: true, color: ACCENT } },
    { text: " — not a hidden ", options: {} },
    { text: "subtype", options: { bold: true, color: T_GI } },
    { text: " structure.", options: {} },
  ], { x: MX+0.5, y: 1.95, w: W-2*MX-1, h: 1.15, fontFace: FONT, fontSize: 22, color: INK, lineSpacingMultiple: 1.12, valign: "middle" });

  const cards = [
    ["01", "Diagnosis is not enough", "Two patients with the same ABI diagnosis can have very different rehabilitation needs."],
    ["02", "Missingness is structured", "Missing values encode fatigue, intolerance, and clinician judgement — not random gaps."],
    ["03", "Robust to imputation", "The same tiers recur across imputation strategies — more credible than one arbitrary choice."],
  ];
  const cw = (W-2*MX-0.8)/3;
  cards.forEach((c,i)=>{
    const x = MX + i*(cw+0.4);
    panel(s, x, 3.65, cw, 2.95);
    s.addText(c[0], { x: x+0.3, y: 3.85, w: cw-0.6, h: 0.6, fontFace: FONT, fontSize: 26, bold: true, color: ACCENT });
    s.addText(c[1], { x: x+0.3, y: 4.5, w: cw-0.6, h: 0.7, fontFace: FONT, fontSize: 15.5, bold: true, color: INK });
    s.addText(c[2], { x: x+0.3, y: 5.25, w: cw-0.6, h: 1.2, fontFace: FONT, fontSize: 12.5, color: BODY, lineSpacingMultiple: 1.18 });
  });
  notes(s, "Three ideas in one sentence. First, diagnosis cannot fully explain cognitive variability — same diagnosis, different needs. Second, missingness must be modelled, because missing values are not random: they reflect fatigue, impairment, test intolerance, examiner judgement. Third, whichever imputation strategy I pick, the recovered tiers agree — so the result is more credible than one arbitrary preprocessing choice. The thesis is therefore both clinical (what structure exists after ABI) and methodological (does that structure survive the missing-data decisions).");
})();

// ============================================================ SLIDE 3 — CLINICAL PROBLEM
(function(){
  const s = content("Why this matters", "The clinical problem: heterogeneity");
  bullets(s, [
    "ABI disrupts attention, memory, language, executive function and visuospatial cognition — and rarely in the same way twice.",
    "Diagnosis and injury severity frame the scope of need, but not the individual pattern or degree of impairment.",
    "Two patients with 'memory deficits' can require entirely different rehabilitation.",
  ], MX, 1.85, 6.5, { fontSize: 16, gap: 12 });

  panel(s, 7.5, 1.85, W-MX-7.5, 4.7);
  s.addText("The missingness trap", { x: 7.8, y: 2.1, w: 4.7, h: 0.5, fontFace: FONT, fontSize: 16, bold: true, color: ACCENT });
  bullets(s, [
    "Batteries are administered when patients are least able to complete them.",
    "Dropping incomplete cases removes the most impaired patients — exactly those rehabilitation must serve.",
    "Missingness must be managed, not ignored.",
  ], 7.8, 2.65, 4.4, { fontSize: 13.5, gap: 10 });
  s.addShape(deck.ShapeType.line, { x: 7.8, y: 5.55, w: 4.4, h: 0, line: { color: RULE, width: 1 } });
  s.addText("Research question: can data-driven clustering produce clinically meaningful cognitive organisation — and does it survive principled handling of missing data?",
    { x: 7.8, y: 5.7, w: 4.55, h: 0.85, fontFace: FONT, fontSize: 12.5, italic: true, color: INK, lineSpacingMultiple: 1.15 });
  notes(s, "The clinical problem is heterogeneity: ABI affects many cognitive functions and not identically across patients. Clinicians use broad categories — diagnosis, injury severity — which frame scope but not the individual pattern. A second layer is missingness: batteries are often administered when patients are least able to complete them, so excluding incomplete cases would discard the most impaired patients. Hence the research question: can clustering produce clinically meaningful organisation, and can we trust it when missing data is managed rather than ignored?");
})();

// ============================================================ SLIDE 4 — PRE-REGISTERED TESTS
(function(){
  const s = content("Pre-registration", "Four hypotheses, objective criteria");
  const rows = [
    ["H1", "Discrete, stable clusters exist", "Silhouette > 0.40, < 30% noise, ≥ 2 clusters for most imputations"],
    ["H2", "Clustering is robust to imputation", "Mean pairwise ARI > 0.50 (fixed-reference design)"],
    ["H3", "Tiers are clinically relevant", "χ² association with clinical unit; Cramér's V > 0.10; adjust for diagnosis"],
    ["H4", "Domain aggregation helps", "Better separation, lower VIF and condition number vs. raw variables"],
  ];
  const y0 = 1.85, rh = 1.12, cols = W-2*MX;
  rows.forEach((r,i)=>{
    const y = y0 + i*(rh+0.13);
    panel(s, MX, y, cols, rh);
    s.addShape(deck.ShapeType.roundRect, { x: MX+0.18, y: y+0.22, w: 0.95, h: rh-0.44, rectRadius: 0.06, fill: { color: ACCENT } });
    s.addText(r[0], { x: MX+0.18, y: y+0.22, w: 0.95, h: rh-0.44, align: "center", valign: "middle", fontFace: FONT, fontSize: 20, bold: true, color: "FFFFFF" });
    s.addText(r[1], { x: MX+1.4, y: y+0.13, w: 5.0, h: rh-0.26, valign: "middle", fontFace: FONT, fontSize: 16, bold: true, color: INK });
    s.addText(r[2], { x: MX+6.6, y: y+0.13, w: cols-6.8, h: rh-0.26, valign: "middle", fontFace: FONT, fontSize: 13, color: BODY, lineSpacingMultiple: 1.12 });
  });
  notes(s, "I built the analysis around four pre-registered, quantitative hypotheses, each with an objective threshold. H1: discrete stable clusters — silhouette above 0.40, under 30% noise, at least two clusters for most imputations. H2: stability to imputation — mean pairwise ARI above 0.50, under a fixed-reference design where the embedding and partition are held fixed while imputed values vary. H3: clinical relevance — chi-square association with clinical unit, Cramér's V above 0.10, adjusting for diagnosis. H4: domain aggregation beats raw variables on separation, VIF and condition number. The point for the examiners: every claim has an objective test.");
})();

// ============================================================ SLIDE 5 — COHORT
(function(){
  const s = content("The data", "A large but incomplete cohort");
  const sx = MX, sy = 1.85, sw = (W-2*MX-1.2)/4;
  stat(s, sx+0*(sw+0.4), sy, sw, "17,406", "assessments", ACCENT);
  stat(s, sx+1*(sw+0.4), sy, sw, "7,285", "patients", ACCENT);
  stat(s, sx+2*(sw+0.4), sy, sw, "14", "variables", ACCENT);
  stat(s, sx+3*(sw+0.4), sy, sw, "6", "cognitive domains", ACCENT);

  // missingness barplot
  fitImg(s, "missingness_barplot.png", MX, 3.2, 7.4, 3.5);

  panel(s, 8.4, 3.2, W-MX-8.4, 3.45);
  s.addText("53.1%", { x: 8.6, y: 3.4, w: 3.8, h: 0.7, fontFace: FONT, fontSize: 34, bold: true, color: T_GI });
  s.addText("of rows are complete across all 14 variables", { x: 8.6, y: 4.1, w: 3.9, h: 0.6, fontFace: FONT, fontSize: 13, color: BODY });
  bullets(s, [
    "Complete-case analysis would discard ≈ 47% of assessments.",
    "Missingness is non-random — it tracks the testing process.",
    "Imputation is required to retain partially observed patients.",
  ], 8.6, 4.8, 3.9, { fontSize: 12.5, gap: 9 });
  notes(s, "All analyses use a rehabilitation-centre neuropsychology database. After filtering and removing assessments with no cognitive testing, 17,406 assessments from 7,285 patients remain, across 14 variables grouped into 6 cognitive domains. Only 53.1% of rows are complete on all 14 variables — so complete-case analysis would discard nearly 47% of assessments, and disproportionately the most impaired patients. Missingness is structured, not incidental, so imputation is required to keep partially observed assessments while letting us test sensitivity.");
})();

// ============================================================ SLIDE 6 — MISSINGNESS
(function(){
  const s = content("Structured, not random", "Missingness is clinically informative");
  fitImg(s, "missingness_heatmap.png", MX, 1.75, 7.4, 5.0);
  s.addText("Routine screening measures are far more complete than long specialist tests.",
    { x: 8.35, y: 1.85, w: W-MX-8.35, h: 0.9, fontFace: FONT, fontSize: 14, bold: true, color: INK, lineSpacingMultiple: 1.15 });
  bullets(s, [
    "Gaps encode fatigue, disorientation and reduced motivation.",
    "Motor load and task aversion shape which tests get completed.",
    "Clinicians may judge an alternative test more suitable.",
    "Dropping rows removes the most cognitively impaired patients.",
  ], 8.35, 2.9, 4.3, { fontSize: 13, gap: 11 });
  s.addText("→ Imputation must preserve these rows and expose sensitivity to the missing values.",
    { x: 8.35, y: 6.0, w: 4.3, h: 0.8, fontFace: FONT, fontSize: 12.5, italic: true, color: ACCENT, lineSpacingMultiple: 1.15 });
  notes(s, "This slide reinforces that missingness is structured. Routine screening measures are much more complete than specialised, time-consuming assessments. The gaps reflect the clinical testing process — fatigue, disorientation, motor load, reduced motivation, or a clinician judging another test more appropriate — not random administration error. Because removing partial rows also removes the most impaired patients, imputation must retain those rows and let us evaluate uncertainty around the imputed values.");
})();

// ============================================================ SLIDE 7 — PIPELINE
(function(){
  const s = content("Methods", "Analysis pipeline");
  const steps = [
    ["Impute", "10 strategies\nsimple → deep learning"],
    ["Scale", "standardise\nacross datasets"],
    ["Aggregate", "14 variables →\n6 domains"],
    ["UMAP", "manifold\nembedding"],
    ["HDBSCAN", "density clustering\n+ silhouette"],
  ];
  const n = steps.length, gap = 0.45, bw = (W-2*MX - (n-1)*gap)/n, by = 2.15, bh = 1.7;
  steps.forEach((st,i)=>{
    const x = MX + i*(bw+gap);
    panel(s, x, by, bw, bh, "FFFFFF");
    s.addShape(deck.ShapeType.rect, { x, y: by, w: bw, h: 0.12, fill: { color: ACCENT } });
    s.addText(st[0], { x, y: by+0.32, w: bw, h: 0.5, align: "center", fontFace: FONT, fontSize: 17, bold: true, color: INK });
    s.addText(st[1], { x: x+0.1, y: by+0.85, w: bw-0.2, h: 0.75, align: "center", fontFace: FONT, fontSize: 11.5, color: BODY, lineSpacingMultiple: 1.1 });
    if (i < n-1){
      s.addText("→", { x: x+bw, y: by, w: gap, h: bh, align: "center", valign: "middle", fontFace: FONT, fontSize: 22, bold: true, color: ACCENT });
    }
  });
  panel(s, MX, 4.35, W-2*MX, 2.05, PANEL);
  s.addText("Fixed-reference design (H2)", { x: MX+0.35, y: 4.55, w: 6, h: 0.45, fontFace: FONT, fontSize: 16, bold: true, color: ACCENT });
  s.addText("A single MICE solution anchors the scaler, UMAP embedding and HDBSCAN partition. Other imputations are projected through this fixed structure — testing whether imputed values land in the same place, not whether independently re-fit pipelines reproduce the hierarchy.",
    { x: MX+0.35, y: 5.05, w: W-2*MX-0.7, h: 1.2, fontFace: FONT, fontSize: 14, color: BODY, lineSpacingMultiple: 1.25 });
  notes(s, "The pipeline: I compared ten imputation strategies from simple to model-based, donor-based, matrix completion and deep learning. After imputation I standardise scores and aggregate them into six cognitive domains, embed with UMAP, and cluster with HDBSCAN, evaluating quality by silhouette versus noise. For H2 I use a fixed-reference design: a MICE solution defines an anchor scaler, embedding and HDBSCAN partition, and other imputations are projected through it. This tests whether imputed values fall in similar locations under a fixed structure — a deliberately scoped claim, distinct from re-fitting the whole pipeline per dataset.");
})();

// ============================================================ SLIDE 8 — H1 RESULT
(function(){
  const s = content("Result · H1", "Three cognitive severity tiers emerge");
  fitImg(s, "tsne_umap_clusters.png", MX, 1.9, 7.6, 4.7);
  const tiers = [
    ["Above-Average", "6,725", "above cohort mean", T_AA],
    ["Near-Normal", "6,328", "close to the average", T_NN],
    ["Global Impairment", "4,353", "below cohort mean", T_GI],
  ];
  let ty = 1.95;
  tiers.forEach(t=>{
    s.addShape(deck.ShapeType.roundRect, { x: 8.5, y: ty, w: W-MX-8.5, h: 1.15, rectRadius: 0.06, fill: { color: PANEL }, line: { color: RULE, width: 1 } });
    s.addShape(deck.ShapeType.rect, { x: 8.5, y: ty, w: 0.13, h: 1.15, fill: { color: t[3] } });
    s.addText(t[0], { x: 8.75, y: ty+0.13, w: 2.6, h: 0.4, fontFace: FONT, fontSize: 14.5, bold: true, color: INK });
    s.addText(t[2], { x: 8.75, y: ty+0.55, w: 2.6, h: 0.5, fontFace: FONT, fontSize: 11.5, color: BODY });
    s.addText(t[1], { x: 11.3, y: ty+0.2, w: 1.3, h: 0.7, align: "right", valign: "middle", fontFace: FONT, fontSize: 20, bold: true, color: t[3] });
    ty += 1.32;
  });
  s.addText("All 10 imputations cleared pre-registered thresholds · MICE reference silhouette ≈ 0.53 · k = 3. Not natural kinds — ordered bands on a continuum.",
    { x: MX, y: 6.45, w: 7.6, h: 0.5, fontFace: FONT, fontSize: 11.5, italic: true, color: MUTED, lineSpacingMultiple: 1.12 });
  notes(s, "The first result: three severity tiers emerge — Above-Average with 6,725 assessments scoring above the cohort mean; Near-Normal with 6,328 near the average; and Global Impairment with 4,353 below the mean. All ten imputations cleared the pre-registered thresholds; in the MICE reference, the full-coverage silhouette was about 0.53 with three tiers recovered. I deliberately do not call these natural kinds or sharply separated phenotypes — they are best understood as ordered bands on a severity continuum.");
})();

// ============================================================ SLIDE 9 — SEVERITY PROFILE
(function(){
  const s = content("Interpretation · H1", "The signal is global severity");
  fitImg(s, "cognitive_radar_profiles.png", MX, 1.85, 7.3, 4.7);
  panel(s, 8.2, 1.9, W-MX-8.2, 4.5);
  s.addText("PC1", { x: 8.45, y: 2.1, w: 3.9, h: 0.5, fontFace: FONT, fontSize: 16, bold: true, color: ACCENT });
  s.addText("≈ 56%", { x: 8.45, y: 2.5, w: 3.9, h: 0.7, fontFace: FONT, fontSize: 34, bold: true, color: INK });
  s.addText("of variance — a single dominant axis", { x: 8.45, y: 3.2, w: 3.9, h: 0.5, fontFace: FONT, fontSize: 12.5, color: BODY });
  s.addShape(deck.ShapeType.line, { x: 8.45, y: 3.85, w: 3.9, h: 0, line: { color: RULE, width: 1 } });
  bullets(s, [
    "All domains load positively on PC1.",
    "Radar profiles are concentric — same shape, different size.",
    "No symptom-specific dissociation dominates.",
  ], 8.45, 4.0, 3.9, { fontSize: 13, gap: 11 });
  notes(s, "The first major finding is a strong cognitive severity gradient. PCA confirms it: the first component explains nearly 56% of variance, and every domain loads positively on it — the signature of a broad severity dimension. The radar profiles are concentric: tiers share the same shape but differ in overall level. So the dominant signal is not a symptom-specific dissociation or a catalogue of distinct subtypes — it is global cognitive severity.");
})();

// ============================================================ SLIDE 10 — H2 RESULT
(function(){
  const s = content("Result · H2", "Robust across imputation methods");
  fitImg(s, "h2_ari_nmi_heatmap.png", MX, 1.9, 7.5, 4.6);
  const sx = 8.45, sw = W-MX-8.45;
  stat(s, sx, 1.95, sw, "0.71", "mean pairwise ARI   (95% CI 0.70–0.72)", ACCENT);
  s.addShape(deck.ShapeType.line, { x: sx, y: 3.25, w: sw, h: 0, line: { color: RULE, width: 1 } });
  const mini = [["44 / 45", "method pairs survive Holm correction"], ["> 86%", "assessments with high-confidence consensus"]];
  let my = 3.45;
  mini.forEach(m=>{
    s.addText(m[0], { x: sx, y: my, w: sw, h: 0.5, fontFace: FONT, fontSize: 24, bold: true, color: INK, align: "center" });
    s.addText(m[1], { x: sx, y: my+0.5, w: sw, h: 0.45, fontFace: FONT, fontSize: 11.5, color: MUTED, align: "center" });
    my += 1.15;
  });
  s.addText("Only KNN vs. SoftImpute fell just short. Scope: point assignments are stable under a fixed embedding and partition.",
    { x: sx, y: 5.85, w: sw, h: 0.8, fontFace: FONT, fontSize: 11, italic: true, color: MUTED, lineSpacingMultiple: 1.15 });
  notes(s, "Second finding: robustness to imputation. The mean pairwise adjusted Rand index across methods is 0.71, bootstrap 95% CI 0.70 to 0.72 — substantial agreement. Of 45 method-pair comparisons, 44 survived Holm correction; the only exception was KNN versus SoftImpute, just under threshold. At the assessment level, over 86% of assessments received high-confidence consensus labels. So the choice of imputation matters little for point assignments under a fixed embedding and partition — though I'm careful that this is the scope of the claim, not that independently re-fit pipelines yield identical density hierarchies.");
})();

// ============================================================ SLIDE 11 — WHY IMPUTATION MATTERS
(function(){
  const s = content("Result · H2", "Complete-case analysis changes the answer");
  const head = [
    { text: "", options: { fill: { color: "FFFFFF" } } },
    { text: "MICE reference", options: { fill: { color: ACCENT }, color: "FFFFFF", bold: true, align: "center" } },
    { text: "Complete-case", options: { fill: { color: T_GI }, color: "FFFFFF", bold: true, align: "center" } },
  ];
  const data = [
    head,
    ["Assessments retained", "100%", "53.1%"],
    ["Tiers recovered", "3", "2"],
    ["Silhouette", "≈ 0.53", "≈ 0.26"],
    ["ARI vs. reference (shared rows)", "—", "≈ 0.63"],
  ];
  s.addTable(data, { x: MX, y: 1.95, w: 7.6, colW: [3.4, 2.1, 2.1], rowH: [0.55,0.7,0.7,0.7,0.7],
    fontFace: FONT, fontSize: 14, color: BODY, align: "center", valign: "middle",
    border: { pt: 1, color: RULE }, fill: { color: "FFFFFF" } });
  // left-align first column text by overlay? Keep center for simplicity.

  panel(s, 8.5, 1.95, W-MX-8.5, 4.55);
  s.addText("Deleting cases is not a weaker version of the same analysis —", { x: 8.75, y: 2.2, w: 3.85, h: 0.9, fontFace: FONT, fontSize: 15, bold: true, color: INK, lineSpacingMultiple: 1.18 });
  s.addText("it changes the partition.", { x: 8.75, y: 3.05, w: 3.85, h: 0.5, fontFace: FONT, fontSize: 17, bold: true, color: T_GI });
  s.addShape(deck.ShapeType.line, { x: 8.75, y: 3.7, w: 3.85, h: 0, line: { color: RULE, width: 1 } });
  s.addText("The baseline collapses three tiers to two and halves the silhouette. How missing data is handled becomes part of the model's substantive output.",
    { x: 8.75, y: 3.85, w: 3.85, h: 2, fontFace: FONT, fontSize: 13, color: BODY, lineSpacingMultiple: 1.25 });
  notes(s, "This shows why imputation matters. Restrict to complete cases and only 53.1% of the 17,406 assessments remain. The complete-case baseline recovers two clusters, not three, and its silhouette drops to about 0.26 versus 0.53 for the MICE reference. Even on shared assessments, the ARI between the two solutions is only about 0.63 — far from identical. So deleting incomplete cases is not a less-powerful version of the same analysis; it changes the partition. How you handle missing data is part of the model's substantive output.");
})();

// ============================================================ SLIDE 12 — H3 RESULT
(function(){
  const s = content("Result · H3", "Tiers track clinical unit assignment");
  fitImg(s, "h3_clinical_unit_heatmap.png", MX, 1.9, 6.6, 4.7);
  const sx = 7.7, sw = W-MX-7.7;
  s.addText([
    { text: "χ² = 911", options: { bold: true, fontSize: 26, color: INK } },
    { text: "   p < 10⁻¹⁵⁶", options: { fontSize: 15, color: BODY } },
  ], { x: sx, y: 1.95, w: sw, h: 0.6, fontFace: FONT });
  stat(s, sx, 2.75, sw, "0.16", "Cramér's V  ( pre-registered threshold 0.10 )", ACCENT);
  s.addShape(deck.ShapeType.line, { x: sx, y: 4.05, w: sw, h: 0, line: { color: RULE, width: 1 } });
  bullets(s, [
    "Cochran–Mantel–Haenszel: association holds after adjusting for diagnosis.",
    "Severity tier adds predictive information beyond diagnostic label.",
    "Informs rehabilitation routing — it does not dictate placement.",
  ], sx, 4.2, sw, { fontSize: 13.5, gap: 12 });
  notes(s, "Third hypothesis: are the severity tiers clinically relevant? A chi-square test between tier and clinical unit gives chi-square 911, p below ten-to-the-minus-156, and Cramér's V of 0.16 — above my pre-registered 0.10 threshold, so H3 is supported. A Cochran–Mantel–Haenszel test shows the association persists after adjusting for diagnosis, so tier carries information beyond the diagnostic label. Clinically, global-impairment patients plausibly need more intensive rehabilitation. The claim is that tier informs routing decisions, not that it dictates placement.");
})();

// ============================================================ SLIDE 13 — H4 RESULT
(function(){
  const s = content("Result · H4", "Domain aggregation is more stable");
  fitImg(s, "h4_domain_vs_variable.png", MX, 1.85, W-2*MX, 2.2);
  const metrics = [
    ["Silhouette", "0.47", "0.48", T_AA],
    ["Mean VIF", "2.80", "1.90", ACCENT],
    ["Condition number", "62", "12", ACCENT],
  ];
  const cw = (W-2*MX-0.8)/3;
  metrics.forEach((m,i)=>{
    const x = MX+i*(cw+0.4), y = 4.35;
    panel(s, x, y, cw, 2.0);
    s.addText(m[0], { x: x+0.2, y: y+0.18, w: cw-0.4, h: 0.4, fontFace: FONT, fontSize: 14, bold: true, color: INK, align: "center" });
    s.addText([
      { text: m[1]+"  ", options: { color: MUTED, fontSize: 17, strike: true } },
      { text: "→  ", options: { color: MUTED, fontSize: 15 } },
      { text: m[2], options: { color: m[3], fontSize: 28, bold: true } },
    ], { x: x+0.2, y: y+0.7, w: cw-0.4, h: 0.8, align: "center", valign: "middle", fontFace: FONT });
    s.addText("variables → domains", { x: x+0.2, y: y+1.5, w: cw-0.4, h: 0.35, fontFace: FONT, fontSize: 10.5, color: MUTED, align: "center" });
  });
  notes(s, "Final hypothesis: does aggregating variables into domains beat clustering raw variables? Domain-level clustering was marginally better on separation — silhouette 0.48 versus 0.47 — but much better on numerical stability: mean VIF fell from about 2.80 to 1.90, and the condition number from about 62 to 12. That matters for distance-based methods like UMAP and HDBSCAN, which are sensitive to redundant, correlated features. Aggregating into clinically meaningful domains reduces redundancy while keeping interpretable constructs — so it's preferable on both stability and interpretability.");
})();

// ============================================================ SLIDE 14 — RESULT SUMMARY
(function(){
  const s = content("Synthesis", "All four hypotheses supported");
  const rows = [
    ["H1", "Stable clusters recovered — read as severity tiers, not subtypes", T_AA],
    ["H2", "Mean pairwise ARI ≈ 0.71 under the fixed-reference design", ACCENT],
    ["H3", "Tier ↔ clinical unit, significant after adjusting for diagnosis", ACCENT],
    ["H4", "Domain aggregation improves stability (VIF, condition number)", ACCENT],
  ];
  const cw = (W-2*MX-0.5)/2, ch = 1.55;
  rows.forEach((r,i)=>{
    const x = MX + (i%2)*(cw+0.5), y = 1.95 + Math.floor(i/2)*(ch+0.4);
    panel(s, x, y, cw, ch);
    s.addText(r[0], { x: x+0.25, y: y+0.2, w: 1.3, h: ch-0.4, valign: "middle", fontFace: FONT, fontSize: 30, bold: true, color: r[2] });
    s.addText("✓ supported", { x: x+cw-1.9, y: y+0.22, w: 1.65, h: 0.35, align: "right", fontFace: FONT, fontSize: 11, bold: true, color: T_AA });
    s.addText(r[1], { x: x+1.6, y: y+0.2, w: cw-1.85, h: ch-0.4, valign: "middle", fontFace: FONT, fontSize: 13.5, color: BODY, lineSpacingMultiple: 1.18 });
  });
  s.addText("→ Empirical support for a missingness-aware severity-stratification framework for routine neuropsychological data after ABI.",
    { x: MX, y: 6.0, w: W-2*MX, h: 0.7, fontFace: FONT, fontSize: 14, italic: true, color: INK, align: "center", lineSpacingMultiple: 1.15 });
  notes(s, "Summarising the four hypotheses. H1 supported: stable clusters, interpreted as severity tiers rather than categorical subtypes. H2 supported within the fixed-reference design: mean pairwise ARI about 0.71. H3 supported: tier relates to clinical unit and stays significant after adjusting for diagnosis. H4 supported: domain-level clustering gives better numerical properties. Together these support developing and applying a missingness-aware severity-stratification approach for routine post-ABI neuropsychological assessment.");
})();

// ============================================================ SLIDE 15 — INTERPRETATION
(function(){
  const s = content("What it means", "A continuum, not a catalogue");
  // gradient band built from 3 colored segments
  const gy = 2.0, gh = 0.9, gx = MX, gw = W-2*MX;
  const seg = gw/3;
  [[T_AA,"Above-Average"],[T_NN,"Near-Normal"],[T_GI,"Global Impairment"]].forEach((c,i)=>{
    s.addShape(deck.ShapeType.rect, { x: gx+i*seg, y: gy, w: seg, h: gh, fill: { color: c[0] } });
    s.addText(c[1], { x: gx+i*seg, y: gy, w: seg, h: gh, align: "center", valign: "middle", fontFace: FONT, fontSize: 13, bold: true, color: "FFFFFF" });
  });
  s.addText("less impaired", { x: gx, y: gy+gh+0.05, w: 3, h: 0.3, fontFace: FONT, fontSize: 10.5, color: MUTED });
  s.addText("more impaired", { x: gx+gw-3, y: gy+gh+0.05, w: 3, h: 0.3, align: "right", fontFace: FONT, fontSize: 10.5, color: MUTED });

  bullets(s, [
    "Subtypes would imply qualitatively different cognitive profiles.",
    "A gradient implies differences lie mostly along one severity axis.",
    "Evidence for the gradient: concentric radar profiles, PC1 > 50% variance, all-positive loadings, tiers as ordered bands.",
    "Domain-specific dissociations may exist — but here, severity dominates.",
    "Poor scaling, non-cognitive measures or dropped data can fake subtype structure.",
  ], MX, 3.55, W-2*MX, { fontSize: 14.5, gap: 11 });
  notes(s, "The central interpretation: this dataset contains a continuum of cognitive severity, not a collection of discrete subtypes. The distinction matters. A subtype reading implies qualitatively different profiles; a gradient reading implies differences lie almost entirely along an overall severity axis spanning domains. The evidence favours the gradient: concentric radar plots, over half the variance on PC1, all-positive PC1 loadings, and tiers that behave like ordered bands. Domain-specific dissociations can exist after injury, but in this imputation-robust domain-level pipeline, overall severity dominates. And crucially, poor scaling, non-cognitive measures, or dropping missing data can manufacture spurious subtype-like patterns.");
})();

// ============================================================ SLIDE 16 — UTILITY
(function(){
  const s = content("So what", "Clinical and analytic utility");
  const cw = (W-2*MX-0.5)/2, y = 1.95, ch = 4.4;
  // clinical
  panel(s, MX, y, cw, ch);
  s.addShape(deck.ShapeType.rect, { x: MX, y, w: cw, h: 0.14, fill: { color: ACCENT } });
  s.addText("Clinical users", { x: MX+0.3, y: y+0.3, w: cw-0.6, h: 0.5, fontFace: FONT, fontSize: 18, bold: true, color: INK });
  bullets(s, [
    "A shared vocabulary for rehabilitation intensity.",
    "Confidence scores flag borderline cases.",
    "Reduces misinterpretation of cognitive assessment results.",
  ], MX+0.3, y+1.0, cw-0.6, { fontSize: 14, gap: 13 });
  // analytic
  panel(s, MX+cw+0.5, y, cw, ch);
  s.addShape(deck.ShapeType.rect, { x: MX+cw+0.5, y, w: cw, h: 0.14, fill: { color: T_AA } });
  s.addText("Analytic users", { x: MX+cw+0.8, y: y+0.3, w: cw-0.6, h: 0.5, fontFace: FONT, fontSize: 18, bold: true, color: INK });
  bullets(s, [
    "A reproducible missing-data-aware pipeline.",
    "Adaptable for linking cognition to outcomes.",
    "Missing-data choices made explicit and testable.",
  ], MX+cw+0.8, y+1.0, cw-0.6, { fontSize: 14, gap: 13 });
  s.addText("Long-term contribution: transparency about how missingness is handled — make the decisions explicit, then test their influence.",
    { x: MX, y: 6.45, w: W-2*MX, h: 0.5, fontFace: FONT, fontSize: 12.5, italic: true, color: MUTED, align: "center" });
  notes(s, "Two communities benefit. Clinical users gain a shared vocabulary for discussing rehabilitation intensity, with confidence scores that flag borderline cases and reduce misinterpretation. Analytic users gain a reproducible, missing-data-aware pipeline they can adapt to study links between cognition and outcomes. The long-term contribution is transparency: rather than hiding missingness or excluding incomplete cases, researchers make the missing-data decisions explicit and empirically test their influence.");
})();

// ============================================================ SLIDE 17 — COGDASH
(function(){
  const s = content("Translation", "CogDash — a transparent decision-support tool");
  fitImg(s, "dashboard_home.png", MX, 1.9, 6.5, 3.7, { rounding: false });
  fitImg(s, "dashboard_cluster_explorer.png", 7.0, 1.9, 5.6, 3.7);
  bullets(s, [
    "Cluster explorer · patient lookup · new-patient classifier · hypothesis summaries.",
    "Built in Streamlit — auditable inputs and visible confidence.",
    "Supports collaboration; it does not automate clinical decisions.",
  ], MX, 5.85, W-2*MX, { fontSize: 13.5, gap: 8 });
  notes(s, "To make this usable, I built CogDash, a Streamlit web app that turns the analysis into an interactive decision-support tool. It includes a cluster explorer, patient lookup, a new-patient classifier, hypothesis summaries, and advanced analytics. The design goal is auditability: clinicians can see what data feeds the model and when confidence is low. CogDash supports collaboration between clinicians and analysts — it is explicitly not meant to automate clinical decisions.");
})();

// ============================================================ SLIDE 18 — LIMITATIONS
(function(){
  const s = content("Caveats", "Limitations");
  const items = [
    ["Single site", "One rehabilitation centre — external replication is needed before generalising."],
    ["Limited longitudinal modelling", "Repeated assessments hint at recovery, but no full trajectory model is fit."],
    ["Imputation assumptions", "Rests on MAR; extreme-MNAR checks: Global Impairment robust, finer boundaries less so."],
    ["No functional outcomes", "Return-to-work or length-of-stay would be the strongest external validators."],
  ];
  const cw = (W-2*MX-0.5)/2, ch = 2.1;
  items.forEach((it,i)=>{
    const x = MX+(i%2)*(cw+0.5), y = 1.95+Math.floor(i/2)*(ch+0.35);
    panel(s, x, y, cw, ch);
    s.addShape(deck.ShapeType.rect, { x, y, w: 0.14, h: ch, fill: { color: T_NN } });
    s.addText(it[0], { x: x+0.35, y: y+0.25, w: cw-0.6, h: 0.5, fontFace: FONT, fontSize: 16.5, bold: true, color: INK });
    s.addText(it[1], { x: x+0.35, y: y+0.85, w: cw-0.65, h: 1.1, fontFace: FONT, fontSize: 13.5, color: BODY, lineSpacingMultiple: 1.22 });
  });
  notes(s, "Four limitations. First, single-site data — replication elsewhere is needed before treating this structure as general. Second, this is not a full longitudinal recovery model; repeated assessments offer hints, but modelling recovery directly needs a longitudinal design. Third, the imputation rests on a missing-at-random assumption; I can't rule out MNAR, though extreme-MNAR sensitivity checks suggest the Global Impairment tier is robust while finer boundaries are more vulnerable. Fourth, no functional outcomes like return-to-work or length-of-stay were available — those would be the strongest external validators for the tiers.");
})();

// ============================================================ SLIDE 19 — CONCLUSION
(function(){
  const s = content("In summary", "Three conclusions");
  const items = [
    ["Severity gradient", "Routine post-ABI neuropsychological data carry a strong cognitive-severity gradient — three ordered tiers, not discrete phenotypes.", T_AA],
    ["Imputation is modelling", "How missing data is handled is a substantive modelling choice that shapes the recovered structure.", ACCENT],
    ["Domain tiers are useful", "Domain-level severity tiers are clinically usable and numerically stable — preferable to raw-variable clustering.", T_GI],
  ];
  let y = 1.95; const ch = 1.45;
  items.forEach((it,i)=>{
    panel(s, MX, y, W-2*MX, ch);
    s.addText(String(i+1), { x: MX+0.25, y: y, w: 0.9, h: ch, align: "center", valign: "middle", fontFace: FONT, fontSize: 34, bold: true, color: it[2] });
    s.addText(it[0], { x: MX+1.3, y: y+0.22, w: 3.6, h: ch-0.4, valign: "middle", fontFace: FONT, fontSize: 17, bold: true, color: INK });
    s.addText(it[1], { x: MX+5.0, y: y+0.2, w: W-2*MX-5.3, h: ch-0.4, valign: "middle", fontFace: FONT, fontSize: 13.5, color: BODY, lineSpacingMultiple: 1.2 });
    y += ch+0.32;
  });
  notes(s, "Three conclusions. One: routine clinical neuropsychological data after ABI carry a strong cognitive-severity gradient, expressed as three ordered tiers rather than discrete phenotypes. Two: the choice of imputation strategy is a substantive modelling decision that influences the recovered structure — treating missing data as trivial preprocessing can change the answer. Three: domain-level severity tiers are clinically usable and numerically stable, preferable to raw-variable clustering for identifying distinctive patient groups. The thesis neither proves nor refutes discrete phenotypes; it supports an imputation-robust severity-stratification approach that is clinically interpretable and analytically testable.");
})();

// ============================================================ SLIDE 20 — THANK YOU
(function(){
  const s = deck.addSlide(); bg(s);
  s.addShape(deck.ShapeType.rect, { x: 0, y: 0, w: 0.28, h: H, fill: { color: ACCENT } });
  s.addText("THANK YOU", { x: 1.0, y: 2.3, w: 11, h: 0.5, fontFace: FONT, fontSize: 14, bold: true, color: ACCENT, charSpacing: 4 });
  s.addText("Questions & discussion", { x: 1.0, y: 2.8, w: 11.4, h: 1.0, fontFace: FONT, fontSize: 40, bold: true, color: INK });
  s.addText("A severity continuum after acquired brain injury — clinically useful, and more conservative than claiming discrete cognitive subtypes.",
    { x: 1.0, y: 4.0, w: 10.5, h: 0.9, fontFace: FONT, fontSize: 16, italic: true, color: BODY, lineSpacingMultiple: 1.2 });
  s.addShape(deck.ShapeType.line, { x: 1.0, y: 5.1, w: 5.5, h: 0, line: { color: RULE, width: 1.5 } });
  s.addText([
    { text: "Zoltan Kunos", options: { bold: true, color: INK, fontSize: 15 } },
    { text: "   ·   Supervisor: Dr. Alejandro García-Rudolph", options: { color: BODY, fontSize: 13 } },
    { text: "\nMSc Fundamental Principles of Data Science · Universitat de Barcelona", options: { color: MUTED, fontSize: 12 } },
  ], { x: 1.0, y: 5.3, w: 11, h: 1.0, fontFace: FONT, lineSpacingMultiple: 1.2 });
  notes(s, "Thank you for your attention. I'm happy to take questions — on the codebase and dashboard, on technical choices like the imputation and clustering design, or on implications for future rehabilitation-planning research. My overall hope is that this identified something clinically useful, more conservatively construed as a cognitive-severity continuum after acquired brain injury than as discrete cognitive subtypes.");
})();

deck.writeFile({ fileName: "/Users/zoltankunos/Desktop/thesis_project_clean/presentation/thesis_defense_severity_gradient.pptx" })
  .then(fn => console.log("WROTE", fn))
  .catch(e => { console.error(e); process.exit(1); });
