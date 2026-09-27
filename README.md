# Python API Automation Framework with Requests + Behave BDD

**Author:** Dibyojyoti Datta
**Stack:** Python 3.11 · Requests · Behave · Allure · MySQL
**Scope:** Capstone Assignment 3 — User Management API automation

---

## What It Is

A reusable, layered **API automation framework** that automates the User
Management API of **AutomationExercise** and validates contract behaviour on
**JSONPlaceholder** — proving the framework is service-agnostic.

It is designed as a *framework*, not a script collection:

- Session-based HTTP client with retry, masking, and timing
- Uniform `APIResponse` wrapper used across all services
- Centralized endpoint constants (`services/_endpoints.py`)
- Idempotent test data (Faker + UUID)
- MySQL mirror for cross-verification of API state
- Allure reporting with per-step request/response attachments

---

## Quick Start

    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    python -m db.init_db
    python run.py --allure
    allure open reports/allure-report

---

## Directory Layout

    configs/     Environment YAML (dev / qa / prod)
    core/        HTTP client, auth handlers, response validator
    services/    Domain services (User, Auth, Product, Post)
    utils/       Config, logger, data readers, DB, payloads
    features/    Behave features, hooks, step definitions
    testdata/    YAML / JSON / CSV inputs
    schemas/     JSON schemas for contract validation
    db/          MySQL DDL + init script
    reports/     Allure artifacts
    logs/        Runtime logs
    docs/        Architecture, strategy, demo, viva Q&A
    run.py       CLI runner

---

## Tags

| Tag          | Purpose                     |
|--------------|-----------------------------|
| @smoke       | Critical-path scenarios     |
| @regression  | Full sweep                  |
| @negative    | Error-path scenarios        |
| @contract    | Schema-validated scenarios  |
| @database    | MySQL cross-verification    |
| @auth        | Authentication domain       |
| @user_mgmt   | User Management domain      |
| @catalog     | Product Catalog domain      |

---

## Run Examples

    behave                              # all scenarios
    python run.py --tags=@smoke         # smoke only
    python run.py --tags=@database      # DB verification scenarios
    python run.py --env=qa              # switch environment
    python run.py --allure              # full + Allure HTML report

---

## Documentation

- [README_DETAILED.md](README_DETAILED.md) — full walkthrough of architecture,
  concepts, and every file
- [docs/architecture.md](docs/architecture.md)
- [docs/test_strategy.md](docs/test_strategy.md)
- [docs/demo_script.md](docs/demo_script.md)
- [docs/viva_qna.md](docs/viva_qna.md)

---

## Author

**Dibyojyoti Datta**