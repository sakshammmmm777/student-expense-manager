from .database import get_connection


def create_user(name, email):
    """Create a new user profile."""
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (name, email)
        )
        connection.commit()
        return cursor.lastrowid

    except Exception:
        connection.rollback()
        return None

    finally:
        connection.close()


def get_user(user_id):
    """Get a user by their ID."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    )

    user = cursor.fetchone()
    connection.close()

    return user


def update_user(user_id, name, email):
    """Update an existing user profile."""
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE users
            SET name = ?, email = ?
            WHERE id = ?
            """,
            (name, email, user_id)
        )

        connection.commit()
        return cursor.rowcount > 0

    except Exception:
        connection.rollback()
        return False

    finally:
        connection.close()
def get_user_by_email(email):
    """Find a user by email address."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM users
        WHERE email = ?
        """,
        (email.strip(),)
    )

    user = cursor.fetchone()
    connection.close()

    return user        