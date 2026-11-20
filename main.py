import json

from models.email import Email
from services.email_classifier import EmailClassifier


with open("emails.json", "r", encoding="utf-8") as file:
    emails_data = json.load(file)

classifier = EmailClassifier()
results = []

for data in emails_data:
    email = Email(
        data["id"],
        data["sender"],
        data["subject"],
        data["body"]
    )

    analysis = classifier.classify(email)

    results.append({
        "id": email.id,
        "sender": email.sender,
        "subject": email.subject,
        "category": analysis["category"],
        "priority": analysis["priority"]
    })

with open("results.json", "w", encoding="utf-8") as file:
    json.dump(results, file, indent=4)

print(f"Successfully processed {len(results)} emails.")