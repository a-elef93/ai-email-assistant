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


results = []

for email in emails:
    analysis = analyze_email(email["subject"], email["body"])

    result = {
        "id": email["id"],
        "sender": email["sender"],
        "subject": email["subject"],
        "category": analysis["category"],
        "priority": analysis["priority"]
    }

    results.append(result)

with open("results.json", "w", encoding="utf-8") as file:
    json.dump(results, file, indent=4)

print(f"Successfully processed {len(results)} emails.")