from models.email import Email
from models.email_analysis import EmailAnalysis


class EmailClassifier:
    def __init__(self):
        self.categories = ["order", "support", "other"]

    def classify(self, email: Email) -> EmailAnalysis:
        text = f"{email.subject}\n{email.body}".casefold()

        category = "other"

        if "order" in text:
            category = "order"
        elif "not working" in text:
            category = "support"

        priority = "normal"

        if "urgent" in text:
            priority = "high"

        return EmailAnalysis(
            category=category,
            priority=priority,
            reason="Classified using predefined keyword rules."
        )