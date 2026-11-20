import json


def analyze_email(subject: str, body: str) -> dict[str, str]:
    text = f"{subject}\n{body}".casefold()

    category = "other"

    if "order" in text:
        category = "order"
    elif "not working" in text:
        category = "support"

    priority = "normal"

    if "urgent" in text:
        priority = "high"

    return {"category": category, "priority": priority}


with open("emails.json", "r", encoding="utf-8") as file:
    emails = json.load(file)


for email in emails:
    result = analyze_email(email["subject"], email["body"])

    print(f"ID: {email['id']}")
    print(f"From: {email['sender']}")
    print(f"Subject: {email['subject']}")
    print(f"Category: {result['category']}")
    print(f"Priority: {result['priority']}")
    print("-" * 30)