import json
import os

SETTINGS_FILE = "settings.json"

# ==========================================
# DEFAULT SETTINGS
# ==========================================

DEFAULT_SETTINGS = {

    # Process Monitoring
    "monitor_chrome": True,
    "monitor_edge": True,
    "monitor_firefox": True,
    "monitor_powershell": True,
    "monitor_cmd": True,
    "monitor_regedit": True,
    "monitor_tor": True,

    # Security
    "email_alerts": True,
    "auto_block": True,
    "refresh_interval": 2,

    # Security Policy
    "low_action": "Log",
    "medium_action": "Log + Email",
    "high_action": "Email + Block",
    "critical_action": "Block + Email"
}


# ==========================================
# LOAD SETTINGS
# ==========================================

def load_settings():

    if not os.path.exists(SETTINGS_FILE):

        save_settings(DEFAULT_SETTINGS)

        return DEFAULT_SETTINGS.copy()

    with open(SETTINGS_FILE, "r") as file:

        settings = json.load(file)

    # Add any missing settings (helps after upgrades)
    for key, value in DEFAULT_SETTINGS.items():

        if key not in settings:

            settings[key] = value

    return settings


# ==========================================
# SAVE SETTINGS
# ==========================================

def save_settings(settings):

    with open(SETTINGS_FILE, "w") as file:

        json.dump(settings, file, indent=4)