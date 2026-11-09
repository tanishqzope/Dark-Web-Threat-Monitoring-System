import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
from admin import admin_panel
from notifications import notification_center
from login import login_page
from threat_rules import threat_rules_page
from session import clear_session
from settings import (
    load_settings,
    save_settings
)
from utils import (
    load_logs,
    calculate_threat_score,
    threat_level
)

from charts import (
    status_chart,
    process_chart,
    category_chart,
    user_chart,
    timeline_chart,
    threat_gauge
)
from ui import (
    load_css,
    header,
    monitoring_banner,
    metric_card,
    threat_banner,
    recent_alerts,
    footer
)
from config import (
    REFRESH_INTERVAL,
    MAX_RECENT_ALERTS
)
from system_status import (
    monitor_status,
    database_status,
    logger_status,
    email_status,
    authentication_status,
    policy_status
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Dark Web Threat Intelligence",
    page_icon="🛡️",
    layout="wide"
)
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login_page()
    st.stop()

st_autorefresh(
    interval=REFRESH_INTERVAL,
    key="refresh"
)

# ==========================================
# LOAD UI
# ==========================================

load_css()
header()
monitoring_banner()

# ==========================================
# LOAD DATA
# ==========================================

df = load_logs()

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("🛡 Navigation")
st.sidebar.write(
    f"👤 {st.session_state['username']}"
)

st.sidebar.write(
    f"Role : {st.session_state['role']}"
)

if st.sidebar.button("🚪 Logout"):

    clear_session()

    st.session_state.clear()

    st.rerun()

pages = [

    "🏠 Dashboard",

    "📈 Analytics",

    "📋 Logs",

    "🔔 Notifications",

    "⚙ Settings"
]

if st.session_state["role"] == "Admin":

    pages.append("🛡 Threat Rules")

    pages.append("🛡 Admin Panel")

pages.append("ℹ About")


page = st.sidebar.radio(
    " ",
    pages
)


st.sidebar.divider()

st.sidebar.success("🟢 Monitoring Active")

st.sidebar.write(
    f"🕒 {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
)

# ==========================================
# DASHBOARD
# ==========================================

if page == "🏠 Dashboard":
    st.title("🛡 Security Operations Center")

    st.caption(
        "Real-Time Dark Web Threat Intelligence & Browser Activity Monitoring"
    )

    st.divider()

    total = len(df)

    blocked = (
        df["Status"]=="BLOCKED"
    ).sum() if total else 0

    allowed = (
        df["Status"]=="ALLOWED"
    ).sum() if total else 0

    score = calculate_threat_score(df)

    level = threat_level(score)
    settings = load_settings()

    c1, c2, c3 = st.columns(3)

    with c1:

        if monitor_status():
            st.success("🟢 Monitor Running")
        else:
            st.error("🔴 Monitor Offline")

        if authentication_status():
            st.success("🟢 Authentication")
        else:
            st.error("🔴 Authentication")

    with c2:

        if database_status():
            st.success("🟢 Database Connected")
        else:
            st.error("🔴 Database Error")

        if logger_status():
            st.success("🟢 Logger Active")
        else:
            st.error("🔴 Logger Offline")

    with c3:

        if email_status(settings):
            st.success("🟢 Email Alerts Enabled")
        else:
            st.warning("🟡 Email Alerts Disabled")

        if policy_status():
            st.success("🟢 Policy Engine Loaded")
        else:
            st.error("🔴 Policy Error")
        st.divider()

    critical = (
        df["Severity"] == "Critical"
    ).sum() if total else 0

    high = (
        df["Severity"] == "High"
    ).sum() if total else 0

    today = (
        df["Timestamp"].dt.date ==
        datetime.now().date()
    ).sum() if total else 0

    last_scan = (
        df.iloc[0]["Timestamp"]
        if total else "Never"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("📊 Total Events", total)

    with c2:
        st.metric("🚫 Blocked", blocked)

    with c3:
        st.metric("🚨 Critical", critical)

    with c4:
        st.metric("⚠ Threat Score", score)

    st.divider()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("✅ Allowed", allowed)

    with c2:
        st.metric("🟠 High Risk", high)

    with c3:
        st.metric("📅 Today's Events", today)

    with c4:
        st.metric(
            "👤 Active User",
            st.session_state["username"]
        )

    threat_banner(level)
    st.info(
        f"""
    🛡 Current Threat Level : {level}

    📊 Total Events : {total}

    🚨 Critical Threats : {critical}

    ⚠ High Risk Events : {high}

    👤 Logged in as : {st.session_state['username']}
    """
    )

    threat_gauge(score)

    st.divider()

    left,right = st.columns(2)

    with left:
        status_chart(df)

    with right:
        process_chart(df)

    st.divider()

    left,right = st.columns(2)

    with left:
        category_chart(df)

    with right:
        user_chart(df)

    st.divider()

    timeline_chart(df)

    st.divider()

    recent_alerts(df)

    st.divider()
    st.subheader("📡 Live Activity Feed")
    latest = df.sort_values(
    "Timestamp",
    ascending=False).head(MAX_RECENT_ALERTS)

    for _, row in latest.iterrows():

        severity = row["Severity"]

        if severity == "Critical":
            icon = "🚨"

        elif severity == "High":
            icon = "⚠"

        elif severity == "Medium":
            icon = "🟡"

        else:
            icon = "🟢"

        st.write(
            f"""
    {icon} **{row['Timestamp']}**

    **Process :** {row['Process']}

    **Category :** {row['Category']}

    **Severity :** {row['Severity']}

    **Status :** {row['Status']}

    ---
    """
        )
    st.divider()
    st.subheader("📋 Recent Logs")

    st.dataframe(
        df.sort_values(
            "Timestamp",
            ascending=False
        ),
        hide_index=True,
        use_container_width=True
    )

    st.divider()

# ==========================================
# ANALYTICS
# ==========================================

elif page == "📈 Analytics":

    st.title("📊 Threat Analytics")

    col1,col2 = st.columns(2)

    with col1:
        category_chart(df)

    with col2:
        user_chart(df)

    st.divider()

    process_chart(df)

    st.divider()

    timeline_chart(df)

# ==========================================
# LOGS
# ==========================================

elif page == "📋 Logs":

    st.title("📋 Security Logs")

    search = st.text_input(
        "🔍 Search Logs"
    )

    temp = df.copy()

    if search:

        temp = temp[
            temp.astype(str)
            .apply(
                lambda x:
                x.str.contains(
                    search,
                    case=False
                )
            )
            .any(axis=1)
        ]

    st.download_button(
        "⬇ Export CSV",
        temp.to_csv(index=False),
        file_name="security_logs.csv"
    )

    st.dataframe(
        temp.sort_values(
            "Timestamp",
            ascending=False
        ),
        hide_index=True,
        use_container_width=True
    )
# ==========================================
# NOTIFICATIONS
# ==========================================

elif page == "🔔 Notifications":

    notification_center(df)    
# ==========================================
# SETTINGS
# ==========================================

elif page == "⚙ Settings":

    st.title("⚙ Security Settings")

    settings = load_settings()

    st.subheader("Monitored Processes")

    settings["monitor_chrome"] = st.checkbox(
        "Google Chrome",
        settings["monitor_chrome"]
    )

    settings["monitor_edge"] = st.checkbox(
        "Microsoft Edge",
        settings["monitor_edge"]
    )

    settings["monitor_firefox"] = st.checkbox(
        "Mozilla Firefox",
        settings["monitor_firefox"]
    )

    settings["monitor_powershell"] = st.checkbox(
        "PowerShell",
        settings["monitor_powershell"]
    )

    settings["monitor_cmd"] = st.checkbox(
        "Command Prompt",
        settings["monitor_cmd"]
    )

    settings["monitor_regedit"] = st.checkbox(
        "Registry Editor",
        settings["monitor_regedit"]
    )

    settings["monitor_tor"] = st.checkbox(
        "Tor Browser",
        settings["monitor_tor"]
    )

    st.divider()

    st.subheader("Security Options")

    settings["email_alerts"] = st.checkbox(
        "Enable Email Alerts",
        settings["email_alerts"]
    )

    settings["auto_block"] = st.checkbox(
        "Auto Block Unauthorized Processes",
        settings["auto_block"]
    )

    settings["refresh_interval"] = st.slider(
        "Refresh Interval (Seconds)",
        1,
        10,
        settings["refresh_interval"]
    )
    st.divider()

    st.subheader("🛡 Security Policy")

    actions = [
        "Log",
        "Log + Email",
        "Email + Block",
        "Block + Email"
    ]

    settings["low_action"] = st.selectbox(
        "Low Severity",
        actions,
        index=actions.index(settings["low_action"])
    )

    settings["medium_action"] = st.selectbox(
        "Medium Severity",
        actions,
        index=actions.index(settings["medium_action"])
    )

    settings["high_action"] = st.selectbox(
        "High Severity",
        actions,
        index=actions.index(settings["high_action"])
    )

    settings["critical_action"] = st.selectbox(
        "Critical Severity",
        actions,
        index=actions.index(settings["critical_action"])
    )

    if st.button("💾 Save Settings"):

        save_settings(settings)

        st.success("Settings Saved Successfully!")
# ==========================================
# THREAT RULES
# ==========================================

elif page == "🛡 Threat Rules":

    threat_rules_page()        

# ==========================================
# ADMIN PANEL
# ==========================================

elif page == "🛡 Admin Panel":

    admin_panel()
# ==========================================
# ABOUT
# ==========================================

else:

    st.title(" About")

    st.markdown("""
## 🛡 Dark Web Threat Intelligence & Browser Activity Monitoring System

A real-time cybersecurity monitoring system developed using Python, Streamlit, and SQLite that monitors browser and system processes, performs threat analysis, logs security events, and provides an interactive dashboard for administrators.

### Key Features

✅ Real-time Process Monitoring

✅ Role-Based Authentication

✅ Threat Rules Engine

✅ Dynamic Security Policies

✅ Email Alerts

✅ Threat Analytics Dashboard

✅ Live Monitoring

✅ Security Event Logging

✅ Admin Panel

✅ CSV Export

### Technology Stack

• Python

• Streamlit

• SQLite

• Plotly

• Pandas

• Psutil

• SMTP

• Git

""")
st.divider()

st.caption(
    "🛡 Dark Web Threat Intelligence & Browser Activity Monitoring System"
)

st.caption(
    f"Logged in as: {st.session_state['username']} ({st.session_state['role']})"
)

st.caption(
    f"Last Updated: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
)
footer()