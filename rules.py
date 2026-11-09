PROCESS_INFO = {

    "chrome.exe": {
        "category": "Browser",
        "severity": "Low",
        "action": "ALLOW"
    },

    "msedge.exe": {
        "category": "Browser",
        "severity": "Low",
        "action": "ALLOW"
    },

    "firefox.exe": {
        "category": "Browser",
        "severity": "Low",
        "action": "ALLOW"
    },

    "brave.exe": {
        "category": "Browser",
        "severity": "Low",
        "action": "ALLOW"
    },

    "powershell.exe": {
        "category": "Admin Tool",
        "severity": "Medium",
        "action": "ALERT"
    },

    "cmd.exe": {
        "category": "Admin Tool",
        "severity": "Medium",
        "action": "ALERT"
    },

    "regedit.exe": {
        "category": "System Tool",
        "severity": "High",
        "action": "ALERT"
    },

    "tor.exe": {
        "category": "Dark Web",
        "severity": "Critical",
        "action": "BLOCK"
    },

    "torbrowser.exe": {
        "category": "Dark Web",
        "severity": "Critical",
        "action": "BLOCK"
    }

}