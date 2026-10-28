# Security Scan Script for Telco Health Connect Payment Service
# Save as: scripts/security_scan.ps1

param(
    [string]$EvidenceDir = ".\evidence"
)

# Create evidence directory if it doesn't exist
if (-not (Test-Path $EvidenceDir)) {
    New-Item -ItemType Directory -Path $EvidenceDir | Out-Null
}

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

Write-Host "Starting security scans..." -ForegroundColor Green
Write-Host "Timestamp: $timestamp" -ForegroundColor Gray

# Install security tools if needed
Write-Host "`nChecking security tools..." -ForegroundColor Yellow
if (-not (Get-Command bandit -ErrorAction SilentlyContinue)) {
    Write-Host "Installing bandit..." -ForegroundColor Yellow
    pip install bandit --quiet
}
if (-not (Get-Command pip-audit -ErrorAction SilentlyContinue)) {
    Write-Host "Installing pip-audit..." -ForegroundColor Yellow
    pip install pip-audit --quiet
}

# Run Bandit SAST scan
Write-Host "`nRunning Bandit SAST scan..." -ForegroundColor Yellow
$banditOutput = "$EvidenceDir\bandit_$timestamp.txt"
bandit -r app/ -f txt -o $banditOutput 2>&1
Write-Host "Bandit scan complete. Results saved to: $banditOutput" -ForegroundColor Green

# Run pip-audit SCA scan
Write-Host "`nRunning pip-audit SCA scan..." -ForegroundColor Yellow
$pipAuditOutput = "$EvidenceDir\pip_audit_$timestamp.txt"
pip-audit -r requirements.txt -f txt -o $pipAuditOutput 2>&1
Write-Host "pip-audit scan complete. Results saved to: $pipAuditOutput" -ForegroundColor Green

# Copy to standard evidence locations
Copy-Item $banditOutput "$EvidenceDir\bandit_initial.txt" -Force
Copy-Item $pipAuditOutput "$EvidenceDir\pip_audit_initial.txt" -Force

Write-Host "`nSecurity scans completed!" -ForegroundColor Green
Write-Host "Evidence files:" -ForegroundColor Gray
Write-Host "  - $EvidenceDir\bandit_initial.txt"
Write-Host "  - $EvidenceDir\pip_audit_initial.txt"