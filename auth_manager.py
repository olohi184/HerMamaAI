
import streamlit as st
from supabase_client import get_supabase


def register_user(email, password):
    client = get_supabase()

    return client.auth.sign_up({
        "email": email.strip(),
        "password": password
    })


def login_user(email, password):
    client = get_supabase()


    response = client.auth.sign_in_with_password({
        "email": email.strip(),
        "password": password
    })

    return response.user


def logout_user():
    client = get_supabase()
    client.auth.sign_out()

    st.session_state.pop("supabase_client", None)


def get_current_user():
    client = get_supabase()

    session = client.auth.get_session()

    if session is None:
        return None

    response = client.auth.get_user()

    return response.user if response else None


def is_authenticated():
    return get_current_user() is not None
def request_password_reset(email):
    """Request a Supabase password recovery email."""

    client = get_supabase()

    client.auth.reset_password_email(
        email.strip(),
        {
            "redirect_to": (
                __import__("os").environ.get("PASSWORD_RECOVERY_URL")
                or st.secrets.get("PASSWORD_RECOVERY_URL")
                or "http://127.0.0.1:8503"
            )
        }
    )
def verify_recovery_token(token_hash):
    """Verify a recovery token using an isolated client."""
    from supabase import create_client

    if not token_hash or not token_hash.strip():
        raise ValueError("Recovery token is missing.")

    client = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

    response = client.auth.verify_otp({
        "token_hash": token_hash.strip(),
        "type": "recovery"
    })

    if not response.user or not response.session:
        raise RuntimeError("Recovery verification failed.")

    st.session_state["password_recovery_client"] = client

    return response.user


def update_recovered_password(password, confirm):
    """Update a password through a verified recovery session."""

    if len(password) < 12:
        raise ValueError(
            "Password must contain at least 12 characters."
        )

    if password != confirm:
        raise ValueError("Passwords do not match.")

    client = st.session_state.get(
        "password_recovery_client"
    )

    if client is None:
        raise RuntimeError(
            "Recovery session is missing or expired."
        )

    if client.auth.get_session() is None:
        st.session_state.pop(
            "password_recovery_client", None
        )
        raise RuntimeError("Recovery session expired.")

    response = client.auth.update_user({
        "password": password
    })

    if not response.user:
        raise RuntimeError("Password update failed.")

    try:
        client.auth.sign_out()
    finally:
        st.session_state.pop(
            "password_recovery_client", None
        )

    return True
