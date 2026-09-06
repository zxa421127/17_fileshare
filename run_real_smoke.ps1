$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot

Write-Host "====================================="
Write-Host "PM Knowledge Portal Real Smoke Test"
Write-Host "====================================="

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw "Docker command not found. Start Docker Desktop and try again."
}

Write-Host "[1/7] Starting PostgreSQL, MinIO and backend..."
docker compose up -d
if ($LASTEXITCODE -ne 0) { throw "docker compose up failed" }

Write-Host "[2/7] Waiting for backend..."
$ready = $false
for ($i = 1; $i -le 30; $i++) {
    try {
        $root = Invoke-RestMethod -Uri "http://127.0.0.1:8000/" -Method Get -TimeoutSec 3
        if ($root.service) {
            $ready = $true
            break
        }
    }
    catch {
        Start-Sleep -Seconds 2
    }
}
if (-not $ready) {
    docker compose ps
    docker compose logs backend --tail 120
    throw "Backend did not become ready"
}

Write-Host "[3/7] Creating/updating smoke-test administrator..."
$username = "smoke_admin"
$password = "Smoke-" + [Guid]::NewGuid().ToString("N") + "!9"

docker compose exec -T backend python create_admin.py --username $username --password $password --email "smoke@example.com"
if ($LASTEXITCODE -ne 0) { throw "Administrator bootstrap failed" }

Write-Host "[4/7] Logging in..."
$loginBody = @{ username = $username; password = $password } | ConvertTo-Json
$login = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/auth/login" -Method Post -ContentType "application/json" -Body $loginBody
$token = $login.access_token
if (-not $token) { throw "Login did not return access_token" }
$headers = @{ Authorization = "Bearer $token" }

Write-Host "[5/7] Uploading a real file through FastAPI into MinIO..."
$tempFile = Join-Path $env:TEMP ("pm-smoke-" + [Guid]::NewGuid().ToString("N") + ".txt")
"PM Knowledge Portal real smoke test $(Get-Date -Format o)" | Set-Content -Path $tempFile -Encoding UTF8

$httpClient = [System.Net.Http.HttpClient]::new()
$httpClient.DefaultRequestHeaders.Authorization = [System.Net.Http.Headers.AuthenticationHeaderValue]::new("Bearer", $token)
$fileStream = [System.IO.File]::OpenRead($tempFile)
$fileContent = [System.Net.Http.StreamContent]::new($fileStream)
$fileContent.Headers.ContentType = [System.Net.Http.Headers.MediaTypeHeaderValue]::Parse("text/plain")
$multipart = [System.Net.Http.MultipartFormDataContent]::new()
$multipart.Add($fileContent, "file", [System.IO.Path]::GetFileName($tempFile))

try {
    $uploadResponse = $httpClient.PostAsync("http://127.0.0.1:8000/api/files/upload", $multipart).GetAwaiter().GetResult()
    $uploadText = $uploadResponse.Content.ReadAsStringAsync().GetAwaiter().GetResult()
    if (-not $uploadResponse.IsSuccessStatusCode) {
        throw "Upload failed: HTTP $([int]$uploadResponse.StatusCode) $uploadText"
    }
    $uploaded = $uploadText | ConvertFrom-Json
}
finally {
    $fileStream.Dispose()
    $fileContent.Dispose()
    $multipart.Dispose()
    $httpClient.Dispose()
    Remove-Item $tempFile -Force -ErrorAction SilentlyContinue
}

if (-not $uploaded.id) { throw "Upload response missing file id" }

Write-Host "[6/7] Verifying PostgreSQL metadata and owner-scoped file list..."
$files = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/files" -Headers $headers -Method Get
$found = @($files) | Where-Object { $_.id -eq $uploaded.id }
if (-not $found) { throw "Uploaded file was not found in file list" }

Write-Host "[7/7] Requesting MinIO presigned download URL..."
$download = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/files/$($uploaded.id)/download" -Headers $headers -Method Get
if (-not $download.url) { throw "Download endpoint did not return a URL" }

Write-Host ""
Write-Host "REAL INFRA GATE: PASSED"
Write-Host "PostgreSQL metadata: PASSED"
Write-Host "MinIO upload: PASSED"
Write-Host "Authentication: PASSED"
Write-Host "Owner-scoped listing: PASSED"
Write-Host "Presigned download URL: PASSED"
Write-Host ""
Write-Host "Uploaded file id: $($uploaded.id)"
Write-Host "Download URL: $($download.url)"
Write-Host ""
Write-Host "Docker services:"
docker compose ps
