import unittest
import os
import tempfile

from api.app import get_database
from database.database_manager import DatabaseManager

from fastapi.testclient import TestClient
from api.app import app


class TestEmailAPI(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.TemporaryDirectory()
        self.db = DatabaseManager(
            os.path.join(self.temp_db.name, "test_emails.db")
        )
        self.db.create_tables()

        app.dependency_overrides[get_database] = lambda: self.db
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()
        self.temp_db.cleanup()

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

    def test_analyze_and_save_email(self):
        email = {
            "id": 10,
            "sender": "customer@example.com",
            "subject": "Urgent Camera Problem",
            "body": "My security camera system is not working."
        }

        response = self.client.post(
            "/analyze?mode=offline",
            json=email
        )

        self.assertEqual(response.status_code, 200)

        response = self.client.get("/emails")

        self.assertEqual(response.status_code, 200)

        saved_emails = response.json()

        self.assertEqual(len(saved_emails), 1)
        self.assertEqual(saved_emails[0]["id"], 10)
        self.assertEqual(saved_emails[0]["category"], "support")
        self.assertEqual(saved_emails[0]["priority"], "high")




if __name__ == "__main__":
    unittest.main()