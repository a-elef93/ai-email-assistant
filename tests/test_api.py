import unittest

from fastapi.testclient import TestClient
from api.app import app


class TestEmailAPI(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_health_check(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["status"], "healthy"
        )

    def test_analyze_email(self):
        email = {
            "id": 1,
            "sender": "customer@example.com",
            "subject": "Urgent Order Request",
            "body": "Please update me about my order."
        }

        response = self.client.post(
            "/analyze?mode=offline",
            json=email
        )

        self.assertEqual(response.status_code, 200)

        result = response.json()

        self.assertEqual(result["category"], "order")
        self.assertEqual(result["priority"], "high")
        self.assertIn("reason", result)

    def test_invalid_email(self):
        email = {
            "id": 2,
            "sender": "customer@example.com"
        }

        response = self.client.post(
            "/analyze?mode=offline",
            json=email
        )

        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()