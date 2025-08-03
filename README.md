Secure User Management – Retain Coding Challenge
This repository contains solutions to the Retain coding challenge, which includes two independent tasks designed to assess skills in both refactoring legacy code and implementing a new feature from scratch.

## Repository Structure

secure-user-management/
│
├── assignments/
│ ├── messy-migration/ # Task 1: Refactored User Management API
│ │ ├── app.py
│ │ ├── init_db.py
│ │ ├── requirements.txt
│ │ ├── users.db
│ │ └── CHANGES.md
│ │
│ └── url-shortener/ # Task 2: URL Shortener Service
│ ├── app/
│ │ ├── main.py
│ │ ├── models.py
│ │ └── utils.py
│ ├── tests/
│ │ └── test_basic.py
│ ├── requirements.txt
│ └── CHANGES2.md
│
└── README.md # Repository overview (this file)

Task 1: Code Refactoring Challenge
Objective
You are provided with a legacy Flask-based user management API that is functional but poorly written. The goal is to refactor this application to enhance its structure, improve security, and adopt best practices, without adding new features.

Prerequisites
Python 3.8 or higher
Setup Instructions
Navigate to the project directory:

cd assignments/messy-migration
Install the dependencies:

pip install -r requirements.txt
Initialize the SQLite database:

python init_db.py
Start the application:

python app.py
Access the API at: http://localhost:5000

Available API Endpoints
GET / – Health check
GET /users – List all users
GET /user/<id> – Retrieve a specific user
POST /users – Add a new user
PUT /user/<id> – Update user information
DELETE /user/<id> – Delete a user
GET /search?name=<name> – Search for users by name
POST /login – User login
Key Improvements Implemented
Parameterized SQL queries to prevent injection
Passwords securely hashed using Werkzeug
Input validation and error handling added
Consistent JSON responses with proper status codes
Clearer and more maintainable code structure
Refer to CHANGES.md for detailed documentation of changes, decisions, and trade-offs.

Task 2: URL Shortener Service
Objective
Design and implement a basic URL shortening service similar to bit.ly. The goal is to develop a simple, robust API with endpoints for shortening URLs, redirecting to the original link, and viewing analytics.

Prerequisites
Python 3.8 or higher
Setup Instructions
Navigate to the project directory:

cd assignments/url-shortener
Install the dependencies:

pip install -r requirements.txt
Start the application:

python -m flask --app app.main run
Run the tests:

pytest
Access the API at: http://localhost:5000

Core Features Implemented
POST /api/shorten: Accepts a long URL and returns a 6-character short code
GET /<short_code>: Redirects to the original URL if found
GET /api/stats/<short_code>: Returns analytics (click count, timestamp, original URL)
Technical Highlights
URL validation
In-memory storage using Python dictionaries
Thread-safe click tracking
Comprehensive test coverage for core functionality
Refer to CHANGES2.md for additional implementation notes and justifications.

AI Usage Disclosure
Tool Used: ChatGPT (OpenAI)
Purpose: Used for reviewing and improving code structure, identifying common vulnerabilities, and validating architectural decisions
Note: All logic was manually implemented and modified to meet the assignment requirements. No AI-generated code was used without human review and adaptation.
Submission Guidelines
All code and database files are included in this repository.
Both app.py and Flask services run as expected after setup.
For additional documentation, refer to the respective CHANGES.md files in each task folder.
