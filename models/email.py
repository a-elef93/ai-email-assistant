class Email:
    def __init__(self, id: int, sender: str, subject: str, body: str):
        self.id = id
        self.sender = sender
        self.subject = subject
        self.body = body

    def __str__(self):
        return f"{self.sender}: {self.subject}"