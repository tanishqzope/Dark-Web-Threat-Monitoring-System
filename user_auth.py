import bcrypt
from datetime import datetime

from database import get_connection


# ==========================================
# REGISTER USER
# ==========================================

def register_user(username, email, password):

    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    try:

        cursor.execute(
            """
            INSERT INTO users
            (
                username,
                email,
                password,
                created_at
            )

            VALUES (?,?,?,?)
            """,
            (
                username,
                email,
                hashed_password,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )

        conn.commit()

        return True

    except Exception as e:

        print("Registration Error:", e)

        return False

    finally:

        conn.close()


# ==========================================
# LOGIN USER
# ==========================================

def login_user(username, password):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT password, role
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    stored_hash, role = row

    if bcrypt.checkpw(
        password.encode(),
        stored_hash.encode()
    ):

        return role

    return None