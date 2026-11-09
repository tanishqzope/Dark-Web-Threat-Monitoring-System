import streamlit as st
import pandas as pd
from database import (
    fetch_users,
    update_role,
    delete_user,
    admin_count
)


def admin_panel():

    st.title("🛡 Admin Panel")

    users = fetch_users()

    df = pd.DataFrame(
        users,
        columns=[
            "ID",
            "Username",
            "Email",
            "Role",
            "Created"
        ]
    )

# =====================================
# Search User
# =====================================

    search = st.text_input("🔍 Search User")

    if search:

        df = df[
            df["Username"].str.contains(search, case=False) |
            df["Email"].str.contains(search, case=False)
        ]

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    usernames = df["Username"].tolist()

    selected = st.selectbox(
        "Select User",
        usernames
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button("⬆ Promote"):

            current_role = df.loc[
                df["Username"] == selected,
                "Role"
            ].values[0]

            if current_role == "Admin":

                st.info("ℹ User is already an Admin.")

            else:

                update_role(
                    selected,
                    "Admin"
                )

                st.success("✅ User promoted successfully.")

                st.rerun()

    with col2:

        if st.button("⬇ Demote"):

            current_role = df.loc[
                df["Username"] == selected,
                "Role"
            ].values[0]

            if selected == st.session_state["username"]:

                st.error("❌ You cannot demote yourself.")

            elif current_role == "Admin" and admin_count() == 1:

                st.error("❌ Cannot demote the last Admin.")

            else:

                update_role(
                    selected,
                    "User"
                )

                st.success("✅ User demoted successfully.")

                st.rerun()

    with col3:

        confirm = st.checkbox(
            "I understand this action cannot be undone."
        )

        if st.button("🗑 Delete User"):

            if not confirm:

                st.warning("⚠ Please confirm before deleting.")

            elif selected == st.session_state["username"]:

                st.error("❌ You cannot delete your own account.")

            else:

                delete_user(selected)

                st.success("✅ User deleted successfully.")

                st.rerun()