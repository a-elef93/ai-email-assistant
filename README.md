# AI Email Assistant

A Python-based email classification and automation project that combines **object-oriented programming**, **OpenAI-powered analysis**, **structured outputs**, **SQLite persistence**, and a **FastAPI REST API**.

The application can categorize incoming emails, assign a priority, and explain its classification. It supports a free, rule-based **offline mode** and an **AI mode** that makes billable OpenAI API requests.

> **Project status:** Backend development in progress. The classification API, local JSON workflow, and SQLite storage are implemented. Email-provider integration, automated replies, and deployment are planned—not yet implemented.

## Features

- **Email classification:** `order`, `support`, or `other`
- **Priority detection:** `high`, `normal`, or `low`
- **Two classification modes:** offline keyword matching or OpenAI API
- **Structured AI output:** validated with Pydantic (`EmailAnalysis`)
- **JSON workflow:** read sample messages from `emails.json` and write `results.json`
- **SQLite persistence:** insert or update classification results using `DatabaseManager`
- **REST API:** FastAPI endpoints with request validation and interactive Swagger docs
- **Logging and error handling:** local processing continues when individual emails fail
- **Automated tests:** `unittest` and FastAPI `TestClient`

## Technology Stack

- Python 3
- OpenAI Python SDK (Responses API; configured with `gpt-4.1-mini`)
- FastAPI and Uvicorn
- Pydantic
- SQLite (`sqlite3`)
- `python-dotenv`
- `unittest` and `httpx` (for API tests)
- Git and GitHub

## Project Structure

```text
email-assistant/
├── api/
│   ├── __init__.py
│   └── app.py
├── database/
│   ├── __init__.py
│   └── database_manager.py
├── models/
│   ├── __init__.py
│   ├── email.py
│   └── email_analysis.py
├── services/
│   ├── __init__.py
│   ├── email_classifier.py
│   └── ai_email_classifier.py
├── tests/
│   ├── test_api.py
│   ├── test_email_classifier.py
│   └── test_database_manager.py  # If added locally; check test discovery
├── utils/
│   ├── __init__.py
│   └── logger.py
├── main.py
├── test_ai.py
├── emails.json
├── results.json
├── requirements.txt
├── .gitignore
└── README.md
```

`test_database_manager.py` was planned during development, but the latest reported test run did not discover it. Verify that the file exists and is named correctly before treating its tests as part of the passing suite.

## Getting Started

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd email-assistant
```

Replace `<YOUR_REPOSITORY_URL>` with your GitHub repository URL.

### 2. Create a virtual environment

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Set your API key (only for AI mode)

Create a `.env` file in the project root:

```dotenv
OPENAI_API_KEY=your_openai_api_key_here
```

The `.env` file is excluded from Git. **Never commit or share your secret key.** Offline mode does not require an API key for classification, although the installed AI module is still imported by the current application.

## Run the Local Email Processor

In `main.py`, select a mode:

```python
USE_AI = False  # Offline mode; no OpenAI API charges
# USE_AI = True  # AI mode; sends requests to OpenAI
```

Then run:

```bash
python main.py
```

The processor reads sample messages from `emails.json`, classifies them, writes `results.json`, and saves results to the local SQLite file `emails.db`.

> SQLite files are ignored by Git. The local processor and REST API currently have separate workflows: the API's `/analyze` endpoint does **not yet** save requests to SQLite.

## Run the REST API

Start the development server from the project root:

```bash
python -m uvicorn api.app:app --reload --host 127.0.0.1
```

Open the interactive API documentation:

- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI schema: http://127.0.0.1:8000/openapi.json

### Health check

```http
GET /health
```

Example response:

```json
{"status": "healthy"}
```

### Classify an email (offline mode)

```http
POST /analyze?mode=offline
Content-Type: application/json
```

Request body:

```json
{
  "id": 1,
  "sender": "customer@example.com",
  "subject": "Urgent Order Request",
  "body": "Please update me about my order as soon as possible."
}
```

Example response:

```json
{
  "category": "order",
  "priority": "high",
  "reason": "Classified using predefined keyword rules."
}
```

Try the same request using `curl`:

```bash
curl -X POST 'http://127.0.0.1:8000/analyze?mode=offline' \
  -H 'Content-Type: application/json' \
  -d '{
    "id": 1,
    "sender": "customer@example.com",
    "subject": "Urgent Order Request",
    "body": "Please update me about my order as soon as possible."
  }'
```

To use the AI classifier instead, change the query parameter to `mode=ai` **only when you intend to make a billable API request**.

## Run the Tests

From the repository root:

```bash
python -m unittest discover -s tests -v
```

**Latest verified local result (November 23, 2026): 6 tests passed**—three email-classifier tests and three API tests. The two planned database tests were **not shown** in test discovery, so they are not counted as passing.

The automated API tests run in offline mode and do not call the OpenAI API.

## Design Overview

```text
                         +--------------------+
Sample emails.json ----->|      main.py       |-----> results.json
                         +---------+----------+
                                   |
                          Offline or AI mode
                                   |
                   +---------------+---------------+
                   |                               |
          +--------v---------+            +--------v----------+
          | EmailClassifier  |            | AIEmailClassifier  |
          | Keyword rules    |            | OpenAI Responses   |
          +--------+---------+            +--------+----------+
                   |                               |
                   +---------------+---------------+
                                   |
                            EmailAnalysis
                          (Pydantic model)
                                   |
                            SQLite database

HTTP client ---> FastAPI /analyze ---> classifier ---> EmailAnalysis response
                  (SQLite persistence for API requests: planned)
```

### Core classes

| Component | Responsibility |
| --- | --- |
| `Email` | Represent an email using constructor-initialized attributes |
| `EmailAnalysis` | Validate category, priority, and explanation |
| `EmailClassifier` | Apply local keyword rules |
| `AIEmailClassifier` | Call OpenAI's Responses API and parse structured results |
| `DatabaseManager` | Create tables, upsert results, and query SQLite |

Both classifiers expose a `classify(email)` method returning the same `EmailAnalysis` type. This lets the local processor switch between offline and AI modes without changing the result-handling logic.

## Security and Cost Notes

- **Never commit** `.env`, API keys, customer email content, or local database files.
- Check your OpenAI API credit balance and pricing before enabling AI mode.
- Every actual AI request may incur a usage-based charge; offline classification and local unit tests do not.
- API mode is currently intended for **local development only**. There is no authentication or usage-control layer for `/analyze?mode=ai`; do not expose it publicly in this state.
- The API currently returns a generic HTTP 503 on classification exceptions. More specific error handling and retry policies are future improvements.
- Use synthetic, English-language email examples during development.

## Roadmap

- [x] Rule-based email classification
- [x] JSON input/output
- [x] Object-oriented Python classes
- [x] OpenAI API integration
- [x] Pydantic structured responses
- [x] Offline/AI processing modes
- [x] Application logging and error handling
- [x] SQLite storage for the local processor
- [x] FastAPI `/health` and `/analyze` endpoints
- [x] Offline API tests
- [ ] Verify and complete SQLite test discovery
- [ ] Persist API requests/results to SQLite and add `GET /emails`
- [ ] Add API authentication and protect AI usage
- [ ] Add automated reply drafts requiring human approval
- [ ] Integrate an email provider and n8n workflows
- [ ] Dockerize the application
- [ ] Add GitHub Actions CI/CD
- [ ] Deploy to Azure and manage infrastructure with Terraform
- [ ] Add monitoring and security checks

## Learning Goals

This project is being built as a practical portfolio exercise covering **Python OOP, HTTP APIs, AI integration, databases, automated testing, and eventually DevOps workflows**.

---

**Note:** This README documents the implementation through Step 19 of the project. Features marked as planned are not yet available.
