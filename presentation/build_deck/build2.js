const pptx = require("pptxgenjs");
const path = require("path");
const FIG = "/Users/zoltankunos/Desktop/thesis_project_clean/report/Figures";
const f = (n) => path.join(FIG, n);

// ---- Modern-minimal palette ----
const BG="FFFFFF", INK="1B2A30", BODY="3C4A52", MUTED="7C8A94", RULE="E3E9EC",
      PANEL="F5F8F9", ACCENT="11707A", T_AA="2E8B7F", T_NN="D49A4E", T_GI="C25B57";
const FONT="Arial", W=13.333, H=7.5, MX=0.7;

const deck = new pptx();
deck.defineLayout({ name:"W", width:W, height:H });
deck.layout="W";
deck.author="Zoltan Kunos";
deck.title="Data-Driven Cognitive Phenotyping in Acquired Brain Injury";

const RATIO = {
  "tsne_umap_clusters.png":5365/2060, "cognitive_radar_profiles.png":3411/1511,
  "feature_importance.png":4168/1851, "missingness_barplot.png":3569/1770,
  "missingness_heatmap.png":3874/2370, "h2_ari_nmi_heatmap.png":5007/2162,
  "h3_clinical_unit_heatmap.png":1400/1000, "h4_domain_vs_variable.png":2700/800,
  "dashboard_home.png":1920/945, "dashboard_cluster_explorer.png":1920/945,
};

let SNO = 0;
const SLIDES = [];
function newSlide(){ const s=deck.addSlide(); s.background={color:BG}; SNO++; SLIDES.push(s); return s; }
function header(s, kicker, title){
  s.addText(kicker.toUpperCase(),{x:MX,y:0.46,w:W-2*MX,h:0.3,fontFace:FONT,fontSize:11.5,bold:true,color:ACCENT,charSpacing:2});
  s.addText(title,{x:MX,y:0.74,w:W-2*MX,h:0.62,fontFace:FONT,fontSize:26,bold:true,color:INK});
  s.addShape(deck.ShapeType.rect,{x:MX,y:1.42,w:0.85,h:0.07,fill:{color:ACCENT}});
}
function footer(s, num){
  s.addShape(deck.ShapeType.line,{x:MX,y:6.98,w:W-2*MX,h:0,line:{color:RULE,width:1}});
  s.addText("Zoltan Kunos  ·  Data-Driven Cognitive Phenotyping in ABI",{x:MX,y:7.04,w:9,h:0.3,fontFace:FONT,fontSize:9,color:MUTED});
  if(num!==false) s.addText(String(SNO),{x:W-MX-1,y:7.04,w:1,h:0.3,align:"right",fontFace:FONT,fontSize:9,color:MUTED});
}
function content(kicker,title){ const s=newSlide(); header(s,kicker,title); footer(s); return s; }
function fitImg(s,name,bx,by,bw,bh,opts={}){
  const r=RATIO[name]; let w=bw,h=w/r; if(h>bh){h=bh;w=h*r;}
  const x=bx+(bw-w)/2,y=by+(bh-h)/2; s.addImage({path:f(name),x,y,w,h,...opts}); return {x,y,w,h};
}
const EQ = "/Users/zoltankunos/Desktop/thesis_project_clean/presentation/build_deck/eq/";
function eqImg(s,file,pw,ph,bx,by,bw,bh){
  const r=pw/ph; let w=bw,h=w/r; if(h>bh){h=bh;w=h*r;}
  const x=bx+(bw-w)/2,y=by+(bh-h)/2; s.addImage({path:EQ+file,x,y,w,h}); return {x,y,w,h};
}
function bullets(s,items,x,y,w,o={}){
  s.addText(items.map(it=>({text:it,options:{bullet:{code:"2022",indent:16},breakLine:true}})),
   {x,y,w,h:o.h||4.2,fontFace:FONT,fontSize:o.fontSize||15.5,color:o.color||BODY,lineSpacingMultiple:o.ls||1.22,paraSpaceAfter:o.gap!=null?o.gap:9,valign:"top"});
}
function panel(s,x,y,w,h,fill){ s.addShape(deck.ShapeType.roundRect,{x,y,w,h,rectRadius:0.08,fill:{color:fill||PANEL},line:{color:RULE,width:1}}); }
function stat(s,x,y,w,num,label,col){
  s.addText(num,{x,y,w,h:0.62,fontFace:FONT,fontSize:30,bold:true,color:col||ACCENT,align:"center"});
  s.addText(label,{x,y:y+0.62,w,h:0.5,fontFace:FONT,fontSize:11.5,color:MUTED,align:"center"});
}

// ===== 1 TITLE =====
(function(){ const s=newSlide();
  s.addShape(deck.ShapeType.rect,{x:0,y:0,w:0.28,h:H,fill:{color:ACCENT}});
  s.addText("MSC THESIS DEFENSE",{x:1.0,y:1.5,w:11,h:0.4,fontFace:FONT,fontSize:13,bold:true,color:ACCENT,charSpacing:3});
  s.addText("Data-Driven Cognitive Phenotyping\nin Acquired Brain Injury",{x:1.0,y:1.95,w:11.4,h:1.9,fontFace:FONT,fontSize:40,bold:true,color:INK,lineSpacingMultiple:1.04});
  s.addText("Do routine neuropsychological data reveal cognitive subtypes — or a single severity gradient?",{x:1.0,y:3.95,w:10.6,h:0.6,fontFace:FONT,fontSize:16,italic:true,color:BODY});
  s.addShape(deck.ShapeType.line,{x:1.0,y:4.85,w:5.5,h:0,line:{color:RULE,width:1.5}});
  s.addText([{text:"Zoltan Kunos",options:{bold:true,color:INK,fontSize:16}},
    {text:"\nMSc Fundamental Principles of Data Science · Universitat de Barcelona",options:{color:BODY,fontSize:13}},
    {text:"\nSupervisor: Dr. Alejandro García-Rudolph",options:{color:BODY,fontSize:13}}],
    {x:1.0,y:5.05,w:10,h:1.2,fontFace:FONT,lineSpacingMultiple:1.18});
  s.addText("14 June 2026",{x:W-MX-3,y:6.55,w:3,h:0.3,align:"right",fontFace:FONT,fontSize:11,color:MUTED});
})();

// ===== 2 ROADMAP =====
(function(){ const s=content("Overview","Roadmap");
  const items=[
    ["1","Clinical problem and research gap"],
    ["2","Cohort, missingness, and methods"],
    ["3","Four pre-registered hypothesis tests"],
    ["4","Interpretation and practical utility"],
    ["5","Limitations and conclusions"],
  ];
  let y=1.85; const rh=0.84;
  items.forEach(it=>{
    s.addShape(deck.ShapeType.roundRect,{x:MX,y,w:W-2*MX,h:rh,rectRadius:0.05,fill:{color:PANEL},line:{color:RULE,width:1}});
    s.addText(it[0],{x:MX+0.25,y,w:0.8,h:rh,align:"center",valign:"middle",fontFace:FONT,fontSize:26,bold:true,color:ACCENT});
    s.addText(it[1],{x:MX+1.3,y,w:W-2*MX-1.6,h:rh,valign:"middle",fontFace:FONT,fontSize:17,color:INK});
    y+=rh+0.16;
  });
})();

// ===== 3 CLINICAL PROBLEM =====
(function(){ const s=content("Why this matters","The clinical problem: heterogeneity");
  bullets(s,[
    "ABI can disrupt attention, memory, language, executive function, orientation and visuospatial cognition.",
    "Impairment does not follow the same pattern in every patient.",
    "Diagnosis and injury severity are useful categories — but they do not capture cognitive heterogeneity.",
    "Incomplete assessments are common, especially among more impaired patients.",
  ],MX,1.85,7.0,{fontSize:16,gap:13});
  panel(s,8.1,1.85,W-MX-8.1,4.7);
  s.addText("Research question",{x:8.4,y:2.15,w:4.2,h:0.4,fontFace:FONT,fontSize:15,bold:true,color:ACCENT});
  s.addText("Can data-driven clustering recover clinically meaningful cognitive organisation when missing data are handled explicitly — rather than ignored?",
    {x:8.4,y:2.6,w:4.3,h:2.0,fontFace:FONT,fontSize:16,italic:true,color:INK,lineSpacingMultiple:1.3});
})();

// ===== 4 RESEARCH GAP =====
(function(){ const s=content("Positioning","Research gap and contribution");
  const head=[
    {text:"Common limitation in prior work",options:{fill:{color:T_GI},color:"FFFFFF",bold:true}},
    {text:"This dissertation",options:{fill:{color:ACCENT},color:"FFFFFF",bold:true}},
  ];
  const rows=[
    ["Samples often below 200 participants","17,406 assessments · 7,285 patients"],
    ["Complete-case analysis","Ten imputation strategies compared"],
    ["Limited algorithmic sensitivity testing","Hyperparameter, seed and missingness checks"],
    ["Predetermined number of clusters","Density-based clustering (HDBSCAN)"],
    ["Limited clinical validation","Association with clinical-unit assignment"],
  ];
  const data=[head,...rows];
  s.addTable(data,{x:MX,y:1.95,w:W-2*MX,colW:[5.95,5.98],rowH:[0.6,0.82,0.82,0.82,0.82,0.82],
    fontFace:FONT,fontSize:14.5,color:BODY,valign:"middle",align:"left",
    border:{pt:1,color:RULE},fill:{color:"FFFFFF"},margin:[4,8,4,8]});
})();

// ===== 5 PRE-REGISTERED HYPOTHESES =====
(function(){ const s=content("Pre-registration","Four hypotheses, objective criteria");
  const rows=[
    ["H1","Are stable clusters recoverable?","Silhouette > 0.40, < 30% noise, ≥ 2 clusters"],
    ["H2","Robust to imputation choice?","Mean pairwise ARI > 0.50 (fixed-reference)"],
    ["H3","Are tiers clinically relevant?","χ² with clinical unit; Cramér's V > 0.10; adjust for diagnosis"],
    ["H4","Does domain aggregation help?","Better separation, lower VIF and condition number"],
  ];
  const y0=1.82,rh=1.12,cols=W-2*MX;
  rows.forEach((r,i)=>{ const y=y0+i*(rh+0.12);
    panel(s,MX,y,cols,rh);
    s.addShape(deck.ShapeType.roundRect,{x:MX+0.18,y:y+0.22,w:0.95,h:rh-0.44,rectRadius:0.06,fill:{color:ACCENT}});
    s.addText(r[0],{x:MX+0.18,y:y+0.22,w:0.95,h:rh-0.44,align:"center",valign:"middle",fontFace:FONT,fontSize:20,bold:true,color:"FFFFFF"});
    s.addText(r[1],{x:MX+1.4,y:y+0.13,w:5.0,h:rh-0.26,valign:"middle",fontFace:FONT,fontSize:15.5,bold:true,color:INK});
    s.addText(r[2],{x:MX+6.6,y:y+0.13,w:cols-6.8,h:rh-0.26,valign:"middle",fontFace:FONT,fontSize:12.5,color:BODY,lineSpacingMultiple:1.12});
  });
})();

// ===== 6 COHORT & MISSINGNESS =====
(function(){ const s=content("The data","A large but incomplete cohort");
  const sx=MX,sy=1.82,sw=(W-2*MX-1.2)/4;
  stat(s,sx+0*(sw+0.4),sy,sw,"17,406","assessments",ACCENT);
  stat(s,sx+1*(sw+0.4),sy,sw,"7,285","patients",ACCENT);
  stat(s,sx+2*(sw+0.4),sy,sw,"14","variables",ACCENT);
  stat(s,sx+3*(sw+0.4),sy,sw,"6","cognitive domains",ACCENT);
  fitImg(s,"missingness_barplot.png",MX,3.2,7.4,3.5);
  panel(s,8.4,3.2,W-MX-8.4,3.45);
  s.addText("53.1%",{x:8.6,y:3.4,w:3.8,h:0.7,fontFace:FONT,fontSize:34,bold:true,color:T_GI});
  s.addText("of rows are complete across all 14 variables",{x:8.6,y:4.1,w:3.9,h:0.6,fontFace:FONT,fontSize:13,color:BODY});
  bullets(s,[
    "Complete-case analysis would discard ≈ 47% of assessments.",
    "Missingness is non-random — it tracks the testing process.",
    "Imputation is needed to retain partially observed patients.",
  ],8.6,4.8,3.9,{fontSize:12.5,gap:9});
})();

// ===== 7 WHY IMPUTATION =====
(function(){ const s=content("Method rationale","Why imputation is necessary");
  fitImg(s,"missingness_heatmap.png",MX,1.78,6.7,5.0);
  s.addText("Missingness reflects the clinical testing process",{x:7.55,y:1.85,w:W-MX-7.55,h:0.8,fontFace:FONT,fontSize:15.5,bold:true,color:INK,lineSpacingMultiple:1.15});
  bullets(s,[
    "Fatigue or reduced motivation",
    "Cognitive overload or task aversion",
    "Disorientation or motor limitations",
    "Limited tolerance for long batteries",
    "Clinician selects a more suitable test",
  ],7.55,2.7,5.0,{fontSize:14,gap:9});
  s.addText("Dropping incomplete rows preferentially removes the most impaired patients — so missingness must be managed and tested, not hidden.",
    {x:7.55,y:5.6,w:5.05,h:1.0,fontFace:FONT,fontSize:12.5,italic:true,color:ACCENT,lineSpacingMultiple:1.18});
})();

// ===== 8 PIPELINE =====
(function(){ const s=content("Methods","Analysis pipeline");
  const steps=[
    ["Impute","10 strategies\nsimple → deep learning"],
    ["Scale","orient scores —\nhigher = better"],
    ["Aggregate","14 variables →\n6 domains"],
    ["UMAP","manifold\nembedding"],
    ["HDBSCAN","density clustering\n+ sensitivity"],
  ];
  const n=steps.length,gap=0.45,bw=(W-2*MX-(n-1)*gap)/n,by=2.15,bh=1.7;
  steps.forEach((st,i)=>{ const x=MX+i*(bw+gap);
    panel(s,x,by,bw,bh,"FFFFFF");
    s.addShape(deck.ShapeType.rect,{x,y:by,w:bw,h:0.12,fill:{color:ACCENT}});
    s.addText(st[0],{x,y:by+0.32,w:bw,h:0.5,align:"center",fontFace:FONT,fontSize:16,bold:true,color:INK});
    s.addText(st[1],{x:x+0.08,y:by+0.85,w:bw-0.16,h:0.75,align:"center",fontFace:FONT,fontSize:11,color:BODY,lineSpacingMultiple:1.1});
    if(i<n-1) s.addText("→",{x:x+bw,y:by,w:gap,h:bh,align:"center",valign:"middle",fontFace:FONT,fontSize:22,bold:true,color:ACCENT});
  });
  panel(s,MX,4.35,W-2*MX,2.05,PANEL);
  s.addText("Fixed-reference design (H2)",{x:MX+0.35,y:4.55,w:6,h:0.45,fontFace:FONT,fontSize:16,bold:true,color:ACCENT});
  s.addText("A single MICE solution anchors the scaler, UMAP embedding and HDBSCAN partition. Other imputations are projected through this fixed structure — testing whether imputed values land in the same place, not whether independently re-fit pipelines reproduce the hierarchy.",
    {x:MX+0.35,y:5.05,w:W-2*MX-0.7,h:1.2,fontFace:FONT,fontSize:14,color:BODY,lineSpacingMultiple:1.25});
})();

// ===== 9 UMAP =====
(function(){ const s=content("Methods · Dimensionality reduction","UMAP");
  s.addText("Uniform Manifold Approximation & Projection · McInnes, Healy & Melville, 2018",
    {x:MX,y:1.55,w:W-2*MX,h:0.3,fontFace:FONT,fontSize:12.5,italic:true,color:MUTED});
  // left rationale
  bullets(s,[
    "Builds a fuzzy k-NN graph of neighbourhood structure.",
    "Balances local and global geometry.",
    "Reduces dimensionality before density clustering.",
  ],MX,2.1,4.2,{fontSize:14,gap:14});
  panel(s,MX,4.65,4.2,1.85,"FDF6EC");
  s.addText("Caveat: separation in UMAP space can be optimistic — it must be backed by sensitivity analyses.",
    {x:MX+0.3,y:4.65,w:3.7,h:1.85,valign:"middle",fontFace:FONT,fontSize:12.5,italic:true,color:"8A6D2B",lineSpacingMultiple:1.18});
  // right: formal definition (LaTeX)
  s.addText("FORMAL DEFINITION",{x:5.3,y:1.95,w:7.3,h:0.3,fontFace:FONT,fontSize:10.5,bold:true,color:ACCENT,charSpacing:2});
  eqImg(s,"umap-1.png",901,501,5.3,2.25,W-MX-5.3,4.35);
})();

// ===== 10 HDBSCAN =====
(function(){ const s=content("Methods · Density clustering","HDBSCAN");
  s.addText("Hierarchical Density-Based Spatial Clustering of Applications with Noise · Campello, Moulavi & Sander, 2013",
    {x:MX,y:1.55,w:W-2*MX,h:0.3,fontFace:FONT,fontSize:12.5,italic:true,color:MUTED});
  bullets(s,[
    "Needs no predefined number of clusters.",
    "Finds regions dense across density levels.",
    "Labels uncertain points as noise, not forced.",
  ],MX,2.1,4.2,{fontSize:14,gap:14});
  panel(s,MX,4.65,4.2,1.85,PANEL);
  s.addText("The minimum cluster size is the main knob; everything else follows from the density hierarchy.",
    {x:MX+0.3,y:4.65,w:3.7,h:1.85,valign:"middle",fontFace:FONT,fontSize:12.5,italic:true,color:BODY,lineSpacingMultiple:1.18});
  s.addText("FORMAL DEFINITION",{x:5.3,y:1.95,w:7.3,h:0.3,fontFace:FONT,fontSize:10.5,bold:true,color:T_AA,charSpacing:2});
  eqImg(s,"hdbscan-1.png",1038,450,5.3,2.4,W-MX-5.3,4.0);
})();

// ===== 10 H1 RESULT =====
(function(){ const s=content("Result · H1","Three cognitive severity tiers emerge");
  fitImg(s,"tsne_umap_clusters.png",MX,1.9,7.6,4.7);
  const tiers=[["Above-Average","6,725","above cohort mean",T_AA],["Near-Normal","6,328","close to the average",T_NN],["Global Impairment","4,353","below cohort mean",T_GI]];
  let ty=1.95;
  tiers.forEach(t=>{
    s.addShape(deck.ShapeType.roundRect,{x:8.5,y:ty,w:W-MX-8.5,h:1.15,rectRadius:0.06,fill:{color:PANEL},line:{color:RULE,width:1}});
    s.addShape(deck.ShapeType.rect,{x:8.5,y:ty,w:0.13,h:1.15,fill:{color:t[3]}});
    s.addText(t[0],{x:8.75,y:ty+0.13,w:2.6,h:0.4,fontFace:FONT,fontSize:14.5,bold:true,color:INK});
    s.addText(t[2],{x:8.75,y:ty+0.55,w:2.6,h:0.5,fontFace:FONT,fontSize:11.5,color:BODY});
    s.addText(t[1],{x:11.3,y:ty+0.2,w:1.3,h:0.7,align:"right",valign:"middle",fontFace:FONT,fontSize:20,bold:true,color:t[3]});
    ty+=1.32;
  });
  s.addText("All 10 imputations cleared pre-registered thresholds · MICE reference silhouette ≈ 0.53 · k = 3.  Criteria met — but the tiers are not interpreted as natural kinds.",
    {x:MX,y:6.45,w:7.6,h:0.5,fontFace:FONT,fontSize:11.5,italic:true,color:MUTED,lineSpacingMultiple:1.12});
})();

// ===== 11 CONTINUUM EVIDENCE =====
(function(){ const s=content("Interpretation · H1","Continuum evidence: level, not shape");
  fitImg(s,"cognitive_radar_profiles.png",MX,1.85,7.3,4.7);
  panel(s,8.2,1.9,W-MX-8.2,4.5);
  s.addText("PC1",{x:8.45,y:2.1,w:3.9,h:0.5,fontFace:FONT,fontSize:16,bold:true,color:ACCENT});
  s.addText("≈ 56%",{x:8.45,y:2.5,w:3.9,h:0.7,fontFace:FONT,fontSize:34,bold:true,color:INK});
  s.addText("of variance — one dominant axis",{x:8.45,y:3.2,w:3.9,h:0.5,fontFace:FONT,fontSize:12.5,color:BODY});
  s.addShape(deck.ShapeType.line,{x:8.45,y:3.85,w:3.9,h:0,line:{color:RULE,width:1}});
  bullets(s,[
    "Radar profiles are roughly concentric.",
    "All domains move in the same direction.",
    "All domains load positively on PC1.",
    "Signal = global severity, not dissociation.",
  ],8.45,4.0,3.9,{fontSize:12.5,gap:8});
})();

// ===== 12 H2 RESULT =====
(function(){ const s=content("Result · H2","Robust across imputation methods");
  fitImg(s,"h2_ari_nmi_heatmap.png",MX,1.9,7.5,4.6);
  const sx=8.45,sw=W-MX-8.45;
  stat(s,sx,1.95,sw,"0.71","mean pairwise ARI   (95% CI 0.70–0.72)",ACCENT);
  s.addShape(deck.ShapeType.line,{x:sx,y:3.25,w:sw,h:0,line:{color:RULE,width:1}});
  const mini=[["44 / 45","method pairs survive Holm correction"],["> 86%","assessments with high-confidence consensus"]];
  let my=3.45; mini.forEach(m=>{
    s.addText(m[0],{x:sx,y:my,w:sw,h:0.5,fontFace:FONT,fontSize:24,bold:true,color:INK,align:"center"});
    s.addText(m[1],{x:sx,y:my+0.5,w:sw,h:0.45,fontFace:FONT,fontSize:11.5,color:MUTED,align:"center"}); my+=1.15;
  });
  s.addText("Scope: point assignments are robust under a fixed scaler, embedding and partition — not full invariance of independently re-fit pipelines.",
    {x:sx,y:5.85,w:sw,h:0.85,fontFace:FONT,fontSize:11,italic:true,color:MUTED,lineSpacingMultiple:1.15});
})();

// ===== 13 COMPLETE-CASE =====
(function(){ const s=content("Result · H2","Complete-case analysis changes the answer");
  const head=[{text:"",options:{fill:{color:"FFFFFF"}}},
    {text:"MICE reference",options:{fill:{color:ACCENT},color:"FFFFFF",bold:true,align:"center"}},
    {text:"Complete-case",options:{fill:{color:T_GI},color:"FFFFFF",bold:true,align:"center"}}];
  const data=[head,
    ["Assessments retained","100%","53.1%"],
    ["Tiers recovered","3","2"],
    ["Silhouette","≈ 0.53","≈ 0.26"],
    ["ARI vs. reference (shared rows)","—","≈ 0.63"]];
  s.addTable(data,{x:MX,y:1.95,w:7.6,colW:[3.4,2.1,2.1],rowH:[0.55,0.7,0.7,0.7,0.7],
    fontFace:FONT,fontSize:14,color:BODY,align:"center",valign:"middle",border:{pt:1,color:RULE},fill:{color:"FFFFFF"}});
  panel(s,8.5,1.95,W-MX-8.5,4.55);
  s.addText("Deleting cases is not a weaker version of the same analysis —",{x:8.75,y:2.2,w:3.85,h:0.9,fontFace:FONT,fontSize:15,bold:true,color:INK,lineSpacingMultiple:1.18});
  s.addText("it changes the partition.",{x:8.75,y:3.05,w:3.85,h:0.5,fontFace:FONT,fontSize:17,bold:true,color:T_GI});
  s.addShape(deck.ShapeType.line,{x:8.75,y:3.7,w:3.85,h:0,line:{color:RULE,width:1}});
  s.addText("The baseline collapses three tiers to two and halves the silhouette. How missing data is handled becomes part of the model's substantive output.",
    {x:8.75,y:3.85,w:3.85,h:2,fontFace:FONT,fontSize:13,color:BODY,lineSpacingMultiple:1.25});
})();

// ===== 14 H3 =====
(function(){ const s=content("Result · H3","Tiers track clinical unit assignment");
  fitImg(s,"h3_clinical_unit_heatmap.png",MX,1.9,6.6,4.7);
  const sx=7.7,sw=W-MX-7.7;
  s.addText([{text:"χ² = 911",options:{bold:true,fontSize:26,color:INK}},{text:"   p < 10⁻¹⁵⁶",options:{fontSize:15,color:BODY}}],
    {x:sx,y:1.95,w:sw,h:0.6,fontFace:FONT});
  stat(s,sx,2.75,sw,"0.16","Cramér's V  ( pre-registered threshold 0.10 )",ACCENT);
  s.addShape(deck.ShapeType.line,{x:sx,y:4.05,w:sw,h:0,line:{color:RULE,width:1}});
  bullets(s,[
    "Cochran–Mantel–Haenszel: holds after adjusting for diagnosis.",
    "Severity tier adds information beyond the diagnostic label.",
    "Informs rehabilitation routing — it does not dictate placement.",
  ],sx,4.2,sw,{fontSize:13.5,gap:12});
})();

// ===== 15 H4 =====
(function(){ const s=content("Result · H4","Domain aggregation is more stable");
  fitImg(s,"h4_domain_vs_variable.png",MX,1.85,W-2*MX,2.2);
  const metrics=[["Silhouette","0.47","0.48",T_AA],["Mean VIF","2.80","1.90",ACCENT],["Condition number","62","12",ACCENT]];
  const cw=(W-2*MX-0.8)/3;
  metrics.forEach((m,i)=>{ const x=MX+i*(cw+0.4),y=4.35;
    panel(s,x,y,cw,2.0);
    s.addText(m[0],{x:x+0.2,y:y+0.18,w:cw-0.4,h:0.4,fontFace:FONT,fontSize:14,bold:true,color:INK,align:"center"});
    s.addText([{text:m[1]+"  ",options:{color:MUTED,fontSize:17,strike:true}},{text:"→  ",options:{color:MUTED,fontSize:15}},{text:m[2],options:{color:m[3],fontSize:28,bold:true}}],
      {x:x+0.2,y:y+0.7,w:cw-0.4,h:0.8,align:"center",valign:"middle",fontFace:FONT});
    s.addText("variables → domains",{x:x+0.2,y:y+1.5,w:cw-0.4,h:0.35,fontFace:FONT,fontSize:10.5,color:MUTED,align:"center"});
  });
})();

// ===== 16 INTERPRETATION =====
(function(){ const s=content("What it means","A continuum, not a catalogue");
  const gy=2.0,gh=0.9,gx=MX,gw=W-2*MX,seg=gw/3;
  [[T_AA,"Above-Average"],[T_NN,"Near-Normal"],[T_GI,"Global Impairment"]].forEach((c,i)=>{
    s.addShape(deck.ShapeType.rect,{x:gx+i*seg,y:gy,w:seg,h:gh,fill:{color:c[0]}});
    s.addText(c[1],{x:gx+i*seg,y:gy,w:seg,h:gh,align:"center",valign:"middle",fontFace:FONT,fontSize:13,bold:true,color:"FFFFFF"});
  });
  s.addText("less impaired",{x:gx,y:gy+gh+0.05,w:3,h:0.3,fontFace:FONT,fontSize:10.5,color:MUTED});
  s.addText("more impaired",{x:gx+gw-3,y:gy+gh+0.05,w:3,h:0.3,align:"right",fontFace:FONT,fontSize:10.5,color:MUTED});
  bullets(s,[
    "Subtypes would imply qualitatively different cognitive profiles.",
    "A gradient implies differences lie mostly along one severity axis.",
    "The tiers are practical bands extracted from that continuum.",
    "Domain-specific dissociations may exist — but they don't dominate here.",
    "Poor scaling, redundant or non-cognitive features, or complete-case selection can fake subtype structure.",
  ],MX,3.55,W-2*MX,{fontSize:14.5,gap:11});
})();

// ===== 17 UTILITY =====
(function(){ const s=content("So what","Clinical and analytic utility");
  const cw=(W-2*MX-0.5)/2,y=1.95,ch=4.4;
  panel(s,MX,y,cw,ch); s.addShape(deck.ShapeType.rect,{x:MX,y,w:cw,h:0.14,fill:{color:ACCENT}});
  s.addText("Clinical users",{x:MX+0.3,y:y+0.3,w:cw-0.6,h:0.5,fontFace:FONT,fontSize:18,bold:true,color:INK});
  bullets(s,[
    "Shared vocabulary for rehabilitation intensity.",
    "Confidence scores for borderline assignments.",
    "Information alongside diagnosis and judgement.",
  ],MX+0.3,y+1.0,cw-0.6,{fontSize:14,gap:13});
  panel(s,MX+cw+0.5,y,cw,ch); s.addShape(deck.ShapeType.rect,{x:MX+cw+0.5,y,w:cw,h:0.14,fill:{color:T_AA}});
  s.addText("Analytic users",{x:MX+cw+0.8,y:y+0.3,w:cw-0.6,h:0.5,fontFace:FONT,fontSize:18,bold:true,color:INK});
  bullets(s,[
    "Reproducible missingness-aware pipeline.",
    "Explicit, testable imputation decisions.",
    "Adaptable for linking cognition to outcomes.",
  ],MX+cw+0.8,y+1.0,cw-0.6,{fontSize:14,gap:13});
  s.addText("Long-term contribution: make missing-data decisions explicit, then test their influence — rather than hiding them.",
    {x:MX,y:6.45,w:W-2*MX,h:0.5,fontFace:FONT,fontSize:12.5,italic:true,color:MUTED,align:"center"});
})();

// ===== 18 COGDASH =====
(function(){ const s=content("Translation","CogDash — a transparent decision-support tool");
  fitImg(s,"dashboard_home.png",MX,1.9,6.5,3.7);
  fitImg(s,"dashboard_cluster_explorer.png",7.0,1.9,5.6,3.7);
  bullets(s,[
    "Cluster explorer · patient lookup · new-patient classifier · hypothesis summaries.",
    "Built in Streamlit — auditable inputs and visible confidence.",
    "Supports collaboration; it does not automate clinical decisions.",
  ],MX,5.8,W-2*MX,{fontSize:13.5,gap:8});
})();

// ===== 19 LIMITATIONS =====
(function(){ const s=content("Caveats","Limitations");
  const items=[
    ["Single site","One rehabilitation centre — external replication is required."],
    ["Limited longitudinal modelling","Repeated assessments hint at recovery, but no full trajectory model."],
    ["Missing-data assumptions","MAR is a working assumption; MNAR cannot be excluded."],
    ["No functional outcomes","Return-to-work, length-of-stay and independence were unavailable."],
    ["Embedding-based validation","UMAP-space silhouette may overstate separation."],
    ["Pipeline sensitivity","Aggregation + density clustering may favour a general severity axis."],
  ];
  const cw=(W-2*MX-0.5)/2,ch=1.45;
  items.forEach((it,i)=>{ const x=MX+(i%2)*(cw+0.5),y=1.78+Math.floor(i/2)*(ch+0.25);
    panel(s,x,y,cw,ch); s.addShape(deck.ShapeType.rect,{x,y,w:0.14,h:ch,fill:{color:T_NN}});
    s.addText(it[0],{x:x+0.35,y:y+0.18,w:cw-0.6,h:0.45,fontFace:FONT,fontSize:15,bold:true,color:INK});
    s.addText(it[1],{x:x+0.35,y:y+0.62,w:cw-0.65,h:0.75,fontFace:FONT,fontSize:12.5,color:BODY,lineSpacingMultiple:1.18});
  });
})();

// ===== 20 CONCLUSIONS =====
(function(){ const s=content("In summary","Three conclusions");
  const items=[
    ["Empirical","Routine post-ABI neuropsychological data carry a strong cognitive-severity gradient — ordered tiers, not discrete phenotypes.",T_AA],
    ["Methodological","Imputation is a substantive modelling decision that can alter the recovered structure.",ACCENT],
    ["Practical","Domain-level severity tiers are interpretable and numerically stable — preferable to raw-variable clustering.",T_GI],
  ];
  let y=1.95; const ch=1.45;
  items.forEach((it,i)=>{
    panel(s,MX,y,W-2*MX,ch);
    s.addText(String(i+1),{x:MX+0.25,y,w:0.9,h:ch,align:"center",valign:"middle",fontFace:FONT,fontSize:34,bold:true,color:it[2]});
    s.addText(it[0],{x:MX+1.3,y:y+0.22,w:3.4,h:ch-0.4,valign:"middle",fontFace:FONT,fontSize:17,bold:true,color:INK});
    s.addText(it[1],{x:MX+4.8,y:y+0.2,w:W-2*MX-5.1,h:ch-0.4,valign:"middle",fontFace:FONT,fontSize:13,color:BODY,lineSpacingMultiple:1.18});
    y+=ch+0.32;
  });
  s.addText("→ An imputation-robust severity-stratification framework — not a strong claim of discrete cognitive phenotypes.",
    {x:MX,y:6.4,w:W-2*MX,h:0.5,fontFace:FONT,fontSize:13.5,italic:true,color:INK,align:"center"});
})();

// ===== 21 THANK YOU =====
(function(){ const s=newSlide();
  s.addShape(deck.ShapeType.rect,{x:0,y:0,w:0.28,h:H,fill:{color:ACCENT}});
  s.addText("THANK YOU",{x:1.0,y:2.3,w:11,h:0.5,fontFace:FONT,fontSize:14,bold:true,color:ACCENT,charSpacing:4});
  s.addText("Questions & discussion",{x:1.0,y:2.8,w:11.4,h:1.0,fontFace:FONT,fontSize:40,bold:true,color:INK});
  s.addText("A clinically useful severity continuum after acquired brain injury — more conservative than claiming discrete cognitive subtypes.",
    {x:1.0,y:4.0,w:10.5,h:0.9,fontFace:FONT,fontSize:16,italic:true,color:BODY,lineSpacingMultiple:1.2});
  s.addShape(deck.ShapeType.line,{x:1.0,y:5.1,w:5.5,h:0,line:{color:RULE,width:1.5}});
  s.addText([{text:"Zoltan Kunos",options:{bold:true,color:INK,fontSize:15}},
    {text:"   ·   Supervisor: Dr. Alejandro García-Rudolph",options:{color:BODY,fontSize:13}},
    {text:"\nMSc Fundamental Principles of Data Science · Universitat de Barcelona",options:{color:MUTED,fontSize:12}}],
    {x:1.0,y:5.3,w:11,h:1.0,fontFace:FONT,lineSpacingMultiple:1.2});
})();

// ===== APPENDIX DIVIDER =====
(function(){ const s=newSlide();
  s.addShape(deck.ShapeType.rect,{x:0,y:0,w:W,h:H,fill:{color:ACCENT}});
  s.addText("APPENDIX",{x:1.0,y:2.9,w:11,h:0.5,fontFace:FONT,fontSize:15,bold:true,color:"BfE0E2",charSpacing:4});
  s.addText("Backup slides for examiner questions",{x:1.0,y:3.4,w:11,h:0.9,fontFace:FONT,fontSize:34,bold:true,color:"FFFFFF"});
})();

// appendix content helper
function appendix(kicker,title){ const s=newSlide();
  s.addText(("Appendix · "+kicker).toUpperCase(),{x:MX,y:0.46,w:W-2*MX,h:0.3,fontFace:FONT,fontSize:11,bold:true,color:MUTED,charSpacing:2});
  s.addText(title,{x:MX,y:0.74,w:W-2*MX,h:0.62,fontFace:FONT,fontSize:24,bold:true,color:INK});
  s.addShape(deck.ShapeType.rect,{x:MX,y:1.42,w:0.85,h:0.07,fill:{color:MUTED}});
  footer(s); return s;
}

// ===== A: Ten imputation strategies =====
(function(){ const s=appendix("A","Ten imputation strategies");
  const left=["Mean imputation","Median imputation","Predictive mean matching","Expectation–maximization","MICE (reference)"];
  const right=["K-nearest neighbours","MissForest","SoftImpute","Non-negative matrix factorization","Deep generative approaches"];
  const cw=(W-2*MX-0.5)/2;
  panel(s,MX,1.85,cw,4.4); panel(s,MX+cw+0.5,1.85,cw,4.4);
  s.addText("Simple → model-based",{x:MX+0.3,y:2.05,w:cw-0.6,h:0.4,fontFace:FONT,fontSize:13,bold:true,color:ACCENT});
  s.addText("Donor / matrix / deep learning",{x:MX+cw+0.8,y:2.05,w:cw-0.6,h:0.4,fontFace:FONT,fontSize:13,bold:true,color:ACCENT});
  s.addText(left.map((t,i)=>({text:`${i+1}.  ${t}`,options:{breakLine:true}})),{x:MX+0.3,y:2.6,w:cw-0.6,h:3.4,fontFace:FONT,fontSize:15,color:BODY,lineSpacingMultiple:1.5});
  s.addText(right.map((t,i)=>({text:`${i+6}.  ${t}`,options:{breakLine:true}})),{x:MX+cw+0.8,y:2.6,w:cw-0.6,h:3.4,fontFace:FONT,fontSize:15,color:BODY,lineSpacingMultiple:1.5});
})();

// ===== B: H2 fixed-reference design =====
(function(){ const s=appendix("B","H2 fixed-reference design");
  bullets(s,[
    "Fit the reference scaler on MICE-imputed data.",
    "Fit one UMAP embedding from the MICE reference.",
    "Define the reference HDBSCAN partition.",
    "Transform each alternative imputed dataset through the frozen pipeline.",
    "Compare predicted labels using pairwise ARI.",
  ],MX,1.9,7.2,{fontSize:16,gap:14});
  panel(s,8.2,1.9,W-MX-8.2,4.4);
  s.addText("Tests",{x:8.45,y:2.15,w:4,h:0.4,fontFace:FONT,fontSize:14,bold:true,color:T_AA});
  s.addText("Robustness of point assignments to imputed values.",{x:8.45,y:2.55,w:4.1,h:1.0,fontFace:FONT,fontSize:14,color:BODY,lineSpacingMultiple:1.2});
  s.addShape(deck.ShapeType.line,{x:8.45,y:3.7,w:4.1,h:0,line:{color:RULE,width:1}});
  s.addText("Does not test",{x:8.45,y:3.9,w:4,h:0.4,fontFace:FONT,fontSize:14,bold:true,color:T_GI});
  s.addText("Full invariance of independently discovered structures.",{x:8.45,y:4.3,w:4.1,h:1.0,fontFace:FONT,fontSize:14,color:BODY,lineSpacingMultiple:1.2});
})();

// ===== C: HDBSCAN logic =====
(function(){ const s=appendix("C","HDBSCAN logic");
  bullets(s,[
    "Estimate local density via core distance.",
    "Construct mutual-reachability distances.",
    "Build a minimum spanning tree.",
    "Extract a hierarchy of density-connected components.",
    "Select persistent clusters by stability.",
    "Label points outside persistent regions as noise.",
  ],MX,1.9,7.2,{fontSize:16,gap:12});
  panel(s,8.2,1.9,W-MX-8.2,4.4,"FDF6EC");
  s.addText("Unlike DBSCAN, HDBSCAN does not reduce to a single fixed-ε DBSCAN solution — it integrates across density levels.",
    {x:8.45,y:2.2,w:4.1,h:3.0,fontFace:FONT,fontSize:14.5,italic:true,color:"8A6D2B",lineSpacingMultiple:1.3});
})();

// ===== D: Silhouette caveats =====
(function(){ const s=appendix("D","Silhouette caveats");
  bullets(s,[
    "UMAP is designed to emphasise neighbourhood structure.",
    "Silhouette measured in embedded space can overstate separation.",
    "Hyperparameter and seed selection make the chosen estimate optimistic.",
    "Seed stability, PCA and alternative representations provide supporting evidence.",
  ],MX,1.9,W-2*MX,{fontSize:16,gap:14});
  panel(s,MX,5.4,W-2*MX,1.1,PANEL);
  s.addText("Interpret silhouette as an internal pipeline-quality metric — not proof of natural categories.",
    {x:MX+0.35,y:5.4,w:W-2*MX-0.7,h:1.1,valign:"middle",fontFace:FONT,fontSize:15,bold:true,color:ACCENT,lineSpacingMultiple:1.15});
})();

// ===== E: MNAR sensitivity =====
(function(){ const s=appendix("E","Missing-not-at-random sensitivity");
  bullets(s,[
    "MAR was the principal working assumption.",
    "MNAR mechanisms cannot be ruled out from observed values alone.",
    "Extreme-MNAR analyses suggest Global Impairment is comparatively robust.",
    "Boundaries between the less-impaired tiers are more sensitive.",
  ],MX,1.95,W-2*MX,{fontSize:16,gap:16});
})();

// ===== F: clinical interpretation boundary =====
(function(){ const s=appendix("F","Clinical interpretation boundary");
  const cw=(W-2*MX-0.5)/2,y=1.85,ch=4.4;
  panel(s,MX,y,cw,ch); s.addShape(deck.ShapeType.rect,{x:MX,y,w:cw,h:0.14,fill:{color:T_AA}});
  s.addText("The severity tier DOES",{x:MX+0.3,y:y+0.28,w:cw-0.6,h:0.5,fontFace:FONT,fontSize:16,bold:true,color:INK});
  bullets(s,["supplement diagnosis;","support rehabilitation discussion;","carry a confidence estimate;","assist outcome modelling."],MX+0.3,y+0.95,cw-0.6,{fontSize:14.5,gap:14});
  panel(s,MX+cw+0.5,y,cw,ch); s.addShape(deck.ShapeType.rect,{x:MX+cw+0.5,y,w:cw,h:0.14,fill:{color:T_GI}});
  s.addText("The severity tier does NOT",{x:MX+cw+0.8,y:y+0.28,w:cw-0.6,h:0.5,fontFace:FONT,fontSize:16,bold:true,color:INK});
  bullets(s,["diagnose a patient;","prescribe treatment;","determine clinical placement;","replace professional judgement."],MX+cw+0.8,y+0.95,cw-0.6,{fontSize:14.5,gap:14});
})();

// ===== G: future work =====
(function(){ const s=appendix("G","Future work");
  bullets(s,[
    "External replication across rehabilitation centres.",
    "Direct longitudinal modelling of recovery trajectories.",
    "Validation against return-to-work, length-of-stay and independence.",
    "Alternative model-based phenotyping (e.g. latent profile analysis).",
    "Prospective evaluation of CogDash in clinical workflows.",
    "Greater sensitivity to domain-specific dissociations.",
  ],MX,1.9,W-2*MX,{fontSize:16,gap:13});
})();

// ===== APPENDIX H: METRIC INTERPRETATION =====
(function(){ const s=appendix("H","How to read the metrics");
  function block(x,y,w,name,meaning,reading,col){
    s.addText(name,{x,y,w,h:0.32,fontFace:FONT,fontSize:13.5,bold:true,color:INK});
    s.addText(meaning,{x,y:y+0.31,w,h:0.46,fontFace:FONT,fontSize:11,color:BODY,lineSpacingMultiple:1.1});
    s.addText(reading,{x,y:y+0.77,w,h:0.3,fontFace:FONT,fontSize:11,bold:true,color:col||ACCENT});
  }
  const cw=(W-2*MX-0.5)/2, py=1.7, ph=5.05, bh=1.08;
  panel(s,MX,py,cw,ph); s.addShape(deck.ShapeType.rect,{x:MX,y:py,w:cw,h:0.12,fill:{color:ACCENT}});
  s.addText("Clustering quality & robustness",{x:MX+0.3,y:py+0.22,w:cw-0.6,h:0.35,fontFace:FONT,fontSize:13,bold:true,color:ACCENT});
  let y=py+0.7;
  block(MX+0.3,y,cw-0.6,"Silhouette","Cohesion vs. separation — how well a point fits its own tier vs. the nearest other.","−1 to 1; higher = cleaner.  Pre-reg > 0.40 · observed ≈ 0.53",ACCENT); y+=bh;
  block(MX+0.3,y,cw-0.6,"Adjusted Rand Index (ARI)","Agreement between two partitions, corrected for chance.","0 = chance, 1 = identical.  Pre-reg > 0.50 · observed ≈ 0.71",ACCENT); y+=bh;
  block(MX+0.3,y,cw-0.6,"Normalised Mutual Information","Shared information between two partitions, scaled 0–1.","0 = independent, 1 = identical · corroborates ARI",ACCENT); y+=bh;
  block(MX+0.3,y,cw-0.6,"Consensus confidence","Share of assessments given a stable label across imputations.","> 86% high-confidence across methods",ACCENT);

  const rx=MX+cw+0.5;
  panel(s,rx,py,cw,ph); s.addShape(deck.ShapeType.rect,{x:rx,y:py,w:cw,h:0.12,fill:{color:T_AA}});
  s.addText("Association & conditioning",{x:rx+0.3,y:py+0.22,w:cw-0.6,h:0.35,fontFace:FONT,fontSize:13,bold:true,color:T_AA});
  y=py+0.7;
  block(rx+0.3,y,cw-0.6,"χ² statistic","Evidence that tier and clinical unit are associated — significance, not effect size; grows with N.","χ² = 911 · p < 10⁻¹⁵⁶",INK); y+=bh;
  block(rx+0.3,y,cw-0.6,"Cramér's V","Effect size of that association, scaled 0–1.","0.1 small · 0.3 medium · 0.5 large.  Pre-reg > 0.10 · observed 0.16",INK); y+=bh;
  block(rx+0.3,y,cw-0.6,"VIF (variance inflation factor)","Per-feature redundancy from collinearity.","1 = none; > 5–10 concerning.  2.80 → 1.90",INK); y+=bh;
  block(rx+0.3,y,cw-0.6,"Condition number","Global conditioning of the feature set (λmax / λmin of the correlation matrix).","< 10 fine · 10–30 moderate · > 30 strong.  62 → 12",INK);
})();

// ===== SPEAKER NOTES (one per slide, index-aligned) =====
const NOTES = [
// 1 Title
"Good morning, and thank you for being here. The title of my dissertation is Data-Driven Cognitive Phenotyping in Acquired Brain Injury. The question behind it is simple to state: after a brain injury, two patients can carry the same diagnosis and still need very different rehabilitation. So I asked — do routinely collected neuropsychological data contain a consistent cognitive structure, and if they do, is it a set of distinct subtypes or something else? The answer I'll defend is that the structure is real, but it is not a catalogue of subtypes. It is a cognitive severity gradient, which clustering divides into three usable tiers.",
// 2 Roadmap
"Here is the path. I'll start with the clinical problem, because the clinical problem is what creates the research question. Then the cohort and the missingness, because the missingness is what creates the methodological problem. Then the pipeline and the four pre-registered tests. Then the results, their interpretation, and their practical utility — and I'll close with limitations and conclusions. There's an appendix of backup slides if you want to go deeper in questions.",
// 3 Clinical Problem
"Start with the clinic. Acquired brain injury can disrupt attention, memory, language, executive function, orientation and visuospatial cognition — and it does not do so in the same way in any two patients. That is the core fact: impairment after ABI is heterogeneous. Clinicians manage that with broad categories — diagnosis, injury severity — which describe the scope of the problem, not the individual profile or its degree. Two patients who both 'have memory problems' can need completely different programmes. So the question writes itself: can a data-driven method recover a cognitive organisation that is actually meaningful — and can we trust it when missing data are handled honestly rather than ignored?",
// 4 Research Gap
"Where does this sit relative to prior work? Earlier cognitive-phenotyping studies tend to share a set of limitations: small samples, often under two hundred; reliance on complete-case analysis; little algorithmic stress-testing; a number of clusters fixed in advance; and seldom any clinical validation. This dissertation pushes on each. It works at scale — over seventeen thousand assessments. It compares ten imputation strategies instead of deleting incomplete rows. It runs hyperparameter, seed and missingness sensitivity checks. It uses density-based clustering that does not fix the number of clusters in advance. And it validates against clinical-unit assignment. Those five moves are the contribution.",
// 5 Pre-registered Hypotheses
"To keep myself honest, I pre-registered four hypotheses, each with an objective threshold. H1: are stable clusters even recoverable — silhouette above 0.40, under thirty percent noise, at least two clusters. H2: are the assignments robust to which imputation I choose — mean pairwise adjusted Rand index above 0.50, under a fixed-reference design. H3: are the tiers clinically relevant — a chi-square association with clinical unit, Cramér's V above 0.10, holding up after adjusting for diagnosis. H4: does aggregating variables into domains help — better separation and better conditioning. The point is that every claim I make today had a number it must clear, set before I saw the result.",
// 6 Cohort & Missingness
"Now the data. After filtering and removing assessments with no cognitive testing at all, I have 17,406 assessments from 7,285 patients, across 14 variables that map onto 6 cognitive domains. That's a large, real, routine clinical database — which is exactly why it's messy. Here is the number that drove the whole methodology: only 53.1 percent of rows are complete across all fourteen variables, so a complete-case analysis would throw away nearly 47 percent of the data. And the key move: that missingness is not random. It's concentrated in the long, demanding tests, and it tracks the testing process. If I just delete it, I don't get a cleaner version of the same cohort — I get a different cohort.",
// 7 Why Imputation
"Why is the missingness structured? Because a missing value here usually means something clinical: fatigue or low motivation, cognitive overload or task aversion, disorientation or a motor limitation, simple intolerance of a long battery, or a clinician judging a different test more appropriate. Notice what those share: they correlate with impairment. So when you drop incomplete rows you don't remove a random sample — you preferentially remove the most impaired patients, the very people rehabilitation is built around. That's why missingness has to be managed and tested, not hidden — and why the pipeline includes a way to check whether the imputation choice changes the answer.",
// 8 Pipeline
"Here is the pipeline. I impute with ten strategies, from simple mean and median, through model- and donor-based methods, matrix completion, and deep learning. I standardise and orient the scores so higher always means better. I aggregate the fourteen variables into the six domains, embed with UMAP, and cluster with HDBSCAN, with sensitivity analyses around the whole thing. The part to hold onto is the fixed-reference design, because it's how H2 is tested: I take one solution from MICE and freeze it — scaler, embedding and partition all become a fixed reference — then push every other imputation's values through that frozen structure. That asks whether the imputed values land in the same place under a fixed structure. It deliberately does not ask whether re-fitting the whole pipeline reproduces the hierarchy.",
// 9 UMAP
"First method: UMAP, for dimensionality reduction. Intuitively it builds a fuzzy k-nearest-neighbour graph that captures neighbourhood structure, balances local and global geometry, and gives the clustering step a clean low-dimensional space. Formally — the equations on the right — the directed membership of edge i-to-j decays exponentially with distance, normalised by a local scale sigma chosen so each point's memberships sum to log-base-two of k, and shifted by rho, the nearest-neighbour distance. Those directed memberships are symmetrised by a probabilistic t-conorm to give p-i-j. In the low-dimensional space a Student-t-like kernel defines q-i-j, and UMAP minimises the fuzzy-set cross-entropy between p and q by stochastic gradient descent. The caveat I keep on the slide: separation in UMAP space can look better than it is, so I back it with sensitivity analyses.",
// 10 HDBSCAN
"Second method: HDBSCAN, for clustering. The reason it fits my argument is that it needs no predefined number of clusters, it finds regions that stay dense across density levels, and it labels uncertain points as noise rather than forcing them into a group. Formally, it starts from the core distance — the distance to the k-th nearest neighbour — and the mutual-reachability distance, the maximum of the two core distances and the raw distance. It builds a minimum spanning tree of that metric, condenses the hierarchy using a minimum cluster size, and selects the set of non-nested clusters that maximises total stability, where stability sums the one-over-distance lifetimes of points within a cluster. Anything outside the selected clusters is labelled noise. The minimum cluster size is really the only knob.",
// 10 H1
"Here is the first result. The pipeline recovers three tiers: Above-Average — 6,725 assessments scoring above the cohort mean; Near-Normal — 6,328 close to the average; and Global Impairment — 4,353 below the mean. All ten imputation methods cleared the pre-registered H1 thresholds, and in the MICE reference the silhouette was about 0.53 with three tiers. So stable clusters exist. But notice the labels already tell a story — Above-Average, Near-Normal, Global Impairment. Those aren't three different kinds of cognition; they're three levels. I'm flagging that deliberately, because the next slides argue these tiers are bands cut from a continuum, not natural kinds.",
// 11 Continuum Evidence
"This is the conceptual heart of the thesis. If these were genuine subtypes, the tiers would have different shapes — strong here, weak there. They don't. The radar profiles on the left are roughly concentric: the tiers differ in overall size, not in shape, and every domain moves in the same direction together. The PCA on the right confirms it — the first principal component alone explains nearly 56 percent of the variance, and every domain loads positively on it. That is the signature of a single dominant axis: overall cognitive severity. So the dominant signal is global severity, not a symptom-specific dissociation. The three tiers discretize a continuum; they are not a catalogue of phenotypes.",
// 12 H2
"Back to the missingness, because a structure is only worth interpreting if it isn't an artefact of one preprocessing choice — this is H2. Across the imputation methods the mean pairwise adjusted Rand index is 0.71, with a bootstrap 95 percent confidence interval of 0.70 to 0.72. Of the 45 method-pair comparisons, 44 survived Holm correction; the single exception was KNN versus SoftImpute, just under threshold. And more than 86 percent of assessments received high-confidence consensus labels. So the tiers are not a quirk of how I filled the gaps. I'll state the scope precisely: this shows point assignments are robust under a fixed scaler, embedding and partition — not that independently re-fit pipelines reproduce identical density hierarchies.",
// 13 Complete-case
"Here is why the imputation wasn't optional. Suppose I'd done what most studies do and used only complete cases. I keep 53.1 percent of the data — and I get a different result. The complete-case baseline recovers two clusters, not three. Its silhouette drops to about 0.26, roughly half of the 0.53 from the MICE reference. And even on the assessments the two analyses share, the agreement is only about 0.63. So deleting incomplete cases is not a weaker version of the same analysis — it changes the partition. That's the methodological thesis in one slide: how you handle missing data isn't preprocessing hygiene, it's part of the model's substantive output.",
// 14 H3
"A structure can be robust and still be clinically useless, so H3 asks whether the tiers connect to anything real — specifically, which clinical unit a patient is assigned to. They do. The chi-square statistic is 911, p below ten-to-the-minus-156, Cramér's V 0.16 — above my pre-registered 0.10. And importantly, I checked whether this is just diagnosis in disguise: a Cochran–Mantel–Haenszel test shows the association survives adjustment for diagnosis. So the severity tier carries information beyond the diagnostic label. Let me be careful: I'm not saying tier should determine placement. I'm saying it's informative about routing — it adds something, on top of diagnosis, to a conversation about rehabilitation intensity.",
// 15 H4
"The last hypothesis is housekeeping with real consequences. H4 asks whether aggregating the fourteen variables into six domains was right, versus clustering raw variables. It was, on two fronts. Separation is marginally better — silhouette 0.48 versus 0.47. But the bigger win is numerical stability: mean variance inflation factor drops from about 2.80 to 1.90, and the condition number from about 62 to 12. That matters because UMAP and HDBSCAN are distance-based, and distance-based methods are fragile when features are redundant and highly correlated. Aggregating into clinically meaningful domains removes that redundancy while keeping interpretable constructs. So domains win on stability and on interpretability.",
// 16 Interpretation
"Let me pull the interpretation together, because the distinction is the whole point. A subtype account says patients differ qualitatively — different profiles, different kinds. A gradient account says they differ mostly along one shared axis of severity, and the tiers are practical bands cut from that axis. Everything points to the gradient: concentric profiles, over half the variance on PC1, all-positive loadings, tiers behaving like ordered bands. I'm not claiming domain-specific dissociations never exist — they can. I'm claiming that in this dataset, with an imputation-robust domain-level pipeline, overall severity dominates. And a warning is embedded here: poor scaling, redundant or non-cognitive features, or complete-case selection can all manufacture patterns that look like subtypes but aren't.",
// 17 Utility
"So what is this good for? Two audiences. For clinical users, the tiers offer a shared vocabulary for discussing rehabilitation intensity, a confidence score for the borderline cases, and a piece of information that sits alongside diagnosis and clinical judgement — not above it. For analytic users, the contribution is the pipeline itself: reproducible, missingness-aware, with the imputation decisions made explicit and testable, adaptable to studying how cognition links to outcomes. And the long-term point is cultural: rather than hiding missingness or quietly deleting incomplete cases, you make the decision visible and measure its influence.",
// 18 CogDash
"To make this usable rather than just publishable, I built CogDash — a Streamlit application that turns the analysis into an interactive tool, with a cluster explorer, a patient lookup, a new-patient classifier, and summaries of the hypothesis tests. The design principle is auditability: a clinician can see what data feed the model and can see when its confidence is low. That's deliberate — CogDash is built to support a conversation between clinicians and analysts, not to automate a clinical decision.",
// 19 Limitations
"I want to be the first to state the limits. The data are single-site, so external replication is needed before anyone treats this as general. It is not a full longitudinal recovery model — repeated assessments only hint at trajectories. The imputation rests on a missing-at-random working assumption; I can't rule out MNAR from observed values alone, though my extreme-MNAR checks suggest Global Impairment is robust while the finer boundaries are more fragile. I had no functional outcomes — return-to-work, length-of-stay, independence — which would be the strongest validators. Some validation is embedding-based, and UMAP-space silhouette can flatter separation. And the pipeline itself may bias toward a general severity axis. I think the convergent evidence holds — but those are the honest caveats.",
// 20 Conclusions
"Three conclusions. Empirically, routine post-ABI neuropsychological data carry a strong cognitive-severity gradient — three ordered tiers, not discrete phenotypes. Methodologically, imputation is a modelling decision, not preprocessing: treat missing data as trivial and you can change the answer, as the complete-case comparison showed. Practically, domain-level severity tiers are interpretable and numerically stable, preferable to raw-variable clustering. Taken together, the dissertation doesn't prove, and doesn't need to prove, that discrete phenotypes exist. It supports something more conservative and more useful: an imputation-robust severity-stratification framework that can be interpreted clinically and tested analytically.",
// 21 Thank You
"Thank you for your attention. I'm glad to take questions — on the codebase and the dashboard, on the technical choices behind the imputation and clustering, or on what this might mean for rehabilitation-planning research. And if it's useful, I have backup slides on the imputation set, the fixed-reference design, HDBSCAN, the silhouette caveats, the MNAR analysis, and the clinical boundary. My hope is simply that this found something genuinely useful — best understood, conservatively, as a cognitive-severity continuum after acquired brain injury rather than as a set of discrete subtypes.",
// 22 Appendix divider
"Backup slides follow, prepared for detailed examiner questions on the imputation set, the fixed-reference design, HDBSCAN, silhouette caveats, MNAR sensitivity, the clinical interpretation boundary, and future work.",
// 23 A Ten imputation strategies
"The ten span simple methods — mean, median — model-based methods like predictive mean matching, EM and MICE which is my reference, donor and tree methods like KNN and MissForest, matrix-completion methods like SoftImpute and non-negative matrix factorization, and deep generative approaches. The spread is the point: agreement across that range is what makes the result credible.",
// 24 B H2 fixed-reference design
"Five steps: fit the scaler on MICE-imputed data; fit one UMAP embedding from that reference; define the reference HDBSCAN partition; transform every alternative imputed dataset through that frozen pipeline; and compare predicted labels with pairwise ARI. This tests robustness of point assignments to the imputed values. It does not test full invariance of independently discovered structures — an important scope boundary I'm careful to state.",
// 25 C HDBSCAN logic
"HDBSCAN estimates local density via core distance, builds mutual-reachability distances, constructs a minimum spanning tree, extracts a hierarchy of density-connected components, selects persistent clusters by stability, and labels points outside persistent regions as noise. Unlike DBSCAN it does not reduce to a single fixed-epsilon solution — it integrates across density levels, which is why it can recover clusters of varying density without a preset count.",
// 26 D Silhouette caveats
"A caveat on silhouette. UMAP is designed to emphasise neighbourhood structure, so a silhouette measured in embedded space can overstate separation. Hyperparameter and seed selection also bias the chosen estimate optimistically. That's why I lean on seed stability, PCA and alternative representations as supporting evidence. Silhouette should be read as an internal pipeline-quality metric, not proof of natural categories.",
// 27 E MNAR sensitivity
"On missing-not-at-random. MAR was my principal working assumption, and MNAR cannot be ruled out from observed values alone. Extreme-MNAR sensitivity analyses suggest the Global Impairment tier is comparatively robust, while the boundaries between the less-impaired tiers are more sensitive. So the coarse severity signal is more trustworthy than the fine boundaries under adversarial missingness assumptions.",
// 28 F Clinical interpretation boundary
"This makes the clinical boundary explicit. The severity tier can supplement diagnosis, support rehabilitation discussion, carry a confidence estimate, and assist outcome modelling. It does not diagnose a patient, prescribe treatment, determine clinical placement, or replace professional judgement. I keep this slide ready because it's the question I most expect about responsible use.",
// 29 G Future work
"Future work: external replication across rehabilitation centres; direct longitudinal modelling of recovery trajectories; validation against functional outcomes like return-to-work, length-of-stay and independence; alternative model-based phenotyping such as latent profile analysis; prospective evaluation of CogDash in clinical workflows; and methods with greater sensitivity to domain-specific dissociations.",
// 30 H Metric interpretation
"A quick reading guide for the metrics, in case you want to interrogate any number. Silhouette measures cohesion versus separation, between minus one and one — I pre-registered above 0.40 and observed about 0.53. ARI measures agreement between two partitions corrected for chance — pre-registered above 0.50, observed about 0.71 — and NMI corroborates it. Consensus confidence is the share of assessments with a stable label across imputations, over 86 percent. On the right: the chi-square statistic shows the association is significant but it scales with sample size, so it's not an effect size; Cramér's V is the effect size, where 0.1 is small and I observed 0.16 against a 0.10 threshold. VIF is per-feature collinearity, where 1 is ideal and above 5 to 10 is concerning, dropping from 2.80 to 1.90. The condition number is the global conditioning of the feature set — the ratio of largest to smallest eigenvalue of the correlation matrix — where under 10 is fine and over 30 is strong collinearity, dropping from 62 to 12.",
];
SLIDES.forEach((s,i)=>{ if(NOTES[i]) s.addNotes(NOTES[i]); });

deck.writeFile({ fileName:"/Users/zoltankunos/Desktop/thesis_project_clean/presentation/thesis_defense_severity_gradient.pptx" })
  .then(fn=>console.log("WROTE",fn,"slides:",SNO,"notes:",NOTES.length)).catch(e=>{console.error(e);process.exit(1);});
