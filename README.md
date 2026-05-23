# Closira Backend Assignment

## Overview

This is a simulation of backend service for Closira to manages customer inquiries.

The system takes customer questions, processes them asynchronously behind the scenes, then match them with predefine Standard Operating Procedure (SOPs), tracks conversation history, allows for escalation to human agents, and even facilitates scheduling for follow-ups.

The aim of this implementation is to highlight key backend concepts, API design, asynchronous processing, database modeling, structured logging, and thoughtful engineering decision-making.

---

## Features

- Create inbound customer enquiries
- Asynchronous enquiry processing
- SOP matching using keyword-based rules
- Automatic escalation when no SOP matches
- Manual escalation endpoint
- Follow-up scheduling endpoint
- Full enquiry history and status timeline
- Structured JSON logging
- SQLite persistence using SQLAlchemy
- FastAPI auto-generated Swagger documentation

---

## Tech Stack

- Python 3.11+
- FastAPI
- SQLAlchemy
- SQLite
- FastAPI BackgroundTasks
- Pydantic
- Uvicorn
- python-json-logger

---

## Project Structure

```text
app/
    api/
        enquiry.py
    database/
        database.py
        dependencies.py
    logger/
        logger.py
    models/
        enquiry.py
        event.py
    schemas/
        enquiry.py
    services/
        background_tasks.py
        sop_matcher.py
main.py
requirements.txt
README.md
```

---

## Database Schema

### Enquiries

Stores the current state of each customer enquiry.

| Field | Description |
|---------|------------|
| id | Primary key |
| customer_name | Customer name |
| channel | WhatsApp / Email / Call |
| message | Original enquiry |
| status | processing / open / escalated |
| matched_sop | SOP matched during processing |
| suggested_response | Generated response suggestion |
| created_at | Creation timestamp |
| updated_at | Last update timestamp |

---

### Events

Stores the timeline/history of actions performed on an enquiry.

| Field | Description |
|---------|------------|
| id | Primary key |
| enquiry_id | Linked enquiry |
| event_type | Event category |
| details | Event description |
| created_at | Event timestamp |

Examples:

- ENQUIRY_CREATED
- SOP_MATCHED
- ESCALATED
- AUTO_ESCALATED
- FOLLOWUP_SCHEDULED

---

## API Endpoints

### Create Enquiry

```http
POST /enquiry
```

Request:

```json
{
  "customer_name": "John Doe",
  "channel": "whatsapp",
  "message": "What are your pricing plans?"
}
```

Response:

```json
{
  "enquiry_id": 1,
  "status": "processing"
}
```

---

### Schedule Follow-up

```http
POST /enquiry/{id}/follow-up
```

Request:

```json
{
  "delay_minutes": 30,
  "message_template": "Checking if you still need assistance."
}
```

---

### Escalate Enquiry

```http
POST /enquiry/{id}/escalate
```

Request:

```json
{
  "reason": "Customer requested human support"
}
```

---

### Enquiry History

```http
GET /enquiry/{id}/history
```

Returns enquiry details and full status timeline.

---

### Health Check

```http
GET /health
```

Response:

```json
{
  "status": "healthy"
}
```

---

## Running Locally

### Clone Repository

```bash
git clone <repository-url>
cd backend
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
uvicorn app.main:app --reload
```

Application:

```
http://127.0.0.1:8000
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## Async Processing Flow

1. Client creates enquiry using `POST /enquiry`
2. Enquiry stored with status `processing`
3. Background task is triggered
4. SOP matching runs against inbound message
5. If a match exists:
   - matched SOP stored
   - suggested response generated
   - status changed to `open`
6. If no match exists:
   - enquiry automatically escalated
   - event logged
7. History endpoint exposes the complete timeline

---

## SOP Matching Logic

The implementation uses simple keyword matching instead of AI.

Supported SOP categories:

- Pricing enquiry
- Booking enquiry
- Complaint
- After-hours enquiry
- Support request

Example:

Message:

```
What are your pricing plans?
```

Matched SOP:

```
pricing
```

Suggested response:

```
Thank you for your interest. Our team will share pricing details shortly.
```

---

## BackgroundTasks vs Celery

FastAPI BackgroundTasks was selected because:

- Simpler setup
- No external infrastructure required
- Appropriate for assignment scope
- Easier reviewer setup

Trade-offs:

- No retry mechanism
- No distributed workers
- Tasks are lost if the process crashes

For production workloads, Celery with Redis/RabbitMQ would be preferred.

---

## Database Choice

SQLite was selected because:

- Zero configuration
- Easy local execution
- Suitable for assignment-scale workloads

For production deployment PostgreSQL would be preferred due to:

- Better concurrency handling
- Advanced indexing
- Improved scalability
- Stronger operational tooling

---

## Structured Logging

JSON logs are emitted for key events:

- enquiry_created
- task_processing_started
- sop_matched
- auto_escalation_triggered
- manual_escalation
- followup_scheduled

Example:

```json
{
  "message": "sop_matched",
  "enquiry_id": 1,
  "matched_sop": "pricing"
}
```

---

## Error Handling

The API returns meaningful HTTP status codes.

Examples:

- 200 OK
- 404 Not Found
- 422 Validation Error

Unhandled exceptions are not exposed to clients.

---

## Future Improvements

- PostgreSQL support
- Celery + Redis task queue
- Retry handling
- Authentication & authorization
- Real follow-up scheduler
- AI-powered SOP classification
- Unit and integration testing
- Docker deployment
- Metrics and observability

---

## API Testing

Example API requests are provided in:

```text
tests/tests.http
```

The file contains sample requests for all assignment endpoints:

- GET /health
- POST /enquiry
- GET /enquiry/{id}
- POST /enquiry/{id}/escalate
- POST /enquiry/{id}/follow-up
- GET /enquiry/{id}/history

These requests can be executed directly using the VS Code REST Client extension or compatible HTTP clients.

---

## Author

**Apoorva Badoni**

Backend Assignment Submission for Breakout

GitHub: https://github.com/Oxide06