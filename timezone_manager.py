from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import streamlit as st


def get_user_timezone():
    """
    Return the browser time zone.
    Fall back to UTC when unavailable.
    """
    name = st.context.timezone

    if name:
        try:
            return ZoneInfo(name)
        except (ZoneInfoNotFoundError, ValueError):
            pass

    return timezone.utc


def user_now():
    """Return the current user-local datetime."""
    return datetime.now(get_user_timezone())


def user_today():
    """Return the current user-local calendar date."""
    return user_now().date()
