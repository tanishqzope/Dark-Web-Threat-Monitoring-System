import streamlit as st
from datetime import datetime


# ======================================
# LOAD CSS
# ======================================

def load_css():

    st.markdown("""
    <style>

    .stApp{
        background:#0B1120;
        color:white;
    }

    section[data-testid="stSidebar"]{
        background:#111827;
    }

    .main-title{
        font-size:40px;
        color:#38BDF8;
        font-weight:bold;
        text-align:center;
        margin-bottom:5px;
    }

    .sub-title{
        text-align:center;
        color:#94A3B8;
        margin-bottom:25px;
        font-size:18px;
    }

    .metric-card{

        background:#1E293B;

        border-radius:15px;

        padding:20px;

        text-align:center;

        border-left:6px solid #38BDF8;

        box-shadow:0px 4px 15px rgba(0,0,0,0.35);

        transition:.3s;

        margin-bottom:10px;

    }

    .metric-card:hover{

        transform:translateY(-5px);

        box-shadow:0px 0px 20px #38BDF8;

    }

    .metric-title{

        color:#CBD5E1;

        font-size:16px;

    }

    .metric-value{

        font-size:34px;

        color:white;

        font-weight:bold;

        margin-top:10px;

    }

    .status-box{

        background:#111827;

        padding:15px;

        border-radius:12px;

        border-left:6px solid #22C55E;

        margin-bottom:20px;

        font-size:18px;

    }

    .footer{

        text-align:center;

        color:#94A3B8;

        margin-top:40px;

    }

    </style>
    """, unsafe_allow_html=True)


# ======================================
# HEADER
# ======================================

def header():

    st.markdown("""
    <h1 style='text-align:center;color:#38BDF8'>
    🛡 Dark Web Threat Intelligence Center
    </h1>

    <p style='text-align:center;color:#94A3B8'>
    Real-Time Security Operations Dashboard
    </p>
    """, unsafe_allow_html=True)

# ======================================
# LIVE STATUS
# ======================================

def monitoring_banner():

    now = datetime.now().strftime("%d-%m-%Y  %H:%M:%S")

    st.markdown(f"""
    <div class="status-box">

    🟢 <b>Monitoring Active</b>

    <br><br>

    🕒 <b>Last Refresh :</b> {now}

    </div>
    """, unsafe_allow_html=True)


# ======================================
# KPI CARD
# ======================================

def metric_card(title, value, color):

    st.markdown(f"""
    <div style="
        border-left:5px solid {color};
        background:#1a2233;
        padding:20px;
        border-radius:12px;
    ">

        <div style="
            color:#a5b4fc;
            font-size:16px;
            font-weight:bold;
        ">
            {title}
        </div>

        <div style="
            color:white;
            font-size:42px;
            font-weight:bold;
            margin-top:10px;
        ">
            {value}
        </div>

    </div>
    """, unsafe_allow_html=True)


# ======================================
# THREAT LEVEL
# ======================================

def threat_banner(level):

    colors = {
        "LOW": "#22C55E",
        "MEDIUM": "#FACC15",
        "HIGH": "#F97316",
        "CRITICAL": "#EF4444"
    }

    st.markdown(f"""
    <div style="
        background:#111827;
        border:2px solid {colors[level]};
        border-radius:12px;
        padding:18px;
        text-align:center;
        font-size:30px;
        color:{colors[level]};
        font-weight:bold;
    ">
        🚨 Threat Level : {level}
    </div>
    """, unsafe_allow_html=True)


# ======================================
# RECENT ALERTS
# ======================================

def recent_alerts(df):

    st.subheader("🚨 Recent Alerts")

    if len(df)==0:

        st.info("No alerts found.")

        return

    alerts = df.sort_values(
        "Timestamp",
        ascending=False
    ).head(5)

    for _,row in alerts.iterrows():

        status=row["Status"]

        emoji="🔴"

        if status=="ALLOWED":

            emoji="🟢"

        elif status=="DETECTED":

            emoji="🟡"

        st.markdown(

            f"{emoji} **{row['Process']}** "
            f"({row['Category']}) - "
            f"**{status}**"

        )


def status_panel():

    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    st.markdown(f"""
    <div style="
        background:#111827;
        padding:20px;
        border-radius:15px;
        border-left:5px solid #22c55e;
    ">

    🟢 <b>Monitoring :</b> ACTIVE

    <br>

    💾 <b>Database :</b> CONNECTED

    <br>

    📧 <b>Email Alerts :</b> ENABLED

    <br>

    🔄 <b>Auto Refresh :</b> Running

    <br>

    🕒 <b>{now}</b>

    </div>

    """,unsafe_allow_html=True)        


# ======================================
# FOOTER
# ======================================

def footer():

    st.markdown("""
    <hr>

    <div class="footer">

    Developed  using

    Python • Streamlit • Plotly • Pandas

    </div>
    """, unsafe_allow_html=True)