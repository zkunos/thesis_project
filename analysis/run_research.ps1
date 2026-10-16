param([string]$Python = '.\.venv-research\Scripts\python.exe')
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath (Split-Path -Parent $PSScriptRoot)
foreach ($stage in @('prepare','benchmark','robust','ensemble','aggregate','calibration','sensitivity','scaling','trajectory','report')) {
    Write-Host "Research stage: $stage"
    & $Python -m analysis.run_research --stage $stage
    if ($LASTEXITCODE -ne 0) { throw "Research stage failed: $stage" }
}
& $Python -m analysis.test_research
if ($LASTEXITCODE -ne 0) { throw 'Numerical validation failed' }
& $Python -m analysis.check_artifacts
if ($LASTEXITCODE -ne 0) { throw 'Artifact validation failed' }
