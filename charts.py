import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ======================================
# DONUT CHART
# ======================================

def status_chart(df):

    colors = {
        "BLOCKED": "#EF4444",
        "ALLOWED": "#22C55E",
        "DETECTED": "#FACC15"
    }

    fig = px.pie(
        df,
        names="Status",
        hole=0.65,
        color="Status",
        color_discrete_map=colors
    )

    fig.update_layout(

        title="Threat Status",

        paper_bgcolor="#0B1120",

        plot_bgcolor="#0B1120",

        font_color="white",

        legend_title="",

        height=420
    )

    fig.update_traces(
        textinfo="percent+label",
        pull=[0.03]*len(df["Status"].unique())
    )

    st.plotly_chart(fig, use_container_width=True)


# ======================================
# PROCESS ACTIVITY
# ======================================

def process_chart(df):

    data = (
        df.groupby("Process")
        .size()
        .reset_index(name="Count")
        .sort_values("Count")
    )

    fig = px.bar(

        data,

        x="Count",

        y="Process",

        orientation="h",

        color="Count",

        color_continuous_scale="Blues"

    )

    fig.update_layout(
    title="Process Activity",
    template="plotly_dark",
    paper_bgcolor="#0B1120",
    plot_bgcolor="#0B1120",
    font_color="white",
    coloraxis_showscale=False,
    height=420
)
    st.plotly_chart(fig, use_container_width=True)


# ======================================
# CATEGORY
# ======================================

def category_chart(df):

    fig = px.bar(

        df.groupby("Category")
        .size()
        .reset_index(name="Events"),

        x="Category",

        y="Events",

        color="Events",

        color_continuous_scale="Teal"

    )

    fig.update_layout(
    title="Threat Categories",
    template="plotly_dark",
    paper_bgcolor="#0B1120",
    plot_bgcolor="#0B1120",
    font_color="white",
    coloraxis_showscale=False,
    height=420
)
    st.plotly_chart(fig, use_container_width=True)


# ======================================
# USER ACTIVITY
# ======================================

def user_chart(df):

    fig = px.bar(

        df.groupby("User")
        .size()
        .reset_index(name="Events"),

        x="User",

        y="Events",

        color="Events",

        color_continuous_scale="Greens"

    )

    fig.update_layout(
    title="User Activity",
    template="plotly_dark",
    paper_bgcolor="#0B1120",
    plot_bgcolor="#0B1120",
    font_color="white",
    coloraxis_showscale=False,
    height=420
)

    st.plotly_chart(fig, use_container_width=True)


# ======================================
# TIMELINE
# ======================================

def timeline_chart(df):

    temp = df.copy()

    temp["Events"] = 1

    timeline = (

        temp.groupby("Timestamp")

        ["Events"]

        .sum()

        .reset_index()

    )

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=timeline["Timestamp"],

            y=timeline["Events"],

            mode="lines+markers",

            line=dict(

                color="#38BDF8",

                width=4

            ),

            marker=dict(

                size=9,

                color="#38BDF8"

            ),

            fill="tozeroy"

        )

    )

    fig.update_layout(

        title="Threat Timeline",

        paper_bgcolor="#0B1120",

        plot_bgcolor="#0B1120",

        font_color="white",

        height=420

    )

    st.plotly_chart(fig, use_container_width=True)
def threat_gauge(score):

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": "Threat Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#38BDF8"},
                "steps": [
                    {"range": [0, 20], "color": "#22C55E"},
                    {"range": [20, 50], "color": "#FACC15"},
                    {"range": [50, 75], "color": "#F97316"},
                    {"range": [75, 100], "color": "#EF4444"},
                ],
            },
        )
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0B1120",
        height=320
    )

    st.plotly_chart(fig, use_container_width=True)
