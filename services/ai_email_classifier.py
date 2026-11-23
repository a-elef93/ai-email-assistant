import os

from dotenv import load_dotenv
from openai import OpenAI

from models.email import Email


class AIEmailClassifier:
    def __init__(self):
        load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is missing")

        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4.1-mini"

    def classify(self, email: Email) -> str:
        response = self.client.responses.create(
            model=self.model,
            instructions=(
                "You are an email classification assistant. "
                "Analyze the email and identify its category "
                "(order, support, or other), priority "
                "(high, normal, or low), and a short reason. "
                "Respond in English."
            ),
            input=(
                f"Subject: {email.subject}\n"
                f"Body: {email.body}"
            ),
            max_output_tokens=150
        )

        print(f"Input tokens: {response.usage.input_tokens}")
        print(f"Output tokens: {response.usage.output_tokens}")

        return response.output_text