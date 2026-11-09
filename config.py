"""
=========================================================
Dark Web Threat Intelligence System Configuration
=========================================================
This file stores all configurable values used across
the project.
"""

# =========================================================
# DATABASE
# =========================================================

DATABASE_NAME = "darkweb_monitor.db"

# =========================================================
# FILES
# =========================================================

LOG_FILE = "log.txt"
USERS_FILE = "users_db.txt"

# =========================================================
# MONITORING
# =========================================================

CHECK_INTERVAL = 2          # Seconds between process scans
REFRESH_INTERVAL = 2000     # Streamlit refresh (milliseconds)
MAX_RECENT_ALERTS = 5

# =========================================================
# EMAIL
# =========================================================

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Sender/Password will move to .env later

# =========================================================
# PROCESS RISK SCORES
# =========================================================

CATEGORY_SCORE = {

    "Browser": 1,

    "Admin Tool": 3,

    "System Tool": 2,

    "Security Tool": 4,

    "Dark Web": 5

}

