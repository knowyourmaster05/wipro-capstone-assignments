# Viva Q&A

**Q: What does the framework do?**
A: Automates the User Management, Authentication, and Product Catalog APIs
of AutomationExercise, with contract validation on JSONPlaceholder. Writes
MySQL mirrors, and produces Allure reports.

**Q: Why two APIs?**
A: To prove the framework is service-agnostic — the same client, the same
validators, the same style works on completely different endpoints.

**Q: What does the framework NOT do?**
A: No UI automation (that is Milestone 1). No Robot Framework (Milestone 3).
Both could be added without touching the service layer.

**Q: How do you ensure scenarios are independent?**
A: PayloadFactory generates unique emails; `after_scenario` cleans up;
MySQL rows are removed on delete.

**Q: How do you handle sensitive data in logs?**
A: `BaseClient._mask()` replaces password, token, authorization, api_key,
secret fields with `***` before logging.

**Q: What happens if the API is down?**
A: `BaseClient._request` retries on 429/5xx with exponential backoff, up to
3 attempts, then raises a ConnectionError with context.

**Q: Why assert body code in addition to HTTP status?**
A: AutomationExercise returns HTTP 200 even for business errors (400/404/405
in the body). Relying on HTTP alone would let bugs slip through.

**Q: What is the role of schemas?**
A: Contract validation. They live in the framework, not in tests, and can be
updated independently to detect API drift.

**Q: What did you learn?**
A: That a framework's value comes from its layering — session handling,
retry logic, and assertion helpers are what turn a script into a product.