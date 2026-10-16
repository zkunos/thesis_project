param(
    [ValidateRange(1024, 65535)][int]$Port = 8501,
    [string]$Python = (Join-Path $PSScriptRoot '..\.venv-research\Scripts\python.exe')
)

$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $Python)) {
    throw 'Python environment not found. Follow dashboard/README.md or provide -Python with the interpreter path.'
}
Push-Location $PSScriptRoot
try {
    & $Python -m streamlit run Home.py --server.address 127.0.0.1 --server.port $Port --server.fileWatcherType none
    if ($LASTEXITCODE -ne 0) { throw "CogDash exited with code $LASTEXITCODE." }
}
finally {
    Pop-Location
}
