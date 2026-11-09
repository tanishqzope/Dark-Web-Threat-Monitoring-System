from database import get_connection

username = input("Enter username to promote: ")

conn = get_connection()
cursor = conn.cursor()

cursor.execute(
    """
    UPDATE users
    SET role='Admin'
    WHERE username=?
    """,
    (username,)
)

conn.commit()
conn.close()

print("✅ User promoted to Admin")