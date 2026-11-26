import sqlite3
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

from database.database_manager import DatabaseManager
from models.email import Email
from models.email_analysis import EmailAnalysis
from services.email_classifier import EmailClassifier
from services.ai_email_classifier import AIEmailClassifier


app = FastAPI(
    title="AI Email Assistant API",
    version="1.0.0"
)


class EmailRequest(BaseModel):
    id: int
    sender: str
    subject: str
    body: str


class EmailRecord(EmailAnalysis):
    id: int
    sender: str
    subject: str


def get_database() -> DatabaseManager:
    db = DatabaseManager()
    db.create_tables()
    return db


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/analyze", response_model=EmailAnalysis)
def analyze_email(
    request: EmailRequest,
    mode: Literal["offline", "ai"] = "offline",
    db: DatabaseManager = Depends(get_database)
):
    email = Email(
        request.id,
        request.sender,
        request.subject,
        request.body
    )

    classifier = (
        AIEmailClassifier()
        if mode == "ai"
        else EmailClassifier()
    )

    try:
        analysis = classifier.classify(email)
    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail="Email classification service unavailable"
        ) from error

    result = {
        "id": email.id,
        "sender": email.sender,
        "subject": email.subject,
        **analysis.model_dump()
    }

    try:
        db.save_result(result)
    except sqlite3.Error as error:
        raise HTTPException(
            status_code=500,
            detail="Failed to save email result"
        ) from error

    return analysis


@app.get("/emails", response_model=list[EmailRecord])
def get_emails(
    db: DatabaseManager = Depends(get_database)
):
    try:
        return db.get_all_results()
    except sqlite3.Error as error:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve emails"
        ) from error