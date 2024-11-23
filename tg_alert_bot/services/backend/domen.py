from enum import Enum

from config import BACKEND_URI


class BackendPaths(Enum):
    """Remote backend service paths."""
    USERS: str = f"{BACKEND_URI}/users/"
    TOKEN: str = f"{BACKEND_URI}/auth/tg_user_token"
    REMINDERS: str = f"{BACKEND_URI}/reminders/"
    SELF_REMINDERS: str = f"{BACKEND_URI}/reminders/my_reminders"
