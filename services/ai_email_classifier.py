import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from typing import Literal

from models.email import Email


class EmailAnalysis(BaseModel):
    category: Literal["order", "support", "other"]
    priority: Literal["high", "normal", "low"]
    reason: str


class AIEmailClassifier:
    def __init__(self):
        load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is missing")

        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4.1-mini"

    def classify(self, email: Email) -> EmailAnalysis:
        response = self.client.responses.parse(
            model=self.model,
            instructions=(
                "You are an email classification assistant. "
                "Analyze the email and classify it as order, support, or other. "
                "Assign priority as high, normal, or low. "
                "Provide a short reason in English."
            ),
            input=(
                f"Subject: {email.subject}\n"
                f"Body: {email.body}"
            ),
            text_format=EmailAnalysis,
            max_output_tokens=200
        )

        if response.output_parsed is None:
            raise ValueError("AI response could not be parsed")

        print(f"Input tokens: {response.usage.input_tokens}")
        print(f"Output tokens: {response.usage.output_tokens}")

        return response.output_parsed