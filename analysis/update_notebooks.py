"""Idempotently share preprocessing and add reproducible stage notebooks."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


def patch_legacy():
    path=ROOT/'notebooks/5_Improved_Clustering_Infrastructure.ipynb'
    nb=json.loads(path.read_text(encoding='utf-8'))
    for cell in nb['cells']:
        source=''.join(cell['source'])
        if 'def compute_domain_scores(' in source:
            start=source.index('# Tests where')
            stop=source.index('# Compute reliability weights:')
            source=source[:start]+('from pathlib import Path\nimport sys\n'
                "_project = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\n"
                'if str(_project) not in sys.path: sys.path.insert(0, str(_project))\n'
                'from analysis.preprocessing import compute_domain_scores\n\n')+source[stop:]
            source=source.replace('Compute reliability weights: inverse of missingness rate per variable','Compute administration-frequency weights (not psychometric reliability)')
            source=source.replace('Variables with lower missingness are more reliable and get higher weight','More frequently administered variables receive greater weight')
            cell['source']=source.splitlines(keepends=True)
    for cell in nb['cells']:
        if cell['cell_type']=='code':cell['outputs']=[];cell['execution_count']=None
    path.write_text(json.dumps(nb,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
    path=ROOT/'notebooks/14_Backlog_Additions.ipynb'
    nb=json.loads(path.read_text(encoding='utf-8'))
    for cell in nb['cells']:
        source=''.join(cell['source'])
        if 'def run_pipeline(' in source:
            source=re.sub(r'    dom_cols = list\(DOMAINS.keys\(\)\).*?    dom_std = StandardScaler\(\).fit_transform\(dom\)',
                "    from analysis.preprocessing import compute_domain_scores\n"
                "    completed = pd.DataFrame(imputed_matrix, columns=ELIGIBLE_VARS)\n"
                "    weights = (1.0 - df_el[ELIGIBLE_VARS].isna().mean()).to_dict()\n"
                "    dom = compute_domain_scores(completed, DOMAINS, weights=weights)\n"
                "    dom_std = StandardScaler().fit_transform(dom)",source,flags=re.S)
        if 'A-5: Listwise-deletion baseline' in source:
            source=re.sub(r'dom_cols = list\(DOMAINS.keys\(\)\).*?dom_cc_std = StandardScaler\(\).fit_transform\(dom_cc\)',
                "from analysis.preprocessing import compute_domain_scores\n"
                "weights = (1.0 - df_el[ELIGIBLE_VARS].isna().mean()).to_dict()\n"
                "dom_cc = compute_domain_scores(pd.DataFrame(cc_data, columns=ELIGIBLE_VARS), DOMAINS, weights=weights)\n"
                "dom_cc_std = StandardScaler().fit_transform(dom_cc)",source,flags=re.S)
        if 'ROOT = Path.cwd()' in source and 'sys.path.insert' not in source:
            source=source.replace('RESULTS = ROOT / "results"','if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))\nRESULTS = ROOT / "results"')
        cell['source']=source.splitlines(keepends=True)
        if cell['cell_type']=='code':cell['outputs']=[];cell['execution_count']=None
    note='\n\nPreprocessing corrected on 15 October 2026: the MI and complete-case branches now share NB5\'s domain construction. Historical executed notebooks/results predate this correction. New patient-level results are in `results/research_2026/`.\n'
    if 'Preprocessing corrected on' not in ''.join(nb['cells'][0]['source']):nb['cells'][0]['source'].append(note)
    path.write_text(json.dumps(nb,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')


def make_notebook(number,title,stages):
    cells=[dict(cell_type='markdown',metadata={},source=[f'# NB{number}: {title}\n',
        'Run from the project research environment. Scripts are the source of truth; artifacts are saved separately under `results/research_2026/`.\n'])]
    setup="from pathlib import Path\nimport subprocess, sys\nROOT = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\n"
    for stage in stages:
        code=setup+f"subprocess.run([sys.executable, '-m', 'analysis.run_research', '--stage', '{stage}'], cwd=ROOT, check=True)\n"
        cells.append(dict(cell_type='code',metadata={},source=code.splitlines(keepends=True),outputs=[],execution_count=None))
    nb=dict(cells=cells,metadata=dict(kernelspec=dict(display_name='Python research environment',language='python',name='python3')),
            nbformat=4,nbformat_minor=4)
    (ROOT/f'notebooks/{number}_{title.replace(" ","_")}.ipynb').write_text(json.dumps(nb,indent=1)+'\n',encoding='utf-8')


if __name__=='__main__':
    patch_legacy()
    make_notebook(15,'Original_Space_and_Missing_Data',['prepare','benchmark','robust','calibration','sensitivity'])
    make_notebook(16,'Independent_Imputation_Ensembles',['ensemble','aggregate','scaling'])
    make_notebook(17,'Patient_Trajectories',['trajectory','report'])
