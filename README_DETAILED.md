# API Automation Framework — Detailed Guide

> Companion to `README.md`. This document explains **what the project is**,
> **how it is organized**, **why each design choice was made**, and
> **what every file does**.

---

## Table of Contents

1. [Overview](#1-overview)
2. [High-Level Architecture](#2-high-level-architecture)
3. [Concepts Used](#3-concepts-used)
4. [Data Flow of a Scenario](#4-data-flow-of-a-scenario)
5. [Folder-by-Folder Walkthrough](#5-folder-by-folder-walkthrough)
6. [File-by-File Reference](#6-file-by-file-reference)
7. [Test Data, Schemas, and Databases](#7-test-data-schemas-and-databases)
8. [Running the Suite](#8-running-the-suite)
9. [Reporting with Allure](#9-reporting-with-allure)
10. [Extending the Framework](#10-extending-the-framework)
11. [Design Decisions and Rationale](#11-design-decisions-and-rationale)

---

## 1. Overview

The project automates the **User Management API** of
[AutomationExercise](https://automationexercise.com/api_list) and validates
contract behaviour on
[JSONPlaceholder](https://jsonplaceholder.typicode.com/).

- **AutomationExercise** provides real user lifecycle endpoints — create
  account, verify login, update, delete, fetch-by-email — and a catalog
  (`/productsList`, `/brandsList`, `/searchProduct`).
- **JSONPlaceholder** is a fake REST service used for contract testing of
  `/users`, `/posts`, `/comments`, `/todos`.

Running the same framework against two very different APIs demonstrates that
the design is **service-agnostic** — the same client, validators, and step
vocabulary work across both.

---

## 2. High-Level Architecture

    ┌───────────────────────────────────────────────────────────┐
    │                   features/  (BDD Layer)                  │
    │   .feature files         environment.py      steps/*.py   │
    │   ─────────────         ─────────────        ──────────   │
    │   Business-readable      Lifecycle hooks     Glue code    │
    │   scenarios              (before/after)       (Given/When/│
    │                                                Then)      │
    ├───────────────────────────────────────────────────────────┤
    │                   services/  (Domain Layer)               │
    │   UserService · AuthService · ProductService · PostService│
    │   ─────────────────────────────────────────────────────   │
    │   Domain-level methods (create_user, verify_login, ...)   │
    │   NO assertions. NO hard-coded data. Endpoint-constant-   │
    │   driven.                                                 │
    ├───────────────────────────────────────────────────────────┤
    │                   core/  (Transport Layer)                │
    │   BaseClient · APIResponse · AuthHandler · ResponseValidator│
    │   ─────────────────────────────────────────────────────── │
    │   Sessions, retries, timeouts, masking, timing, uniform   │
    │   response object, assertion helpers.                     │
    ├───────────────────────────────────────────────────────────┤
    │                   utils/  (Cross-cutting)                 │
    │   Config · Logger · DataReader · DBConnector ·            │
    │   UserRepository · PayloadFactory · SchemaLoader          │
    ├───────────────────────────────────────────────────────────┤
    │                   Resources                                │
    │   configs/*.yaml   testdata/*   schemas/*.json   db/*.sql │
    └───────────────────────────────────────────────────────────┘

**Dependency direction is one-way (upwards)** — the BDD layer knows about
services, services know about core, core knows about utils, and utils knows
about the resources. No layer reaches back upward.

---

## 3. Concepts Used

| Concept                              | Where it appears                          |
|--------------------------------------|-------------------------------------------|
| Layered architecture                 | Whole project                             |
| BDD (Behavior-Driven Development)    | `features/*.feature`                      |
| Session-based HTTP client            | `core/base_client.py`                     |
| Response wrapper object              | `core/base_client.py :: APIResponse`      |
| Strategy pattern                     | `core/auth_handler.py`                    |
| JSON Schema contract testing         | `core/response_validator.py`, `schemas/`  |
| Data-driven testing (Scenario Outline)| `features/authentication.feature`, etc.   |
| Fixture factories                    | `utils/payload_factory.py`                |
| Repository pattern (DB)              | `utils/db_repository.py`                  |
| Singleton config                     | `utils/config_loader.py :: Config`        |
| Idempotency through uniqueness       | `PayloadFactory.create_user_payload`      |
| Hooks / lifecycle management         | `features/environment.py`                 |
| Reporting & attachments              | Allure integration in hooks               |
| Retry with exponential backoff       | `core/base_client.py :: _request`         |
| Sensitive-field masking              | `core/base_client.py :: _mask`            |

---

## 4. Data Flow of a Scenario

Take the scenario:
    Behave starts
       │
       ▼
    before_all  ─ load config, ensure reports/ and logs/ exist
       │
       ▼
    before_scenario ─ provision empty context.client = {}
       │
       ▼
    Given the "automation_exercise" API client is ready
       └─▶ environment._get_or_create_client()
              └─▶ BaseClient(service_name="automation_exercise")
                     └─▶ session.headers["User-Agent"] = "Dibyojyoti-QA-Framework/1.0"
       │
       ▼
    When I create a user with a randomly generated payload
       └─▶ steps.user_management.step_create_user()
              ├─▶ PayloadFactory.create_user_payload()      # Faker + uuid
              ├─▶ UserService.create_user(payload)
              │      └─▶ BaseClient.post("/createAccount", data=payload)
              │            ├─▶ mask(password) before logging
              │            ├─▶ send with retry / timeout
              │            └─▶ return APIResponse(...)
              └─▶ UserRepository.insert_user(payload)       # MySQL mirror
       │
       ▼
    Then the response status code should be 200
       └─▶ steps.common.step_status_code()
              └─▶ ResponseValidator.status_code(response, 200)
       │
       ▼
    And the response body should contain "User created!"
       └─▶ ResponseValidator.contains_text(response, "User created!")
       │
       ▼
    after_scenario ─ close clients, best-effort DELETE created users
       │
       ▼
    Allure hook ─ attach request URL, method, status, body, elapsed per step

---

## 5. Folder-by-Folder Walkthrough

### `configs/`
Environment-specific YAML. `Config.get("base_urls.automation_exercise")`
resolves nested keys.

### `core/`
The transport engine. Everything below the domain layer.

### `services/`
Domain verbs. Thin wrappers around `BaseClient` that speak the language of
the API (create_user, verify_login, ...).

### `utils/`
Cross-cutting helpers — config, logging, test data readers, MySQL wrapper,
payload factories, schema loader.

### `features/`
Behave's home. `.feature` files (business scenarios), `environment.py`
(lifecycle hooks), `steps/` (glue code).

### `testdata/`
YAML, JSON, CSV files consumed by `DataReader` for data-driven scenarios.

### `schemas/`
JSON Schema files for contract validation.

### `db/`
`schema.sql` (DDL) and `init_db.py` (creates the database and table).

### `docs/`
Project documentation: architecture, strategy, demo script, viva Q&A.

---

## 6. File-by-File Reference

### Root files

| File                    | Purpose                                                 |
|-------------------------|---------------------------------------------------------|
| `run.py`                | CLI runner — wraps `behave` with flags and Allure       |
| `behave.ini`            | Behave config — formatter, capture, output paths        |
| `requirements.txt`      | Pinned Python dependencies                              |
| `.gitignore`            | Ignores venv, reports, logs, caches                     |
| `README.md`             | Brief project overview                                  |
| `README_DETAILED.md`    | This document                                           |

### `configs/`

| File            | Purpose                                 |
|-----------------|-----------------------------------------|
| `__init__.py`   | Re-exports `Config`                     |
| `dev.yaml`      | Development environment (active by default) |
| `qa.yaml`       | QA environment                          |
| `prod.yaml`     | Production environment                  |

### `core/`

| File                     | Purpose                                                     |
|--------------------------|-------------------------------------------------------------|
| `__init__.py`            | Re-exports public classes                                   |
| `base_client.py`         | `BaseClient` (session, retry, masking, timing) + `APIResponse` |
| `auth_handler.py`        | Strategy pattern — `NoAuth`, `BasicAuth`, `BearerTokenAuth`, `ApiKeyAuth`, `SessionCookieAuth` |
| `response_validator.py`  | Static assertion helpers (status, schema, keys, timing)     |

### `services/`

| File                  | Purpose                                              |
|-----------------------|------------------------------------------------------|
| `__init__.py`         | Re-exports service classes                           |
| `_endpoints.py`       | All endpoint constants in one place                  |
| `user_service.py`     | create / delete / update / get user                  |
| `auth_service.py`     | verify_login + JSONPlaceholder user profile fetch    |
| `product_service.py`  | products, brands, search, negative methods           |
| `post_service.py`     | JSONPlaceholder CRUD                                 |

### `utils/`

| File                  | Purpose                                              |
|-----------------------|------------------------------------------------------|
| `__init__.py`         | Re-exports helpers                                   |
| `config_loader.py`    | Singleton `Config` with dotted-path lookup           |
| `logger.py`           | Idempotent logger factory (console + rotating file)  |
| `data_reader.py`      | YAML / JSON / CSV readers + Scenario-Outline helpers |
| `db_connector.py`     | MySQL wrapper (lazy connect, dict cursor, context mgr) |
| `db_repository.py`    | High-level `UserRepository` CRUD                     |
| `payload_factory.py`  | Faker-based payload generators                       |
| `schema_loader.py`    | Cached JSON schema loader                            |

### `features/`

| File                              | Purpose                                       |
|-----------------------------------|-----------------------------------------------|
| `environment.py`                  | Behave hooks + Allure integration             |
| `user_management.feature`         | User CRUD scenarios                           |
| `authentication.feature`          | Login positive + negative (Scenario Outline)  |
| `product_catalog.feature`         | Products / brands / search + schema checks    |
| `steps/__init__.py`               | Package marker                                |
| `steps/common_steps.py`           | Cross-domain steps (status, message, schema)  |
| `steps/user_management_steps.py`  | User CRUD steps + DB mirror                   |
| `steps/auth_steps.py`             | Login steps                                   |
| `steps/product_steps.py`          | Catalog steps                                 |

### `schemas/`

| File                                  | Validates                                    |
|---------------------------------------|----------------------------------------------|
| `user_schema.json`                    | `/getUserDetailByEmail` response             |
| `product_schema.json`                 | `/productsList` response                     |
| `error_schema.json`                   | Generic error responses                      |
| `login_response_schema.json`          | `/verifyLogin` response                      |
| `jsonplaceholder_post_schema.json`    | JSONPlaceholder `/posts/{id}`                |

### `testdata/`

| File                                  | Contents                                     |
|---------------------------------------|----------------------------------------------|
| `users.yaml`                          | 3 valid AutomationExercise user payloads      |
| `invalid_users.yaml`                  | 5 invalid login scenarios                     |
| `products.csv`                        | Search terms for Scenario Outline             |
| `payloads/create_user.json`           | Fallback template payload                     |

### `db/`

| File             | Purpose                                       |
|------------------|-----------------------------------------------|
| `schema.sql`     | DDL for `api_automation_db.user_management`   |
| `init_db.py`     | Creates database and table                    |

### `docs/`

| File                  | Purpose                                       |
|-----------------------|-----------------------------------------------|
| `architecture.md`     | Diagram + data-flow description               |
| `test_strategy.md`    | Scope, tagging, risks, mitigations            |
| `demo_script.md`      | Step-by-step demo plan                        |
| `viva_qna.md`         | Anticipated Q&A                               |

---

## 7. Test Data, Schemas, and Databases

### Test Data
Two strategies coexist:

1. **Static** — `testdata/*.yaml` and `testdata/*.csv`, read via `DataReader`.
2. **Dynamic** — `PayloadFactory` generates unique payloads per call using
   Faker + UUID. Used by the default scenarios to keep runs idempotent.

### JSON Schemas
Schemas live in the framework, not in tests. They are loaded and cached by
`SchemaLoader` and enforced by `ResponseValidator.json_schema`. When the API
changes shape, only the schema file needs updating.

### MySQL
`db.init_db` provisions the schema. `UserRepository` mirrors API state:

    API call  →  BaseClient returns APIResponse
              →  Step calls UserRepository.insert_user / update / delete
              →  MySQL row reflects the API's claim

Scenarios tagged `@database` add a `Then ... should exist in the database`
assertion, catching any mismatch between what the API says and what it
actually stores.

---

## 8. Running the Suite

### All scenarios

    behave

### With Allure report

    python run.py --allure

### By tag

    behave --tags=@smoke
    behave --tags="@regression and not @database"
    python run.py --tags=@database

### Different environment

    python run.py --env=qa
    python run.py --env=prod

### Behind the scenes

`run.py` sets `ENV`, optionally cleans allure-results, invokes Behave, then
generates the Allure HTML report.

---

## 9. Reporting with Allure

### Generation

    allure generate reports/allure-results -o reports/allure-report --clean

### View

    allure open reports/allure-report

### What's inside

- **Behaviors** — grouped by feature file
- **Suites** — grouped by directory
- **Graphs** — pass/fail rates, severity distribution
- **Timeline** — execution duration per test
- **Per-scenario attachments** — request URL, method, status, body, elapsed
  time for each `When` step

The hook in `features/environment.py :: after_step` performs the attachments.

---

## 10. Extending the Framework

### Add a new API

1. Add the base URL to `configs/*.yaml` under `base_urls.<service_name>`.
2. Create `services/<new_service>.py` with domain methods.
3. Add endpoint constants to `services/_endpoints.py`.
4. Create a `.feature` file and matching steps in `features/steps/`.

### Add a new test data source

1. Place the file under `testdata/`.
2. Use `DataReader.read_yaml / read_json / read_csv` from a step.

### Add a new environment

1. Copy `configs/dev.yaml` → `configs/staging.yaml`.
2. Adjust URLs / DB / timeouts.
3. Run with `python run.py --env=staging`.

### Add Selenium (future Milestone 1)

The service layer is HTTP-agnostic. A `ui/` package could wrap Selenium
without touching any `.feature` file — only new steps would be required.

### Add Robot Framework (future Milestone 3)

`robot/` could call the same services through a thin keyword library, keeping
the service layer as the single source of truth.

---

## 11. Design Decisions and Rationale

### Why a layered architecture?
Separation of concerns. The BDD layer never sees HTTP. The transport layer
never sees business logic. Each layer can be tested and replaced in isolation.

### Why a Session-based client instead of `requests.get`?
- Cookies and auth persist across calls (needed for chained scenarios)
- One place for timeouts, retries, and default headers
- One place to mask sensitive fields in logs
- Uniform response wrapper → assertion code is identical across APIs

### Why is `APIResponse` a wrapper, not just a raw response?
- Auto-parses JSON safely
- Provides `assert_status`, `get("a.b.c")` dotted-path lookup
- Captures timing
- Prints a readable `__repr__`

### Why assertion helpers in `ResponseValidator`?
Step definitions stay one line long. Failures raise a consistent
`AssertionError` with expected / actual / URL / body — never a mystery.

### Why centralize endpoints?
A URL change touches one file. Reviewers can see the full API surface in a
single 20-line module.

### Why two APIs?
JSONPlaceholder can't support user creation or login. AutomationExercise can.
Testing both demonstrates the framework is service-agnostic. JSONPlaceholder
adds contract and negative-path coverage with no state side-effects.

### Why Behave rather than pytest?
- Business-readable `.feature` files
- Free data-driven tests (Scenario Outline)
- Hooks centralize lifecycle
- The same framework can be extended to UI/robot engines without rewriting

### Why MySQL?
Syllabus 19.3 explicitly requires MySQL-driven data. But more importantly,
it lets us **cross-verify** the API's claim against persisted state — a
stronger assertion than response-shape checks alone.

### Why mask sensitive fields?
Passwords and tokens in logs are a common real-world leak. Masking is
applied centrally in `BaseClient._mask` before anything hits the logger.

### Why idempotent test data?
Repeated local runs would otherwise collide on emails. UUID suffixes keep
scenarios independent and re-runnable without cleanup failures.

---

## Author

**Dibyojyoti Datta**