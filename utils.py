import pandas as pd
from database import fetch_logs
from config import CATEGORY_SCORE

# =====================================
# Load Logs from SQLite
# =====================================

def load_logs():

    rows = fetch_logs()

    df = pd.DataFrame(
        rows,
        columns=[
            "Timestamp",
            "User",
            "Process",
            "Category",
            "Severity",
            "Status"
        ]
    )

    if not df.empty:

        df["Timestamp"] = pd.to_datetime(
            df["Timestamp"],
            errors="coerce"
        )

    return df


# =====================================
# Threat Score
# =====================================


def calculate_threat_score(df):

    if df.empty:
        return 0

    score = 0

    for category in df["Category"]:

        score += CATEGORY_SCORE.get(category, 1)

    return score


# =====================================
# Threat Level
# =====================================

def threat_level(score):

    if score < 10:
        return "LOW"

    elif score < 25:
        return "MEDIUM"

    elif score < 50:
        return "HIGH"

    else:
        return "CRITICAL"


# =====================================
# Filter Logs
# =====================================

def filter_logs(
        df,
        user=None,
        process=None,
        category=None,
        severity=None,
        status=None
):

    temp = df.copy()

    if user:
        temp = temp[temp["User"] == user]

    if process:
        temp = temp[temp["Process"] == process]

    if category:
        temp = temp[temp["Category"] == category]

    if severity:
        temp = temp[temp["Severity"] == severity]

    if status:
        temp = temp[temp["Status"] == status]

    return temp


# =====================================
# Export CSV
# =====================================

def export_csv(df):

    return df.to_csv(index=False).encode("utf-8")