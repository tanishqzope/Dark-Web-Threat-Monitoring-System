import streamlit as st
import pandas as pd

from database import (
    fetch_rules,
    add_rule,
    update_rule,
    delete_rule
)


def threat_rules_page():

    st.title("🛡 Threat Intelligence Rules")

    rules = fetch_rules()

    if not rules:
        st.info("No threat rules found.")
        return

    df = pd.DataFrame(
        rules,
        columns=[
            "ID",
            "Process",
            "Category",
            "Severity",
            "Enabled"
        ]
    )

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True
    )

    st.divider()

    # =====================================================
    # ADD RULE
    # =====================================================

    st.subheader("➕ Add New Rule")

    with st.form("add_rule_form"):

        process = st.text_input(
            "Process Name",
            placeholder="example.exe"
        )

        category = st.selectbox(
            "Category",
            [
                "Browser",
                "Admin Tool",
                "System Tool",
                "Dark Web"
            ]
        )

        severity = st.selectbox(
            "Severity",
            [
                "Low",
                "Medium",
                "High",
                "Critical"
            ]
        )

        submitted = st.form_submit_button("➕ Add Rule")

        if submitted:

            process = process.strip().lower()

            if process == "":

                st.warning("Please enter a process name.")

            else:

                try:

                    add_rule(
                        process,
                        category,
                        severity
                    )

                    st.success("✅ Rule Added Successfully")

                    st.rerun()

                except Exception as e:

                    st.error(f"❌ {e}")

    st.divider()

    # =====================================================
    # EDIT RULE
    # =====================================================

    st.subheader("✏ Manage Existing Rule")

    selected = st.selectbox(
        "Select Rule",
        df["Process"].tolist()
    )

    rule = df[df["Process"] == selected].iloc[0]

    with st.form("edit_rule_form"):

        new_category = st.selectbox(
            "Category",
            [
                "Browser",
                "Admin Tool",
                "System Tool",
                "Dark Web"
            ],
            index=[
                "Browser",
                "Admin Tool",
                "System Tool",
                "Dark Web"
            ].index(rule["Category"])
        )

        new_severity = st.selectbox(
            "Severity",
            [
                "Low",
                "Medium",
                "High",
                "Critical"
            ],
            index=[
                "Low",
                "Medium",
                "High",
                "Critical"
            ].index(rule["Severity"])
        )

        enabled = st.checkbox(
            "Monitoring Enabled",
            value=bool(rule["Enabled"])
        )

        col1, col2 = st.columns(2)

        with col1:
            update = st.form_submit_button("💾 Update Rule")

        with col2:
            delete = st.form_submit_button("🗑 Delete Rule")

        if update:

            update_rule(
                int(rule["ID"]),
                new_category,
                new_severity,
                int(enabled)
            )

            st.success("✅ Rule Updated Successfully")

            st.rerun()

        if delete:

            delete_rule(int(rule["ID"]))

            st.success("✅ Rule Deleted Successfully")

            st.rerun()