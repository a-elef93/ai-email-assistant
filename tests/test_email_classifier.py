import unittest

from models.email import Email
from services.email_classifier import EmailClassifier


class TestEmailClassifier(unittest.TestCase):

    def setUp(self):
        self.classifier = EmailClassifier()

    def test_order_classification(self):
        email = Email(
            1, "customer@example.com",
            "Order Status", "Where is my order?"
        )

        result = self.classifier.classify(email)

        self.assertEqual(result.category, "order")

    def test_support_classification(self):
        email = Email(
            2, "support@example.com",
            "Camera Issue", "My camera is not working."
        )

        result = self.classifier.classify(email)

        self.assertEqual(result.category, "support")

    def test_urgent_priority(self):
        email = Email(
            3, "customer@example.com",
            "Urgent Request", "Please contact me."
        )

        result = self.classifier.classify(email)

        self.assertEqual(result.priority, "high")


if __name__ == "__main__":
    unittest.main()