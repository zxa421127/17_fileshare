$ErrorActionPreference = "Stop"

Write-Host "================================"
Write-Host "PM Knowledge Portal Quality Gate"
Write-Host "================================"

$CoverageMin = 80

python -m pytest tests -v `
    --cov=app `
    --cov-report=term-missing `
    --cov-report=xml:coverage.xml `
    --junitxml=pytest-results.xml `
    --cov-fail-under=$CoverageMin

if ($LASTEXITCODE -ne 0) {
    Write-Host "QUALITY GATE: FAILED"
    Write-Host "Required coverage: $CoverageMin%"
    exit $LASTEXITCODE
}

Write-Host "AUTH GATE: PASSED"
Write-Host "FILE GATE: PASSED"
Write-Host "COVERAGE GATE: PASSED (>= $CoverageMin%)"
Write-Host "QUALITY GATE: PASSED"
