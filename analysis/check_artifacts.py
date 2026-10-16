"""Check completed research outputs without loading patient values into logs."""
import ast
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results/research_2026'


def rows(name):
    with (OUT / name).open(encoding='utf-8', newline='') as handle:
        return list(csv.DictReader(handle))


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def main():
    manifest = json.loads((OUT / 'run_manifest.json').read_text())
    for name, expected in manifest['input_hashes'].items():
        assert digest(ROOT / name) == expected, f'Input changed: {name}'
    artifact_hashes = json.loads((OUT / 'artifact_hashes.json').read_text())
    for name, expected in artifact_hashes.items():
        assert digest(ROOT / name) == expected, f'Artifact changed: {name}'
    index = rows('index_patient_manifest.csv')
    by_key = {r['assessment_key']: r for r in index}
    assert len(by_key) == len(index) == 7285
    assert len({r['patient_key'] for r in index}) == len(index)
    assert sum(r['split'] == 'discovery' for r in index) == manifest['train_patients']
    assert sum(r['split'] == 'validation' for r in index) == manifest['validation_patients']
    assignment_models = {}
    for name in ['selected_assignments.csv', 'incomplete_assignments.csv']:
        groups = {}
        for row in rows(name):
            original = by_key[row['assessment_key']]
            assert row['patient_key'] == original['patient_key']
            assert row['split'] == original['split']
            keys = groups.setdefault(row['model'], set())
            assert row['assessment_key'] not in keys
            keys.add(row['assessment_key'])
            if 'maximum_probability' in row:
                assert 0 <= float(row['maximum_probability']) <= 1 + 1e-12
                assert float(row['entropy']) >= -1e-10
        assert groups and all(keys == set(by_key) for keys in groups.values())
        assignment_models[name] = len(groups)
    mixture = rows('incomplete_mixture_comparison.csv')
    expected = {(f, k) for f in ['normal', 't4', 't10', 'contaminated'] for k in range(1, 9)}
    assert {(r['family'], int(r['k'])) for r in mixture} == expected and len(mixture) == 32
    assert all(float(r['min_covariance_eigenvalue']) >= .02 - 1e-10 for r in mixture)
    assert len(rows('cluster_count_distribution.csv')) == 20
    assert len(rows('continuous_null_simulations.csv')) == 100
    notebook_names = ['5_Improved_Clustering_Infrastructure', '14_Backlog_Additions',
                      '15_Original_Space_and_Missing_Data', '16_Independent_Imputation_Ensembles',
                      '17_Patient_Trajectories']
    for name in notebook_names:
        notebook = json.loads((ROOT / 'notebooks' / f'{name}.ipynb').read_text(encoding='utf-8'))
        for cell in notebook['cells']:
            if cell['cell_type'] == 'code':
                source = ''.join(cell['source'])
                # These notebooks contain only line magics, not cell magics.
                source = '\n'.join('' if line.lstrip().startswith(('%', '!')) else line for line in source.splitlines())
                ast.parse(source, filename=name)
    report = ROOT / 'report/research/clustering_results_2026.md'
    assert report.exists() and report.stat().st_size > 1000
    for name in ['scaling_sensitivity', 'imputation_stability', 'incomplete_mixtures', 'validation_profiles']:
        path = report.parent / 'figures' / f'{name}.png'
        assert path.read_bytes()[:8] == b'\x89PNG\r\n\x1a\n'
    result = dict(status='passed', input_hashes_checked=len(manifest['input_hashes']),
                  artifact_hashes_checked=len(artifact_hashes), index_patients=len(index),
                  complete_mixture_fits=len(mixture), assignment_models=assignment_models,
                  notebook_sources_checked=len(notebook_names))
    (OUT / 'artifact_validation.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
