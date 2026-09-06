$ErrorActionPreference = "Stop"

Write-Host "=============================="
Write-Host "PM Knowledge Portal Auth Gate"
Write-Host "=============================="

python -m pytest tests -v --cov=app --cov-report=term-missing

if ($LASTEXITCODE -ne 0) {
    Write-Host "AUTH GATE: FAILED"
    exit $LASTEXITCODE
}

Write-Host "AUTH GATE: PASSED"
