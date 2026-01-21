# MBG Remote Installer for Windows
# Jalankan dengan: irm https://raw.githubusercontent.com/jokobim12/MBG-Manajemen-Basis-Data-Geratis-/main/install.ps1 | iex

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "     MBG - Remote Installer            " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "X Python tidak ditemukan!" -ForegroundColor Red
    Write-Host "  Download dari: https://python.org/downloads" -ForegroundColor Yellow
    exit 1
}

Write-Host "[OK] Python ditemukan" -ForegroundColor Green

# Create MBG directory
$mbgDir = "$env:LOCALAPPDATA\MBG"
Write-Host "Membuat direktori $mbgDir..." -ForegroundColor Yellow

if (Test-Path $mbgDir) {
    Remove-Item $mbgDir -Recurse -Force
}
New-Item -ItemType Directory -Path $mbgDir -Force | Out-Null
New-Item -ItemType Directory -Path "$mbgDir\dapur" -Force | Out-Null

# Download files
Write-Host "Mengunduh file MBG..." -ForegroundColor Yellow
$baseUrl = "https://raw.githubusercontent.com/jokobim12/MBG-Manajemen-Basis-Data-Geratis-/main"

$files = @("mbg.py", "translator.py", "db.py", "bantuan.py")
foreach ($file in $files) {
    Invoke-WebRequest -Uri "$baseUrl/$file" -OutFile "$mbgDir\$file"
}

Write-Host "[OK] File berhasil diunduh" -ForegroundColor Green

# Create launcher batch file
$launcherPath = "$mbgDir\mbg.bat"
@"
@echo off
python "$mbgDir\mbg.py" %*
"@ | Out-File -FilePath $launcherPath -Encoding ASCII

# Add to PATH
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$mbgDir*") {
    [Environment]::SetEnvironmentVariable("Path", "$userPath;$mbgDir", "User")
    Write-Host "[OK] MBG ditambahkan ke PATH" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  [OK] Instalasi berhasil!             " -ForegroundColor Green
Write-Host "                                       " -ForegroundColor Cyan
Write-Host "  Buka terminal baru, lalu ketik: mbg  " -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
