import json

from models.email import Email
from services.email_classifier import EmailClassifier
from services.ai_email_classifier import AIEmailClassifier
from utils.logger import setup_logger


USE_AI = False

logger = setup_logger()


def main():
    try:
        with open("emails.json", "r", encoding="utf-8") as file:
            emails_data = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError) as error:
        logger.error("Failed to load emails: %s", error)
        return

    classifier = AIEmailClassifier() if USE_AI else EmailClassifier()

    results = []

    for data in emails_data:
        try:
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

            logger.info("Email %s processed successfully", email.id)

        except (KeyError, TypeError, ValueError) as error:
            logger.error("Invalid email data: %s", type(error).__name__)

        except Exception as error:
            logger.error(
                "Email processing failed: %s",
                type(error).__name__
            )

    try:
        with open("results.json", "w", encoding="utf-8") as file:
            json.dump(results, file, indent=4)

    except OSError as error:
        logger.error("Failed to save results: %s", error)
        return

    logger.info("Successfully processed %s emails", len(results))
    logger.info("Mode: %s", "AI" if USE_AI else "Offline")


if __name__ == "__main__":
    main()