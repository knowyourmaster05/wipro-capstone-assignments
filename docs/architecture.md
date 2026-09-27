# Architecture

## Overview

The framework is organized as a layered stack. Each layer depends only on
the layers beneath it, keeping responsibilities clean and enabling reuse
across different REST services and different BDD engines.

    ┌─────────────────────────────────────────┐
    │  features/  (BDD - Behave)              │
    │  .feature files + step definitions      │
    ├─────────────────────────────────────────┤
    │  services/  (Domain layer)              │
    │  UserService, AuthService, ...          │
    ├─────────────────────────────────────────┤
    │  core/  (HTTP + assertions)             │
    │  BaseClient, APIResponse, Validators    │
    ├─────────────────────────────────────────┤
    │  utils/  (Cross-cutting)                │
    │  Config, Logger, DataReader, DB, Payload│
    ├─────────────────────────────────────────┤
    │  configs/ + testdata/ + schemas/        │
    └─────────────────────────────────────────┘

## Why Layers?

- **testable**: each layer can be tested in isolation
- **reusable**: the same `BaseClient` drives both AutomationExercise and JSONPlaceholder
- **readable**: feature files never know about HTTP; they speak business language
- **maintainable**: an endpoint change touches exactly one file (`services/_endpoints.py`)

## Data Flow for a Single Scenario

1. Behave reads a `.feature` file
2. `environment.py` provisions a `BaseClient` per service for this scenario
3. Step definitions call domain methods on services (`UserService.create_user`)
4. Services delegate to `BaseClient` which handles session, retry, logging
5. `BaseClient` wraps the response in `APIResponse`
6. Step definitions call `ResponseValidator` methods to assert
7. MySQL mirror is updated via `UserRepository` when relevant
8. Allure hooks attach request/response artifacts for reporting

## Why a Session-Based Client Instead of Bare requests.get()

- Cookies + auth persist across calls (needed for chained scenarios)
- One place to set timeouts, retries, User-Agent
- One place to mask sensitive fields in logs (passwords never leak)
- One place to capture timing → enables SLA assertions
- Response wrapped in a uniform object → assertion code is identical across services