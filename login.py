import streamlit as st
from session import save_session
from user_auth import (
    register_user,
    login_user
)


def login_page():

    tab1, tab2 = st.tabs(
        ["🔐 Login", "📝 Register"]
    )

    # ==================================
    # LOGIN
    # ==================================

    with tab1:

        st.title("🔐 Login")

        username = st.text_input(
            "Username",
            key="login_user"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_pass"
        )

        if st.button("Login"):

            role = login_user(
                username,
                password
            )

            if role:

                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["role"] = role
                save_session(username,role)
                st.success("Login Successful")

                st.rerun()

            else:

                st.error("Invalid Username or Password")

    # ==================================
    # REGISTER
    # ==================================

    with tab2:

        st.title("📝 Register")

        username = st.text_input(
            "Username",
            key="reg_user"
        )

        email = st.text_input(
            "Email",
            key="reg_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="reg_pass"
        )

        confirm = st.text_input(
            "Confirm Password",
            type="password",
            key="reg_confirm"
        )

        if st.button("Create Account"):

            if password != confirm:

                st.error("Passwords do not match")

            else:

                if register_user(
                    username,
                    email,
                    password
                ):

                    st.success(
                        "Account Created Successfully"
                    )

                else:

                    st.error(
                        "Username or Email already exists"
                    )