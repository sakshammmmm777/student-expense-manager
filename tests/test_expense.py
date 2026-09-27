import unittest

from src.database import initialize_database, get_connection
from src.user import create_user
from src.expense import (
    add_expense,
    get_expenses,
    update_expense,
    delete_expense
)


class TestExpense(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        initialize_database()

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)",
            ("Test User", "test_expense@example.com")
        )

        connection.commit()

        cursor.execute(
            "SELECT id FROM users WHERE email = ?",
            ("test_expense@example.com",)
        )

        cls.user_id = cursor.fetchone()["id"]
        connection.close()

    def test_add_expense(self):
        expense_id = add_expense(
            self.user_id,
            500,
            "Food",
            "Test lunch",
            "2026-09-26"
        )

        self.assertIsNotNone(expense_id)

    def test_get_expenses(self):
        expenses = get_expenses(self.user_id)
        self.assertGreaterEqual(len(expenses), 1)

    def test_update_expense(self):
        expenses = get_expenses(self.user_id)
        expense_id = expenses[0]["id"]

        result = update_expense(
            expense_id,
            self.user_id,
            600,
            "Food",
            "Updated lunch",
            "2026-09-26"
        )

        self.assertTrue(result)

    def test_delete_expense(self):
        expense_id = add_expense(
            self.user_id,
            100,
            "Other",
            "Temporary expense",
            "2026-09-26"
        )

        result = delete_expense(expense_id, self.user_id)

        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()