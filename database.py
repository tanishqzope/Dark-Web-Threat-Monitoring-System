import sqlite3

DB_NAME = "darkweb_monitor.db"


# =====================================
# Database Connection
# =====================================

def get_connection():
    return sqlite3.connect(DB_NAME)


# =====================================
# Create Database
# =====================================

def initialize_database():
    """
    Creates the SQLite database
    and required tables if they
    do not already exist.
    """

    conn = get_connection()
    cursor = conn.cursor()

    # =====================================
    # Logs Table
    # =====================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        timestamp TEXT,

        user TEXT,

        process TEXT,

        category TEXT,

        severity TEXT,

        status TEXT

    )
    """)

# =====================================
# Threat Rules Table
# =====================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS threat_rules(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        process_name TEXT UNIQUE,

        category TEXT,

        severity TEXT,

        enabled INTEGER DEFAULT 1

    )
    """)

    conn.commit()
    conn.close()

    initialize_users_table()
    initialize_default_rules()

def initialize_users_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        role TEXT DEFAULT 'User',

        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()
# =====================================
# Default Threat Rules
# =====================================

def initialize_default_rules():

    conn = get_connection()
    cursor = conn.cursor()

    rules = [

        ("chrome.exe", "Browser", "Low", 1),
        ("msedge.exe", "Browser", "Low", 1),
        ("firefox.exe", "Browser", "Low", 1),
        ("brave.exe", "Browser", "Low", 1),
        ("powershell.exe", "Admin Tool", "Medium", 1),
        ("cmd.exe", "Admin Tool", "Medium", 1),
        ("regedit.exe", "System Tool", "High", 1),
        ("tor.exe", "Dark Web", "Critical", 1),
        ("torbrowser.exe", "Dark Web", "Critical", 1)

    ]

    cursor.executemany("""

    INSERT OR IGNORE INTO threat_rules(

        process_name,
        category,
        severity,
        enabled

    )

    VALUES(?,?,?,?)

    """, rules)

    conn.commit()
    conn.close()    
# =====================================
# Insert Log
# =====================================

def insert_log(
    timestamp,
    user,
    process,
    category,
    severity,
    status
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO logs(
        timestamp,
        user,
        process,
        category,
        severity,
        status
    )
    VALUES(?,?,?,?,?,?)
    """,
    (
        timestamp,
        user,
        process,
        category,
        severity,
        status
    ))

    conn.commit()
    conn.close()


# =====================================
# Fetch Logs
# =====================================

def fetch_logs():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        timestamp,
        user,
        process,
        category,
        severity,
        status
    FROM logs
    ORDER BY timestamp DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows
# =====================================
# Fetch Users
# =====================================

def fetch_users():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        username,
        email,
        role,
        created_at
    FROM users
    ORDER BY username
    """)

    users = cursor.fetchall()

    conn.close()

    return users


# =====================================
# Update Role
# =====================================

def update_role(username, role):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET role=?
        WHERE username=?
        """,
        (role, username)
    )

    conn.commit()

    conn.close()


# =====================================
# Delete User
# =====================================

def delete_user(username):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM users
        WHERE username=?
        """,
        (username,)
    )

    conn.commit()

    conn.close()
   
# =====================================
# Count Admins
# =====================================

def admin_count():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM users
    WHERE role='Admin'
    """)

    count = cursor.fetchone()[0]

    conn.close()

    return count
# =====================================
# Fetch Threat Rules
# =====================================

def fetch_rules():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        process_name,
        category,
        severity,
        enabled
    FROM threat_rules
    ORDER BY process_name
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows
# =====================================
# Add Threat Rule
# =====================================

def add_rule(process_name, category, severity):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO threat_rules(
        process_name,
        category,
        severity,
        enabled
    )
    VALUES(?,?,?,1)
    """,
    (
        process_name.lower(),
        category,
        severity
    ))

    conn.commit()
    conn.close()
# =====================================
# Update Threat Rule
# =====================================

def update_rule(rule_id, category, severity, enabled):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE threat_rules
        SET
            category=?,
            severity=?,
            enabled=?
        WHERE id=?
        """,
        (
            category,
            severity,
            int(enabled),
            int(rule_id)
        )
    )

    conn.commit()

    print("Rows Updated:", cursor.rowcount)   # Debug

    conn.close()
# =====================================
# Delete Threat Rule
# =====================================

def delete_rule(rule_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM threat_rules
        WHERE id=?
        """,
        (int(rule_id),)
    )

    conn.commit()

    print("Rows Deleted:", cursor.rowcount)   # Debug

    conn.close()
# =====================================
# Get Enabled Rules
# =====================================

def get_enabled_rules():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT

        process_name,

        category,

        severity

    FROM threat_rules

    WHERE enabled=1

    """)

    rows = cursor.fetchall()

    conn.close()

    rules = {}

    for process, category, severity in rows:

        rules[process] = {

            "category": category,

            "severity": severity

        }

    return rules           