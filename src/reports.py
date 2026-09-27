from .database import get_connection


def get_total_expenses(user_id):
    """Calculate the total amount spent by a user."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COALESCE(SUM(amount), 0) AS total
        FROM expenses
        WHERE user_id = ?
        """,
        (user_id,)
    )

    result = cursor.fetchone()
    connection.close()

    return result["total"]


def get_category_summary(user_id):
    """Return total spending grouped by category."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT category, SUM(amount) AS total
        FROM expenses
        WHERE user_id = ?
        GROUP BY category
        ORDER BY total DESC
        """,
        (user_id,)
    )

    results = cursor.fetchall()
    connection.close()

    return results


def get_highest_expense(user_id):
    """Return the highest individual expense."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM expenses
        WHERE user_id = ?
        ORDER BY amount DESC
        LIMIT 1
        """,
        (user_id,)
    )

    result = cursor.fetchone()
    connection.close()

    return result


def get_monthly_summary(user_id, month):
    """Return spending summary for a particular month."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            COUNT(*) AS expense_count,
            COALESCE(SUM(amount), 0) AS total,
            COALESCE(AVG(amount), 0) AS average
        FROM expenses
        WHERE user_id = ?
        AND substr(expense_date, 1, 7) = ?
        """,
        (user_id, month)
    )

    result = cursor.fetchone()
    connection.close()

    return result