class Email:
    def __init__(
        self,
        id: int,
        sender: str,
        subject: str,
        body: str,
        gmail_id: str | None = None
    ):
        self.id = id
        self.sender = sender
        self.subject = subject
        self.body = body
        self.gmail_id = gmail_id

    def __str__(self):
        return f"{self.sender}: {self.subject}"