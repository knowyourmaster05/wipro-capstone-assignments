# Test Strategy

## Scope

End-to-end API automation of the User Management, Authentication, and
Product Catalog domains, backed by contract (schema) validation and
database cross-verification.

## Test Pyramid (as applied)

- **Unit (light)**: validators, payload factories, config loader
- **Integration (core)**: services against live APIs, driven by Behave
- **End-to-End (BDD)**: full user lifecycle create → login → update → delete,
  with MySQL mirror verification
- **Contract**: JSON schemas for each response family

## Tagging Strategy

| Tag          | Meaning                                      |
|--------------|----------------------------------------------|
| @smoke       | Fast critical-path checks (run first)        |
| @regression  | Full regression sweep                        |
| @negative    | Error-path / bad-input scenarios             |
| @contract    | Schema-validated scenarios                   |
| @database    | Scenarios that also assert MySQL state       |
| @auth        | Authentication-related                      |
| @user_mgmt   | User Management domain                       |
| @catalog     | Product Catalog domain                       |

Run examples:

    behave --tags=@smoke
    behave --tags="@regression and not @database"
    python run.py --tags=@database --allure

## Why BDD (Behave) Rather Than Plain Pytest

- Feature files are readable by non-technical stakeholders
- Scenario Outlines give us data-driven tests for free
- Hooks centralize setup/teardown without boilerplate
- The same steps work across two different APIs — proof of reusability

## Cleanup and Idempotency

Every scenario is independent:

- PayloadFactory generates unique emails (uuid suffix)
- `after_scenario` best-effort deletes any user created during the run
- MySQL rows are removed on delete; leftover rows don't affect future runs

## Risks and Mitigations

| Risk                                    | Mitigation                                  |
|-----------------------------------------|---------------------------------------------|
| Third-party API downtime                | Retry with exponential backoff              |
| API returns 200 but business error code | Assert body `responseCode` in addition to HTTP status |
| Schema drift                            | Versioned schemas in `schemas/`             |
| Sensitive data in logs                  | Field masking in `BaseClient._mask`         |