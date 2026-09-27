# Demo Script (5-7 minutes)

## 0. Pre-flight (before demo)

    cd C:\Users\rajdi\Downloads\Capstone1
    .\.venv\Scripts\Activate.ps1

Have these windows open:
- PowerShell (project root)
- Browser tab on https://automationexercise.com/api_list
- MySQL Workbench (or a terminal querying MySQL)

## 1. Elevator Pitch (30 s)

"This is a Python API automation framework built with Requests and Behave BDD.
It automates User Management on AutomationExercise, validates contracts with
JSON Schema, and mirrors state into MySQL for cross-verification. All results
are captured in an Allure report."

## 2. Show the Structure (45 s)

    Get-ChildItem -Name
    Get-ChildItem features -Name
    Get-ChildItem features\steps -Name

Point out: features, steps, services, core, utils, schemas — the layers.

## 3. Run Smoke Only (1 min)

    python run.py --tags=@smoke

Narrate: "Smoke suite runs critical-path scenarios — login, create user,
fetch products. Notice the structured logs — each request is logged with
method, URL, status, and elapsed ms."

## 4. Show Allure Report (1 min)

    python run.py --allure

Then:

    allure open reports/allure-report

Point at:
- Behaviors view (grouped by feature)
- Click into a scenario — show attached request/response bodies
- Graphs — pass rate
- Timing — total runtime

## 5. Show MySQL Cross-Verification (1 min)

Run a database-tagged scenario:

    python run.py --tags=@database

Then query:

    python -c "from utils import DBConnector; db=DBConnector(); rows=db.fetch_all('SELECT id, email, company FROM user_management ORDER BY id DESC LIMIT 5'); [print(r) for r in rows]; db.close()"

Say: "The framework mirrors every API-created user into MySQL. If the API
lies about persistence, the database assertion catches it."

## 6. Failure Demo (optional — big wow factor) (1 min)

Temporarily break a schema file (`schemas/product_schema.json`) and re-run:

    python run.py --tags=@contract

Show how Allure captures the exact assertion failure with the offending
payload attached. Revert the schema.

## 7. Q&A Prep (see viva_qna.md)

---

## Talking Points If Asked "Why Not Just requests.get()?"

- Sessions, retries, masking, timing, uniform response objects
- Same client drives two different APIs → reusability
- Assertion library → identical tests across services

## If Asked "Why Behave Rather Than Pytest?"

- Business-readable features
- Free data-driven tests (Scenario Outline)
- Hooks centralize lifecycle
- Same framework could support Selenium via new steps only

## If Asked "What Is the Hardest Part?"

- Handling AutomationExercise's 200-with-body-error convention: HTTP status
  is 200 even for business errors; must assert on `responseCode` in the body.