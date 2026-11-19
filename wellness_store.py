from datetime import timedelta
from timezone_manager import user_today

from supabase_client import get_supabase
from auth_manager import get_current_user


TABLE_NAME = "wellness_checkins"


def require_user():
    user = get_current_user()

    if user is None:
        raise PermissionError("Sign in is required.")

    return user


def save_checkin(record, consent=False):
    if not consent:
        raise PermissionError("Storage consent is required.")

    user = require_user()
    client = get_supabase()

    payload = {
        "user_id": str(user.id),
        "date": user_today().isoformat(),
        "goal": str(record["goal"]),
        "context": str(record["context"]),
        "energy": str(record["energy"]),
        "restart": bool(record["restart"]),
        "completed": bool(record["completed"]),
        "sleep": str(record["sleep"]),
        "stress": str(record["stress"])
    }

    response = (
        client.table(TABLE_NAME)
        .upsert(payload, on_conflict="user_id,date,goal")

        .execute()
    )

    return response.data


def load_history(days=7):
    user = require_user()
    client = get_supabase()

    days = max(1, min(int(days), 365))

    today = user_today()

    start_date = (
        today - timedelta(days=days - 1)
    ).isoformat()

    response = (
        client.table(TABLE_NAME)
        .select(
            "date,goal,context,energy,"
            "restart,completed,sleep,stress"
        )
        .eq("user_id", str(user.id))
        .gte("date", start_date)
        .lte("date", today.isoformat())
        .order("date", desc=True)
        .execute()
    )

    return response.data or []


def delete_history():
    user = require_user()
    client = get_supabase()

    response = (
        client.table(TABLE_NAME)
        .delete()
        .eq("user_id", str(user.id))
        .execute()
    )

    return response.data
