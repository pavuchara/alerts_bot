from enum import Enum

from email_validator import validate_email, EmailNotValidError

from users.exceptions import UserValidationException


class RegistationSource(Enum):
    manual: str = "manual"
    telegram: str = "telegram"

    @classmethod
    def choises(cls) -> set[str]:
        return {item.value for item in cls}


def validate_user_email(email: str):
    try:
        emailinfo = validate_email(email, check_deliverability=False)
        return emailinfo.normalized
    except EmailNotValidError as e:
        raise UserValidationException(str(e))
