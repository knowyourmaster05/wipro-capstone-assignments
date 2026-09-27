<div align="center">

# Python Automation Assignments

### Selenium · PyTest · Behave · Robot Framework

**Python Automation Course · 2026**

[![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.x-43B02A?style=for-the-badge&logo=selenium&logoColor=white)](https://selenium.dev/)
[![PyTest](https://img.shields.io/badge/PyTest-Framework-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest.org/)
[![Behave](https://img.shields.io/badge/Behave-BDD-4B8BBE?style=for-the-badge)](https://behave.readthedocs.io/)
[![Robot](https://img.shields.io/badge/Robot_Framework-000000?style=for-the-badge&logo=robotframework&logoColor=white)](https://robotframework.org/)

</div>

---

## Table of Contents

| Section | What you'll find |
|---|---|
| [Overview](#overview) | What this folder contains |
| [Demo Video & Screenshots](#demo-video--screenshots) | Walkthrough video + visual proof |
| [Assignments at a Glance](#assignments-at-a-glance) | Full index table with code + video links |
| [Part 1 — Automation with Selenium](#part-1--automation-with-selenium) | Locators, waits, alerts, tables, windows |
| [Part 2 — Unit Test Frameworks](#part-2--unit-test-frameworks) | POM, DDT, HTML reporting |
| [Part 3 — Python BDD + REST API](#part-3--python-bdd--rest-api) | Behave + Requests |
| [Part 4 — Robot Framework](#part-4--robot-framework) | Basics, variables, custom keywords |
| [Folder Structure](#folder-structure) | Full directory tree |
| [Dependencies](#dependencies) | Required libraries and versions |
| [How to Run](#how-to-run) | Every command you need |
| [Test Sites Used](#test-sites-used) | Public sites and endpoints |
| [Notes](#notes) | Course-specific remarks |

---

## Overview

This folder contains **all course assignments**, organized into four thematic parts that mirror the syllabus progression:

1. **Selenium WebDriver** — browser automation fundamentals
2. **Unit Test Frameworks** — PyTest, Page Object Model, data-driven testing
3. **BDD + REST API** — Behave (Gherkin) and Requests-based API testing
4. **Robot Framework** — keyword-driven automation

Each part has its own subfolder with runnable scripts, test data, and — in some cases — its own `README.md` with a deeper explanation.

---

## Assignments at a Glance

| # | Part | Assignment | Code | Video |
|:--:|---|---|:--:|:--:|
| 1 | Selenium | **Locators** — Login to saucedemo.com using ID, Name, and XPath strategies | [Code](./Part_1_Automation_With_Selenium/assignment_1_locators.py) | [Video](<!-- ADD VIDEO LINK -->) |
| 2 | Selenium | **Synchronization** — Explicit waits with WebDriverWait (no `time.sleep()`) | [Code](./Part_1_Automation_With_Selenium/assignment_2_sync.py) | [Video](<!-- ADD VIDEO LINK -->) |
| 3 | Selenium | **Dropdowns & Checkboxes** — Verify state with `.is_selected()`; autocomplete dropdown loop | [Code](./Part_1_Automation_With_Selenium/assignment_3_dropdowns_checkboxes.py) | [Video](<!-- ADD VIDEO LINK -->) |
| 4 | Selenium | **JavaScript Alerts** — Handle Alert, Confirm, and Prompt dialogs | [Code](./Part_1_Automation_With_Selenium/assignment_4_alerts.py) | [Video](<!-- ADD VIDEO LINK -->) |
| 5 | Selenium | **Web Tables** — Iterate rows/columns, find by string match, extract adjacent value | [Code](./Part_1_Automation_With_Selenium/assignment_5_webtables.py) | [Video](<!-- ADD VIDEO LINK -->) |
| 6 | Selenium | **Windows · Tabs · Frames** — Switch contexts with `switch_to.frame()` and `window_handles` | [Code](./Part_1_Automation_With_Selenium/assignment_6_windows_frames.py) | [Video](<!-- ADD VIDEO LINK -->) |
| 7 | PyTest | **Page Object Model** — BasePage → LoginPage → PyTest tests with separated assertions | [Code](./Part_2_Unit_Test_Frameworks/assignment_7_pom/) | [Video](<!-- ADD VIDEO LINK -->) |
| 8 | PyTest | **Data-Driven Testing** — CSV + `@pytest.mark.parametrize` over multiple login combos | [Code](./Part_2_Unit_Test_Frameworks/assignment_8_ddt.py) | [Video](<!-- ADD VIDEO LINK -->) |
| 9 | PyTest | **HTML Reporting** — Module-scoped fixture + `pytest-html` self-contained report | [Code](./Part_2_Unit_Test_Frameworks/assignment_9_pytest_html.py) | [Video](<!-- ADD VIDEO LINK -->) |
| 10 | Behave | **BDD Framework** — Gherkin scenarios + step definitions for login flows | [Code](./Part_3_Python_BDD_Restful_Automations/features/login.feature) | [Video](<!-- ADD VIDEO LINK -->) |
| 11 | Behave | **Data-Driven API** — POST JSON payloads, validate 201 + response body | [Code](./Part_3_Python_BDD_Restful_Automations/assignment_2_api_data_driven.py) | [Video](<!-- ADD VIDEO LINK -->) |
| 12 | Robot | **Basic Syntax** — SeleniumLibrary keywords for login + inventory verification | [Code](./Part_4_Robot_Framework/assignment_1_basic.robot) | [Video](<!-- ADD VIDEO LINK -->) |
| 13 | Robot | **Variables** — `${VARIABLE}` syntax in the `*** Variables ***` section | [Code](./Part_4_Robot_Framework/assignment_2_variables.robot) | [Video](<!-- ADD VIDEO LINK -->) |
| 14 | Robot | **Custom Keywords** — User-defined keywords with `[Arguments]` + `[Teardown]` | [Code](./Part_4_Robot_Framework/assignment_3_custom_keywords.robot) | [Video](<!-- ADD VIDEO LINK -->) |

---

## Part 1 — Automation with Selenium

**Folder:** [`Part_1_Automation_With_Selenium/`](./Part_1_Automation_With_Selenium/)

Covers core Selenium WebDriver concepts — locating elements, waiting for conditions, handling alerts, reading tables, and switching contexts.

| # | Topic | What it demonstrates |
|---|---|---|
| 1 | **Locators** | Log into saucedemo.com using three different locator strategies — `By.ID`, `By.NAME`, `By.XPATH`. Validates redirect to `inventory.html`. |
| 2 | **Synchronization** | Wait for a dynamically-loaded element using `WebDriverWait` + `expected_conditions`. Explicit waits only — no `time.sleep()`. |
| 4 | **JavaScript Alerts** | Handle JS `Alert`, `Confirm`, and `Prompt` dialogs — accept, dismiss, and enter text into the prompt. |
| 5 | **Web Tables** | Iterate rows and columns of an HTML `<table>`, find a row by string match, extract an adjacent column value. |
| 6 | **Windows · Tabs · Frames** | Switch into an iframe with `switch_to.frame()`, open a new tab, and switch between tabs using `window_handles`. |

---

## Part 2 — Unit Test Frameworks

**Folder:** [`Part_2_Unit_Test_Frameworks/`](./Part_2_Unit_Test_Frameworks/)

Introduces PyTest and design patterns that make test code maintainable.

| # | Topic | What it demonstrates |
|---|---|---|
| 7 | **Page Object Model** | A reusable `BasePage` class (`find`, `click`, `type`) and a `LoginPage` subclass holding locators + UI actions. Tests assert separately from locators. |
| 8 | **Data-Driven Testing** | External CSV (`testdata.csv`) driven through `@pytest.mark.parametrize` — loops over multiple username/password combinations. |
| 9 | **HTML Reporting** | Module-scoped PyTest fixture for browser setup/teardown. Generates a self-contained HTML report via `pytest-html`. |

**Key files in Assignment 7:**

- `base_page.py` — the reusable base with generic `find`, `click`, `type`
- `login_page.py` — the LoginPage, inherits BasePage, holds locators + actions
- `test_login_pom.py` — PyTest tests with assertions separated from the page objects

---

## Part 3 — Python BDD + REST API

**Folder:** [`Part_3_Python_BDD_Restful_Automations/`](./Part_3_Python_BDD_Restful_Automations/)

Bridges UI automation into behavior-driven development and API testing.

| # | Topic | What it demonstrates |
|---|---|---|
| B1 | **Behave BDD Framework** | Gherkin scenarios (`login.feature`) with Given/When/Then steps implemented in `steps/login_steps.py`. |
| B2 | **Data-Driven API Automation** | POST requests to `jsonplaceholder.typicode.com/posts` with multiple JSON payloads via `@pytest.mark.parametrize`. Validates `201` status and response body. |

**Files in B1:**

- `features/login.feature` — Gherkin scenarios: *Successful Login*, *Invalid Login*
- `features/steps/login_steps.py` — step definitions

**Run with:**

```powershell
behave Part_3_Python_BDD_Restful_Automations
```

---

## Part 4 — Robot Framework

**Folder:** [`Part_4_Robot_Framework/`](./Part_4_Robot_Framework/)

Keyword-driven automation with Robot Framework and SeleniumLibrary.

| # | Topic | What it demonstrates |
|---|---|---|
| R1 | **Basic Syntax** | Opens a browser, logs in, verifies the inventory page, closes the browser — using SeleniumLibrary keywords. |
| R2 | **Variables** | Same login flow but using variables declared in the `*** Variables ***` section with `${VARIABLE}` syntax. |
| R3 | **Custom Keywords** | Refactors the login flow into user-defined keywords using `[Arguments]` and `[Teardown]`. |

Robot Framework auto-generates `report.html`, `log.html`, and `output.xml` on every run.

---

## Folder Structure

```
Assignments/
├── venv/                               Virtual environment (not committed)
├── run_all.ps1                         One-shot runner for every part
├── README.md                           ← you are here
│
├── Part_1_Automation_With_Selenium/
│   ├── assignment_1_locators.py
│   ├── assignment_2_sync.py
│   ├── assignment_4_alerts.py
│   ├── assignment_5_webtables.py
│   └── assignment_6_windows_frames.py
│
├── Part_2_Unit_Test_Frameworks/
│   ├── testdata.csv
│   ├── assignment_8_ddt.py
│   ├── assignment_9_pytest_html.py
│   └── assignment_7_pom/
│       ├── base_page.py
│       ├── login_page.py
│       └── test_login_pom.py
│
├── Part_3_Python_BDD_Restful_Automations/
│   ├── assignment_2_api_data_driven.py
│   └── features/
│       ├── login.feature
│       └── steps/
│           └── login_steps.py
│
└── Part_4_Robot_Framework/
    ├── assignment_1_basic.robot
    ├── assignment_2_variables.robot
    └── assignment_3_custom_keywords.robot
```

---

## Dependencies

```
selenium
pytest
pytest-html
behave
robotframework
robotframework-seleniumlibrary
requests
```

Install with:

```powershell
pip install -r requirements.txt
```

---

## How to Run

### Activate the virtual environment

```powershell
cd Assignments
.\venv\Scripts\Activate.ps1
```

### Run everything at once

```powershell
.\run_all.ps1
```

### Run individual parts

**Part 1 — Selenium:**

```powershell
python Part_1_Automation_With_Selenium\assignment_1_locators.py
python Part_1_Automation_With_Selenium\assignment_2_sync.py
python Part_1_Automation_With_Selenium\assignment_4_alerts.py
python Part_1_Automation_With_Selenium\assignment_5_webtables.py
python Part_1_Automation_With_Selenium\assignment_6_windows_frames.py
```

**Part 2 — PyTest:**

```powershell
pytest Part_2_Unit_Test_Frameworks\assignment_7_pom\
pytest Part_2_Unit_Test_Frameworks\assignment_8_ddt.py
pytest Part_2_Unit_Test_Frameworks\assignment_9_pytest_html.py --html=report.html --self-contained-html
```

**Part 3 — Behave + API:**

```powershell
behave Part_3_Python_BDD_Restful_Automations
pytest Part_3_Python_BDD_Restful_Automations\assignment_2_api_data_driven.py
```

**Part 4 — Robot Framework:**

```powershell
robot Part_4_Robot_Framework
```

After running Robot, open `report.html` and `log.html` in the same directory.

---

## Test Sites Used

| Purpose | Site / Endpoint |
|---|---|
| Selenium practice site | [saucedemo.com](https://www.saucedemo.com) — credentials: `standard_user` / `secret_sauce` |
| API test endpoint | [jsonplaceholder.typicode.com/posts](https://jsonplaceholder.typicode.com/posts) |
| Alert / table / frame demos | Local HTML fixtures or embedded JS test pages |

---

## Notes

- **Assignment 3 is intentionally absent** in Part 1 — the syllabus skips from 2 to 4.
- Robot Framework generates `report.html`, `log.html`, and `output.xml` in the working directory on each run.
- PyTest HTML report is generated via the `pytest-html` plugin with `--self-contained-html` so the file is portable.
- All scripts use explicit waits — `time.sleep()` is avoided except where a specific assignment explicitly forbids it.

---

<div align="center">

**All assignments runnable · All reports attached · All code documented**

*Python Automation Course · 2026*

</div>
