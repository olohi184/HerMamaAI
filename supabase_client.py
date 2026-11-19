import os
import streamlit as st
from supabase import create_client, Client


def get_supabase() -> Client:
    """Create a client isolated to the current Streamlit session."""

    if "supabase_client" not in st.session_state:

        url = (os.getenv("SUPABASE_URL") or st.secrets["SUPABASE_URL"])
        key = (os.getenv("SUPABASE_KEY") or st.secrets["SUPABASE_KEY"])

        st.session_state["supabase_client"] = create_client(
            url,
            key
        )

    return st.session_state["supabase_client"]
