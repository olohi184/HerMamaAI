import streamlit as st

from auth_manager import (
    register_user,
    login_user,
    logout_user,
    get_current_user
)





def clear_private_session():
    """Clear session data while preserving language preference."""

    language = st.session_state.get("hm_language", "en")

    st.session_state.clear()

    if isinstance(language, str) and language in {
        "en", "ha", "yo", "ig"
    }:
        st.session_state["hm_language"] = language
    else:
        st.session_state["hm_language"] = "en"

    st.session_state["page"] = "🌱 AdaptiveCare"


def render_password_recovery():
    from auth_manager import (
        verify_recovery_token,
        update_recovered_password
    )

    token = st.query_params.get("token_hash")
    recovery_type = st.query_params.get("type")

    if token:
        st.session_state.pop(
            "password_recovery_client", None
        )

        st.query_params.clear()

        if recovery_type != "recovery":
            st.error("Invalid recovery link.")
            return True

        try:
            verify_recovery_token(token)
        except Exception:
            st.error(
                "This recovery link is invalid or expired. "
                "Please request a new link."
            )
            return True

    if "password_recovery_client" not in st.session_state:
        return False

    st.subheader("Create your new password")

    st.caption(
        "Choose a secure password with at least 12 characters."
    )

    with st.form("new_password_form", clear_on_submit=True):
        password = st.text_input(
            "New password", type="password"
        )

        confirm = st.text_input(
            "Confirm new password", type="password"
        )

        submitted = st.form_submit_button(
            "Save new password"
        )

    if submitted:
        if len(password) < 12:
            st.warning("Use at least 12 characters.")

        elif password != confirm:
            st.error("Passwords do not match.")

        else:
            try:
                update_recovered_password(password, confirm)
            except Exception:
                st.error(
                    "Password update could not be confirmed. "
                    "Please try signing in or request a new link."
                )
            else:
                clear_private_session()
                st.session_state["password_reset_success"] = True
                st.rerun()

    if st.button("Cancel password reset"):
        client = st.session_state.pop(
            "password_recovery_client", None
        )

        if client is not None:
            try:
                client.auth.sign_out()
            except Exception:
                pass

        st.query_params.clear()
        st.rerun()

    return True


def render_auth():
    if render_password_recovery():
        return None

    if st.session_state.pop("password_reset_success", False):
        st.success(
            "Password updated successfully. "
            "Please sign in with your new password."
        )

    if st.session_state.pop("wellness_logout_warning", False):
        st.warning(
            "You have been signed out locally. "
            "Remote sign-out could not be confirmed."
        )

    st.subheader("My Wellness Account")

    try:
        user = get_current_user()
    except Exception:
        st.warning("Account service is temporarily unavailable.")
        return None

    if user:
        st.success("You are signed in.")

        if st.button("Sign out", key="wellness_logout"):
            remote_failed = False

            try:
                logout_user()
            except Exception:
                remote_failed = True
            finally:
                clear_private_session()

            if remote_failed:
                st.session_state["wellness_logout_warning"] = True

            st.rerun()

        return user

    st.caption(
        "Create an account to save your wellness "
        "progress across visits."
    )

    login_tab, register_tab, recovery_tab = st.tabs(
        ["Sign in", "Create account", "Forgot password"]
    )

    with login_tab:
        with st.form("wellness_login", clear_on_submit=True):
            email = st.text_input("Email address")
            password = st.text_input(
                "Password", type="password"
            )

            submitted = st.form_submit_button("Sign in")

        if submitted:
            try:
                user = login_user(email, password)

                if user:
                    st.rerun()
                else:
                    st.error("Sign-in could not be completed.")

            except Exception:
                st.error(
                    "Unable to sign in. Check your credentials "
                    "and email confirmation."
                )

    with register_tab:
        with st.form("wellness_registration", clear_on_submit=True):
            email = st.text_input("Email address")
            password = st.text_input(
                "Create password", type="password"
            )
            confirm = st.text_input(
                "Confirm password", type="password"
            )

            consent = st.checkbox(
                "I agree to create a wellness account. "
                "This prototype is for fictional test data only."
            )

            submitted = st.form_submit_button(
                "Create account"
            )

        if submitted:
            if not consent:
                st.warning("Please confirm your agreement.")

            elif len(password) < 12:
                st.warning(
                    "Use at least 12 characters."
                )

            elif password != confirm:
                st.error("Passwords do not match.")

            else:
                try:
                    register_user(email, password)

                    st.success(
                        "Registration submitted. Check your "
                        "email for a confirmation link."
                    )

                except Exception:
                    st.error(
                        "Registration could not be completed. "
                        "Please try again later."
                    )

    with recovery_tab:
        from auth_manager import request_password_reset

        st.subheader("Reset your password")

        st.caption(
            "Enter your registered email address."
        )

        st.info("Enter your email to receive a password recovery link.")

        with st.form("wellness_password_recovery",
                     clear_on_submit=True):

            recovery_email = st.text_input(
                "Email address"
            )

            recovery_submitted = st.form_submit_button(
                "Send recovery link"
            )

        if recovery_submitted:
            if not recovery_email.strip():
                st.warning("Please enter your email address.")
            else:
                try:
                    request_password_reset(recovery_email)
                except Exception:
                    st.warning(
                        "Recovery could not be confirmed. "
                        "Please try again later."
                    )
                else:
                    st.success(
                        "If an account exists for this email, "
                        "a password recovery link will be sent."
                    )

    st.info(
        "You can continue using educational resources "
        "without creating an account."
    )

    return None
