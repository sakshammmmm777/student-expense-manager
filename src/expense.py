from .database import get_connection


def add_expense(user_id, amount, category, description, expense_date):
    """Add a new expense for a user."""
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO expenses
            (user_id, amount, category, description, expense_date)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, amount, category, description, expense_date)
        )

        connection.commit()
        return cursor.lastrowid

    except Exception:
        connection.rollback()
        return None

    finally:
        connection.close()


def get_expenses(user_id):
    """Return all expenses belonging to a user."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM expenses
        WHERE user_id = ?
        ORDER BY expense_date DESC, id DESC
        """,
        (user_id,)
    )

    expenses = cursor.fetchall()
    connection.close()

    return expenses


def get_expense(expense_id, user_id):
    """Get one specific expense."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM expenses
        WHERE id = ? AND user_id = ?
        """,
        (expense_id, user_id)
    )

    expense = cursor.fetchone()
    connection.close()

    return expense


def update_expense(
    expense_id,
    user_id,
    amount,
    category,
    description,
    expense_date
):
    """Update an existing expense."""
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE expenses
            SET amount = ?,
                category = ?,
                description = ?,
                expense_date = ?
            WHERE id = ? AND user_id = ?
            """,
            (
                amount,
                category,
                description,
                expense_date,
                expense_id,
                user_id
            )
        )

        connection.commit()
        return cursor.rowcount > 0

    except Exception:
        connection.rollback()
        return False

    finally:
        connection.close()


def delete_expense(expense_id, user_id):
    """Delete an expense."""
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM expenses
            WHERE id = ? AND user_id = ?
            """,
            (expense_id, user_id)
        )

        connection.commit()
        return cursor.rowcount > 0

    except Exception:
        connection.rollback()
        return False

    finally:
        connection.close()


def search_expenses(user_id, keyword):
    """Search expenses by category or description."""
    connection = get_connection()
    cursor = connection.cursor()

    search_term = f"%{keyword}%"

    cursor.execute(
        """
        SELECT * FROM expenses
        WHERE user_id = ?
        AND (category LIKE ? OR description LIKE ?)
        ORDER BY expense_date DESC
        """,
        (user_id, search_term, search_term)
    )

    expenses = cursor.fetchall()
    connection.close()

    return expenses