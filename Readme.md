# Celestius Event Registration API

A REST API built with FastAPI and SQLite for managing registrations for the Celestius Backend Development Workshop.

## Features

- Register participants with name, email, college, and department.
- Validate email addresses and request data.
- Prevent duplicate email registrations.
- Enforce the event capacity limit of 50 participants.
- Retrieve all registrations with pagination.
- Retrieve an individual registration by ID.
- Automated tests using pytest and an isolated in-memory SQLite database.

## Tech Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Pytest

## Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd celestius-event-registration
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

## Run the API

```powershell
uvicorn app.main:app --reload
```

The API runs at `http://127.0.0.1:8000`.

Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check API status |
| POST | `/register` | Register a participant |
| GET | `/registrations` | List registrations |
| GET | `/registrations/{registration_id}` | Retrieve a registration by ID |

The registration list supports `skip` and `limit` query parameters.

## Run Tests

```powershell
python -m pytest -v
```

The tests use an in-memory SQLite database, separate from the application's local database.

## Example Registration Request

```json
{
  "name": "Arun Kumar",
  "email": "arun@example.com",
  "college": "CIT",
  "department": "CSBS"
}
```

A successful registration returns HTTP `201 Created`. Duplicate emails and full event capacity return HTTP `409 Conflict`. Invalid request data returns HTTP `422 Unprocessable Entity`.

## Database

The application creates a local SQLite database named `celestius.db` when it starts. The database file is excluded from version control.
