# CHANGES2.md

This document summarizes the improvements made in Task 2 – implementing a URL shortener API. The focus was to design a simple, secure, and testable Flask-based service that generates short URLs, handles redirection, tracks analytics, and exposes relevant API endpoints.

---

## Major Goals / Requirements

- Implement a minimal working URL shortener backend.
- Avoid using a database (in-memory model only).
- Follow API behavior as described in the provided README.
- Add validation, proper response codes, and basic analytics.
- Write simple and accurate test cases (similar to industry practice).

---

## Changes Made and Why

1. **Created `models.py`**  
   → Defined `URLStore` class using `dict` and `Lock()` for thread-safe in-memory storage.

2. **Created `utils.py`**  
   → Added short code generator and safe URL validator using `urlparse`.

3. **Refactored `main.py`**  
   → Used reusable functions for creating and redirecting short URLs.
   → Ensured appropriate status codes and error messages were returned.

4. **Added input validation**  
   → Invalid or missing URLs return HTTP 400 with clear error messages.

5. **Analytics support**  
   → Tracks number of clicks and creation time per short code.

6. **Test cases**  
   → Covered core functionality: creation, redirection, stats, and validation failures.

---

## Assumptions and Trade-offs

- In-memory store was used to keep the application stateless and database-free as per spec.
- `urlparse()` was chosen over regex for URL validation to avoid complexity.
- Short codes are generated randomly; no collision prediction is implemented beyond retries.
- Click stats are reset on app restart (due to no persistence layer).

---

## What I Would Do with More Time

- Add persistent storage (e.g., SQLite or Redis).
- Store short codes with expiration support.
- Add rate limiting for abuse protection.
- Create a frontend UI for testing.
- Add logging, monitoring, and error tracing.
- Improve test coverage with edge cases and performance scenarios.

---

## AI Usage

- **Tool**: ChatGPT (OpenAI)  
- **Purpose**: Used only for reviewing/refactoring utility structure, test format, and URL validation logic.  
- **Note**: All code was manually reviewed and adjusted to meet the assignment requirements. No AI-generated code was used directly without modification.
