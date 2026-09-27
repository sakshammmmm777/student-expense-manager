def validate_name(name):
    """Validate a user's name."""
    name = name.strip()

    if not name:
        return False

    if not all(char.isalpha() or char.isspace() for char in name):
        return False

    return True


def validate_email(email):
    """Very basic email check – just looks for @ and a dot after it."""
    email = email.strip()

    return "@" in email and "." in email.split("@")[-1]


def validate_amount(amount):
    """Validate an expense or budget amount."""
    try:
        amount = float(amount)
        return amount > 0
    except (ValueError, TypeError):
        return False