# Maven Installation Helper
# Run this script to download and install Maven on Windows

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Green
Write-Host "Maven Installation Helper" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Configuration
$mavenVersion = "3.9.6"
$mavenUrl = "https://dlcdn.apache.org/maven/maven-3/$mavenVersion/binaries/apache-maven-$mavenVersion-bin.zip"
$installDir = "$env:USERPROFILE\maven"
$zipFile = "$env:TEMP\maven.zip"

try {
    Write-Host "`nChecking if Maven is already installed..." -ForegroundColor Yellow
    try {
        $existingMaven = mvn --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Maven is already installed!" -ForegroundColor Green
            Write-Host $existingMaven
            exit 0
        }
    } catch {
        # Maven not found, proceed with installation
    }

    Write-Host "`n[1/4] Downloading Maven $mavenVersion..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri $mavenUrl -OutFile $zipFile
    Write-Host "  ✓ Downloaded to $zipFile" -ForegroundColor Green

    Write-Host "`n[2/4] Extracting Maven..." -ForegroundColor Yellow
    if (Test-Path $installDir) {
        Remove-Item -Recurse -Force $installDir
    }
    Expand-Archive -Path $zipFile -DestinationPath $installDir -Force
    
    # Move files up one level (remove apache-maven-x.x.x folder)
    $innerDir = Get-ChildItem -Path $installDir -Directory | Select-Object -First 1
    Get-ChildItem -Path $innerDir.FullName | Move-Item -Destination $installDir -Force
    Remove-Item -Recurse -Force $innerDir.FullName
    
    Write-Host "  ✓ Extracted to $installDir" -ForegroundColor Green

    Write-Host "`n[3/4] Adding Maven to PATH..." -ForegroundColor Yellow
    $mavenBinPath = "$installDir\bin"
    
    # Get current user PATH
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    
    # Add Maven to PATH if not already there
    if ($currentPath -notlike "*$mavenBinPath*") {
        $newPath = "$currentPath;$mavenBinPath"
        [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
        $env:Path = "$env:Path;$mavenBinPath"
        Write-Host "  ✓ Added $mavenBinPath to PATH" -ForegroundColor Green
    } else {
        Write-Host "  ✓ Maven already in PATH" -ForegroundColor Green
    }

    Write-Host "`n[4/4] Verifying installation..." -ForegroundColor Yellow
    $env:Path = [Environment]::GetEnvironmentVariable("Path", "User") + ";" + [Environment]::GetEnvironmentVariable("Path", "Machine")
    
    $verification = & "$mavenBinPath\mvn.cmd" --version 2>&1
    Write-Host $verification -ForegroundColor Green

    # Clean up
    Remove-Item -Force $zipFile

    Write-Host "`n========================================" -ForegroundColor Green
    Write-Host "✅ Maven installed successfully!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "`nIMPORTANT: Please restart your terminal or VS Code" -ForegroundColor Yellow
    Write-Host "Then run: mvn --version" -ForegroundColor Yellow
    Write-Host "`nMaven Home: $installDir" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Green

} catch {
    Write-Host "`n✗ Installation failed: $_" -ForegroundColor Red
    Write-Host "`nManual installation:" -ForegroundColor Yellow
    Write-Host "1. Download from: https://maven.apache.org/download.cgi"
    Write-Host "2. Extract to: $installDir"
    Write-Host "3. Add to PATH: $installDir\bin"
    exit 1
}
