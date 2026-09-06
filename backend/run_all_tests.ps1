$ErrorActionPreference = "Stop"

Write-Host "================================"
Write-Host "PM Knowledge Portal Quality Gate"
Write-Host "================================"

python -m pytest tests -v --cov=app --cov-report=term-missing

if ($LASTEXITCODE -ne 0) {
    Write-Host "QUALITY GATE: FAILED"
    exit $LASTEXITCODE
}

Write-Host "AUTH GATE: PASSED"
Write-Host "FILE GATE: PASSED"
Write-Host "QUALITY GATE: PASSED"
