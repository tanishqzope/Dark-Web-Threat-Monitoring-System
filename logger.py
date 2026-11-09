from datetime import datetime
from database import insert_log


def log_event(
    user,
    process,
    category,
    severity,
    status
):
    """
    Stores a security event in the SQLite database.
    """

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    insert_log(
        timestamp,
        user,
        process,
        category,
        severity,
        status
    )