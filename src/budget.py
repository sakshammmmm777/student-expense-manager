from .database import get_connection


def set_budget(user_id, month, amount):
    """Create or update a monthly budget."""
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO budgets (user_id, month, amount)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id, month)
            DO UPDATE SET amount = excluded.amount
            """,
            (user_id, month, amount)
        )

        connection.commit()
        return True

    except Exception:
        connection.rollback()
        return False

    finally:
        connection.close()


def get_budget(user_id, month):
    """Get the budget for a specific month."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM budgets
        WHERE user_id = ? AND month = ?
        """,
        (user_id, month)
    )

    budget = cursor.fetchone()
    connection.close()

    return budget


def get_monthly_expenses(user_id, month):
    """Calculate total expenses for a specific month."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COALESCE(SUM(amount), 0) AS total
        FROM expenses
        WHERE user_id = ?
        AND substr(expense_date, 1, 7) = ?
        """,
        (user_id, month)
    )

    result = cursor.fetchone()
    connection.close()

    return result["total"]


def get_budget_status(user_id, month):
    """Return budget, spending, remaining amount and status."""
    budget = get_budget(user_id, month)

    if budget is None:
        return None

    spent = get_monthly_expenses(user_id, month)
    budget_amount = budget["amount"]
    remaining = budget_amount - spent

    if remaining < 0:
        status = "OVER BUDGET"
    elif remaining == 0:
        status = "BUDGET REACHED"
    else:
        status = "WITHIN BUDGET"

    return {
        "budget": budget_amount,
        "spent": spent,
        "remaining": remaining,
        "status": status
    }