import psutil
import time

from detector import (
    initialize_processes,
    detect_new_process
)

from settings import load_settings
from database import initialize_database
from logger import log_event
from email_service import send_alert
from session import load_session

from config import CHECK_INTERVAL

from database import get_enabled_rules

# ==========================================
# BLOCK PROCESS
# ==========================================

def block_process(pid):
    """
    Terminates the detected process.
    """

    try:

        psutil.Process(pid).kill()

        return "BLOCKED"

    except Exception:

        return "DETECTED"


# ==========================================
# MAIN MONITOR
# ==========================================

def monitor():
    """
    Main monitoring loop.

    Detects newly launched monitored processes,
    checks user authorization,
    blocks unauthorized threats,
    sends alerts,
    logs every event,
    and updates the dashboard.
    """

    print("=" * 55)
    print("🛡 Dark Web Threat Intelligence Monitor")
    print("=" * 55)

    print("\nMonitoring Started...\n")

    initialize_processes()

    print("✅ Existing processes remembered")
    print("👀 Waiting for newly launched monitored processes...\n")
    session = load_session()

    if session is None:
        print("⏳ No user is currently logged in.")
        print("👉 Please log in via the dashboard at http://localhost:8501")
        print("Waiting for login...")
        while session is None:
            time.sleep(2)
            session = load_session()
        print("✅ User session detected!")

    username = session["username"]

    role = session["role"]

    print(f"👤 Logged in User : {username}")
    print(f"🔐 Role : {role}")

    while True:

        settings = load_settings()

        pid, process_name = detect_new_process()

        if not pid:
            time.sleep(settings["refresh_interval"])
            continue

# ==========================================
# LOAD ENABLED RULES FROM DATABASE
# ==========================================

        rules = get_enabled_rules()

        if process_name not in rules:
            continue

        # ==========================================
        # CHECK SETTINGS
        # ==========================================

        if process_name == "chrome.exe" and not settings["monitor_chrome"]:
          continue

        if process_name == "msedge.exe" and not settings["monitor_edge"]:
            continue

        if process_name == "firefox.exe" and not settings["monitor_firefox"]:
            continue

        if process_name == "powershell.exe" and not settings["monitor_powershell"]:
            continue

        if process_name == "cmd.exe" and not settings["monitor_cmd"]:
            continue

        if process_name == "regedit.exe" and not settings["monitor_regedit"]:
            continue

        if process_name in ["tor.exe", "torbrowser.exe"] and not settings["monitor_tor"]:
            continue

        # ==========================================
        # PROCESS INFORMATION
        # ==========================================

        info = rules[process_name]
        category = info["category"]
        severity = info["severity"]
# ==========================================
# GET POLICY FOR THIS SEVERITY
# ==========================================

        policy_map = {
            "Low": settings["low_action"],
            "Medium": settings["medium_action"],
            "High": settings["high_action"],
            "Critical": settings["critical_action"]
        }

        policy = policy_map[severity]
        print("=" * 50)
        print("DEBUG")
        print("Severity :", severity)
        print("Policy   :", repr(policy))
        print("=" * 50)

        print(f"🛡 Policy : {policy}")

        print(f"⚠ Process  : {process_name}")
        print(f"📂 Category : {category}")
        print(f"🚨 Severity : {severity}")

# ==========================================
# APPLY SECURITY POLICY
# ==========================================

        action = "ALLOWED"

        # Log Only
        if policy == "Log":

            print("📝 Policy Action : Log Only")

        # Log + Email
        elif policy == "Log + Email":

            print("📧 Policy Action : Email Alert")

            action = "DETECTED"

            if settings["email_alerts"]:
                send_alert(username, process_name)

        # Email + Block
        elif policy == "Email + Block":

            print("🚫 Policy Action : Block + Email")

            if settings["auto_block"]:
                action = block_process(pid)
            else:
                action = "DETECTED"

            if settings["email_alerts"]:
                send_alert(username, process_name)

        # Block + Email
        elif policy == "Block + Email":

            print("🚨 Policy Action : Critical Block")

            if settings["auto_block"]:
                action = block_process(pid)
            else:
                action = "DETECTED"

            if settings["email_alerts"]:
                send_alert(username, process_name)
        # ==========================================
        # LOG EVENT
        # ==========================================

        log_event(
            username,
            process_name,
            category,
            severity,
            action
        )

        print("📝 Event Logged")

        print("-" * 55)

        time.sleep(settings["refresh_interval"])


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    initialize_database()

    monitor()