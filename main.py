import json

from models.email import Email
from services.email_classifier import EmailClassifier
from services.ai_email_classifier import AIEmailClassifier


USE_AI = False  # Change to True to enable OpenAI API


def main():
    with open("emails.json", "r", encoding="utf-8") as file:
        emails_data = json.load(file)

    if USE_AI:
        classifier = AIEmailClassifier()
    else:
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
            **analysis.model_dump()
        })

    with open("results.json", "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4)

    print(f"Successfully processed {len(results)} emails.")
    print(f"Mode: {'AI' if USE_AI else 'Offline'}")


if __name__ == "__main__":
    main()