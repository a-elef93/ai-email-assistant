from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/analyze", response_model=EmailAnalysis)
def analyze_email(
    request: EmailRequest,
    mode: Literal["offline", "ai"] = "offline"
):
    email = Email(
        request.id,
        request.sender,
        request.subject,
        request.body
    )

    if mode == "ai":
        classifier = AIEmailClassifier()
    else:
        classifier = EmailClassifier()

    try:
        return classifier.classify(email)

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Email classification service unavailable"
        )