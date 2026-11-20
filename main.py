def analyze_email(subject: str, body: str) -> dict[str, str]:
    text = f"{subject}\n{body}".casefold()

    category = "other"
    if "παραγγελία" in text:
        category = "order"
    elif "δεν λειτουργεί" in text:
        category = "support"

    priority = "normal"
    if "επείγον" in text:
        priority = "high"

    return {"category": category, "priority": priority}


result = analyze_email(
    subject=" Παραγγελία για αύριο",
    body="Μπορείτε να μου επιβεβαιώσετε αν θα παραδοθεί αύριο;",
)

print(result)