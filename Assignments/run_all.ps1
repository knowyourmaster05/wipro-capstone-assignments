# ============================================
# Run All Assignments - Summary Script
# ============================================

$ErrorActionPreference = "Continue"
$root = "C:\Users\rajdi\Downloads\Assignments"
Set-Location $root

$results = @()

function Run-Step {
    param(
        [string]$Name,
        [scriptblock]$Action
    )
    Write-Host ""
    Write-Host "=== Running: $Name ===" -ForegroundColor Cyan
    try {
        & $Action
        if ($LASTEXITCODE -eq 0 -or $null -eq $LASTEXITCODE) {
            $script:results += [PSCustomObject]@{ Test = $Name; Status = "PASS" }
            Write-Host ">>> $Name : PASS" -ForegroundColor Green
        } else {
            $script:results += [PSCustomObject]@{ Test = $Name; Status = "FAIL" }
            Write-Host ">>> $Name : FAIL" -ForegroundColor Red
        }
    } catch {
        $script:results += [PSCustomObject]@{ Test = $Name; Status = "ERROR" }
        Write-Host ">>> $Name : ERROR - $_" -ForegroundColor Red
    }
}

# ---------- PART 1 ----------
Run-Step "Part1-A1-Locators"      { python Part_1_Automation_With_Selenium\assignment_1_locators.py }
Run-Step "Part1-A2-Sync"          { python Part_1_Automation_With_Selenium\assignment_2_sync.py }
Run-Step "Part1-A4-Alerts"        { python Part_1_Automation_With_Selenium\assignment_4_alerts.py }
Run-Step "Part1-A5-WebTables"     { python Part_1_Automation_With_Selenium\assignment_5_webtables.py }
Run-Step "Part1-A6-WindowsFrames" { python Part_1_Automation_With_Selenium\assignment_6_windows_frames.py }

# ---------- PART 2 ----------
Run-Step "Part2-A7-POM" {
    Push-Location Part_2_Unit_Test_Frameworks\assignment_7_pom
    pytest -q
    Pop-Location
}
Run-Step "Part2-A8-DDT" {
    Push-Location Part_2_Unit_Test_Frameworks
    pytest assignment_8_ddt.py -q
    Pop-Location
}
Run-Step "Part2-A9-PyTestHTML" {
    Push-Location Part_2_Unit_Test_Frameworks
    pytest assignment_9_pytest_html.py -q --html=report.html --self-contained-html
    Pop-Location
}

# ---------- PART 3 ----------
Run-Step "Part3-A1-Behave" {
    Push-Location Part_3_Python_BDD_Restful_Automations
    behave
    Pop-Location
}
Run-Step "Part3-A2-API-DDT" {
    Push-Location Part_3_Python_BDD_Restful_Automations
    pytest assignment_2_api_data_driven.py -q
    Pop-Location
}

# ---------- PART 4 ----------
Run-Step "Part4-RobotFramework" {
    Push-Location Part_4_Robot_Framework
    robot .
    Pop-Location
}

# ---------- SUMMARY ----------
Write-Host ""
Write-Host "============================================" -ForegroundColor Yellow
Write-Host "              FINAL SUMMARY                 " -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Yellow
$results | Format-Table -AutoSize

$pass = ($results | Where-Object { $_.Status -eq "PASS" }).Count
$fail = ($results | Where-Object { $_.Status -ne "PASS" }).Count
Write-Host ""
Write-Host "Passed: $pass / $($results.Count)" -ForegroundColor Green
if ($fail -gt 0) {
    Write-Host "Failed: $fail" -ForegroundColor Red
}
