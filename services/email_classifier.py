from models.email import Email


class EmailClassifier:
    def __init__(self):
        self.categories = ["order", "support", "other"]

    def classify(self, email: Email) -> dict[str, str]:
        text = f"{email.subject}\n{email.body}".casefold()

        category = "other"

        if "order" in text:
            category = "order"
        elif "not working" in text:
            category = "support"

        priority = "normal"

        if "urgent" in text:
            priority = "high"

        return {"category": category, "priority": priority}