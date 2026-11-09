import streamlit as st


def notification_center(df):

    st.title("🔔 Notification Center")

    if df.empty:

        st.info("No notifications available.")

        return

    latest = df.sort_values(
        "Timestamp",
        ascending=False
    ).head(20)

    for _, row in latest.iterrows():

        severity = row["Severity"]
        process = row["Process"]
        status = row["Status"]
        time = row["Timestamp"]

        if severity == "Critical":

            st.error(
                f"🚨 [{time}] {process} - {severity} - {status}"
            )

        elif severity == "High":

            st.warning(
                f"⚠ [{time}] {process} - {severity} - {status}"
            )

        elif severity == "Medium":

            st.info(
                f"🟡 [{time}] {process} - {severity} - {status}"
            )

        else:

            st.success(
                f"🟢 [{time}] {process} - {severity} - {status}"
            )