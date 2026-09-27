import unittest

from src.database import initialize_database
from src.user import create_user
from src.budget import (
    set_budget,
    get_budget,
    get_monthly_expenses,
    get_budget_status
)
from src.expense import add_expense


class TestBudget(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        initialize_database()

        cls.user_id = create_user(
            "Budget Test User",
            "budget_test@example.com"
        )

    def test_set_budget(self):
        result = set_budget(
            self.user_id,
            "2026-09",
            5000
        )

        self.assertTrue(result)

    def test_get_budget(self):
        set_budget(
            self.user_id,
            "2026-09",
            5000
        )

        budget = get_budget(
            self.user_id,
            "2026-09"
        )

        self.assertIsNotNone(budget)
        self.assertEqual(budget["amount"], 5000)

    def test_monthly_expenses(self):
        add_expense(
            self.user_id,
            1000,
            "Food",
            "Test expense",
            "2026-09-26"
        )

        total = get_monthly_expenses(
            self.user_id,
            "2026-09"
        )

        self.assertGreaterEqual(total, 1000)

    def test_budget_status(self):
        set_budget(
            self.user_id,
            "2026-09",
            5000
        )

        status = get_budget_status(
            self.user_id,
            "2026-09"
        )

        self.assertIsNotNone(status)
        self.assertEqual(status["budget"], 5000)


if __name__ == "__main__":
    unittest.main()