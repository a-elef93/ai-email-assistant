from models.email import Email
from services.ai_email_classifier import AIEmailClassifier


email = Email(
    1,
    "customer@example.com",
    "Security Camera Issue",
    "My cameras stopped recording last night. "
    "I need someone to fix this as soon as possible."
)

classifier = AIEmailClassifier()
result = classifier.classify(email)

print("\nAI Analysis:")
print(f"Category: {result.category}")
print(f"Priority: {result.priority}")
print(f"Reason: {result.reason}")

print("\nJSON Output:")
print(result.model_dump_json(indent=4))