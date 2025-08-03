# CHANGES.md

This document explains the changes made to the original user management API as part of Task 1 in the code refactoring challenge. The focus was on improving code quality, security, and maintainability without changing the existing functionality or adding new features.

---

## Major Issues Identified

1. **SQL Injection Vulnerability**  
   All database queries used string formatting (e.g., `f"SELECT * FROM users WHERE id = '{user_id}'"`), which is unsafe and exposes the system to SQL injection attacks.

2. **Lack of Input Validation**  
   The API trusted user input without checking for required fields, data types, or structure, which could lead to invalid or unexpected behavior.

3. **Plain-Text Password Storage**  
   User passwords were stored in the database without any encryption or hashing, making it insecure.

4. **Improper HTTP Status Codes and Response Format**  
   Several endpoints returned plain text instead of JSON responses, and used incorrect or missing status codes.

5. **Poor Code Readability and Hardcoded Values**  
   Variable names were unclear, strings were hardcoded, and logic was repeated across endpoints.

6. **No Error Handling**  
   Errors like missing keys, malformed requests, or database exceptions were not handled, which could crash the application.

---

## Changes Made and Why

1. **Replaced all SQL queries with parameterized queries** using `?` placeholders to prevent SQL injection.

2. **Added input validation** for request bodies. Each POST and PUT endpoint now checks for required fields and handles missing or invalid data properly.

3. **Implemented password hashing** using Werkzeug’s `generate_password_hash` and `check_password_hash` to securely store and verify passwords.

4. **Used JSON responses with appropriate HTTP status codes**. All endpoints now return structured JSON data with proper success or error codes like 200, 201, 400, and 404.

5. **Improved code readability** by using descriptive variable names and reducing redundant code.

6. **Added error handling** for invalid inputs, database errors, and non-existent users using try-except blocks.

---

## Assumptions and Trade-offs

- The application was kept in a single file (`app.py`) as the original structure did not include modular design. Modularization was avoided to maintain simplicity.

- Schema validation libraries (like Marshmallow or Pydantic) were not added to keep dependencies minimal.

- Email uniqueness or format validation was not enforced in the database schema.

- The existing SQLite database and schema were used without modification.

---

## What I Would Do with More Time

- Split the code into multiple modules such as `routes.py`, `db.py`, and `utils.py` for better organization.

- Add automated tests using `pytest` to test all endpoints with valid and invalid input.

- Add email format validation and unique constraints.

- Implement token-based authentication (e.g., JWT) for secure login.

- Use environment variables for sensitive configurations like database paths or secret keys.

- Add centralized logging instead of print statements.

---
## Architecture Diagram

Below is a high-level view of the current Flask-based API architecture after refactoring:
```
+-----------------------+
|     HTTP Client       |
|  (Postman / Browser)  |
+----------+------------+
            |
            v
+-----------------------+
|      Flask App        |
|      (app.py)         |
+----------+------------+
            |
+----------------------+----------------------+
|                      |                     |
v                      v                     v
[Input Validation] [Endpoint Handlers] [Password Hashing]
(Request)    (GET, POST, etc.)   (Login/Auth Logic)
             |
             v
+-----------------------+
|      SQLite DB        |
|    (users.db file)    |
+-----------------------+
```

- The Flask application processes incoming HTTP requests using defined routes.
- Input validation ensures safe and complete data before processing.
- Passwords are hashed securely using Werkzeug before being stored or verified.
- SQLite database (`users.db`) stores user records and handles persistence.

## AI Usage

- **Tool Used**: ChatGPT (OpenAI)  
- **Purpose**: Used for reviewing and validating improvements related to API structure, input validation, and security practices (such as password hashing and query safety).  
- **Approach**: All API logic and refactored code were manually written and reviewed. ChatGPT was only used to guide improvements and suggest best practices — no code was directly copied without being adapted and edited to meet the assignment’s functional and structural goals.

---
