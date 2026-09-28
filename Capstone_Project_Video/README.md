# Capstone Project — Demo & Screenshots

## Demo Video & Screenshots

<div align="center">

### Demo Walkthrough

[![Watch Demo](https://img.shields.io/badge/Watch_Demo_Video-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://drive.google.com/drive/folders/117MXWunjaJcR2FqhbYqhlbEuV-AdYzGT)

*Full framework walkthrough — architecture, live test run, Allure report, and database verification.*

</div>

### Screenshots

<div align="center">
  <img src="https://github.com/user-attachments/assets/8b333e5f-10e5-4c47-9d78-95c8f0ecb002" width="400" />
  <img src="https://github.com/user-attachments/assets/ee2dfea3-1871-4e90-b721-6c86208721fb" width="400" />
  <img src="https://github.com/user-attachments/assets/35052825-279a-4470-90ca-49073f4a6c1e" width="400" />
</div>

---

## 📖 Overview

This capstone project demonstrates an end-to-end test automation framework built with **Python**, **Selenium WebDriver**, **PyTest**, **Behave (BDD)**, and **Robot Framework**. It covers UI automation, API testing, data-driven testing, reporting, and database verification — following industry best practices such as the Page Object Model, explicit waits, and CI-friendly test reports.

### 🎯 Objectives

- Build a modular, reusable automation framework from scratch
- Apply the Page Object Model (POM) design pattern for maintainability
- Demonstrate data-driven testing using CSV and `@pytest.mark.parametrize`
- Integrate BDD with Gherkin scenarios for readable test cases
- Generate rich HTML and Allure reports for stakeholders
- Validate REST APIs and cross-check results against the database

### 🛠️ Tech Stack

| Layer | Tools / Libraries |
|---|---|
| Language | Python 3.11+ |
| UI Automation | Selenium WebDriver |
| Test Runners | PyTest, Behave, Robot Framework |
| API Testing | `requests` |
| Reporting | `pytest-html`, Allure |
| Database | SQLite / MySQL |
| CI | GitHub Actions |

### ✅ Key Features

- **Cross-browser support** — Chrome, Firefox, Edge (via `webdriver-manager`)
- **Explicit waits** — no `time.sleep()`, all waits use `WebDriverWait`
- **Data-driven** — external CSV / JSON for login and API payloads
- **Modular page objects** — assertions separated from locators
- **Rich reporting** — Allure + `pytest-html` self-contained report
- **API + DB validation** — POST / GET requests verified against stored records
- **CI-ready** — runs headless in GitHub Actions on every push

### ▶️ How to Run

```bash
git clone https://github.com/knowyourmaster05/wipro-capstone-assignments.git
cd wipro-capstone-assignments/Capstone_Project
pip install -r requirements.txt
pytest --html=reports/report.html --self-contained-html
behave features/
robot robot/
allure serve reports/allure-results
