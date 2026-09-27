import unittest

from src.validation import (
    validate_name,
    validate_email,
    validate_amount
)


class TestValidation(unittest.TestCase):

    def test_valid_name(self):
        self.assertTrue(validate_name("Rahul Sharma"))

    def test_invalid_name(self):
        self.assertFalse(validate_name(""))

    def test_valid_email(self):
        self.assertTrue(validate_email("student@example.com"))

    def test_invalid_email(self):
        self.assertFalse(validate_email("student"))

    def test_valid_amount(self):
        self.assertTrue(validate_amount("500"))

    def test_invalid_amount(self):
        self.assertFalse(validate_amount("-100"))

    def test_non_numeric_amount(self):
        self.assertFalse(validate_amount("abc"))


if __name__ == "__main__":
    unittest.main()