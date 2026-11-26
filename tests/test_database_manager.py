import unittest
import os
import tempfile

from database.database_manager import DatabaseManager


class TestDatabaseManager(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(
            suffix=".db",
            delete=False
        )
        self.temp_db.close()

        self.db = DatabaseManager(self.temp_db.name)
        self.db.create_tables()

    def tearDown(self):
        os.unlink(self.temp_db.name)

    def test_save_result(self):
        result = {
            "id": 1,
            "sender": "customer@example.com",
            "subject": "Order Status",
            "category": "order",
            "priority": "normal",
            "reason": "Customer requests an order update."
        }

        self.db.save_result(result)

        saved = self.db.get_all_results()

        self.assertEqual(len(saved), 1)
        self.assertEqual(saved[0]["category"], "order")

    def test_update_result(self):
        result = {
            "id": 1,
            "sender": "customer@example.com",
            "subject": "Order Status",
            "category": "order",
            "priority": "normal",
            "reason": "Customer requests an order update."
        }

        self.db.save_result(result)

        result["priority"] = "high"
        self.db.save_result(result)

        saved = self.db.get_all_results()

        self.assertEqual(len(saved), 1)
        self.assertEqual(saved[0]["priority"], "high")


if __name__ == "__main__":
    unittest.main()