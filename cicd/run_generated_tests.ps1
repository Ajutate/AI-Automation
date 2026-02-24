# PowerShell script to compile and run generated Selenium tests
# Usage: .\run_generated_tests.ps1 [-TestName "YourTest"]

param(
    [string]$TestName = "GeneratedTest"
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Green
Write-Host "AI-Generated Test Compilation & Execution" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Configuration
$ProjectDir = "test-project"
$OutputDir = "outputs"

try {
    # Step 1: Check prerequisites
    Write-Host "`n[1/6] Checking prerequisites..." -ForegroundColor Yellow
    
    $javaVersion = java -version 2>&1 | Select-Object -First 1
    $mavenVersion = mvn --version 2>&1 | Select-Object -First 1
    
    if (-not $javaVersion -or -not $mavenVersion) {
        throw "Java or Maven not found!"
    }
    
    Write-Host "✓ Java and Maven found" -ForegroundColor Green

    # Step 2: Create project structure
    Write-Host "`n[2/6] Setting up project structure..." -ForegroundColor Yellow
    
    New-Item -ItemType Directory -Force -Path "$ProjectDir\src\test\java\com\automation" | Out-Null
    New-Item -ItemType Directory -Force -Path "$ProjectDir\src\test\resources" | Out-Null
    Copy-Item "cicd\pom.xml" -Destination "$ProjectDir\" -Force
    
    Write-Host "✓ Project structure created" -ForegroundColor Green

    # Step 3: Copy generated tests
    Write-Host "`n[3/6] Copying generated tests..." -ForegroundColor Yellow
    
    $testFile = "$OutputDir\tests\${TestName}Test.java"
    
    if (Test-Path $testFile) {
        Copy-Item $testFile -Destination "$ProjectDir\src\test\java\com\automation\" -Force
        Write-Host "✓ Test file copied: ${TestName}Test.java" -ForegroundColor Green
    } else {
        throw "Test file not found: $testFile"
    }

    # Step 4: Compile tests
    Write-Host "`n[4/6] Compiling tests..." -ForegroundColor Yellow
    
    Push-Location $ProjectDir
    
    $compileOutput = mvn clean compile test-compile 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Compilation successful!" -ForegroundColor Green
    } else {
        Write-Host "✗ Compilation failed!" -ForegroundColor Red
        Write-Host $compileOutput
        throw "Compilation failed"
    }

    # Step 5: Run tests
    Write-Host "`n[5/6] Running tests..." -ForegroundColor Yellow
    
    $testOutput = mvn test -Dtest="${TestName}Test" 2>&1
    $testStatus = $LASTEXITCODE
    
    if ($testStatus -eq 0) {
        Write-Host "✓ Tests executed successfully!" -ForegroundColor Green
    } else {
        Write-Host "⚠ Tests completed with failures" -ForegroundColor Red
    }

    # Step 6: Generate report
    Write-Host "`n[6/6] Generating test report..." -ForegroundColor Yellow
    
    mvn surefire-report:report | Out-Null
    Write-Host "✓ Report generated: $ProjectDir\target\site\surefire-report.html" -ForegroundColor Green

    Pop-Location

    # Summary
    Write-Host "`n========================================" -ForegroundColor Green
    Write-Host "Execution Summary" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "Test Name: ${TestName}Test"
    Write-Host "Source: $OutputDir\tests\${TestName}Test.java"
    Write-Host "Compiled: $ProjectDir\target\test-classes\com\automation\${TestName}Test.class"
    Write-Host "Report: $ProjectDir\target\site\surefire-report.html"
    Write-Host "========================================" -ForegroundColor Green

    exit $testStatus

} catch {
    Write-Host "`n✗ Error: $_" -ForegroundColor Red
    Pop-Location -ErrorAction SilentlyContinue
    exit 1
}
