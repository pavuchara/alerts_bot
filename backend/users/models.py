from sqlalchemy import (
    Integer,
    String,
    Boolean,
    Enum,
)
from sqlalchemy.orm import (
    Mapped,
    validates,
    mapped_column,
    relationship,
)

from database.db import Base
from users.utils import (
    RegistationSource,
    validate_user_email,
)
from users.exceptions import UserValidationException


class User(Base):
    __tablename__ = "users"
    # Fields:
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(256), unique=True, nullable=True)
    password: Mapped[str | None] = mapped_column(String(60), nullable=True)
    telegram_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True, unique=True)
    first_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    registration_source: Mapped[RegistationSource] = mapped_column(
        Enum(RegistationSource), default=RegistationSource.manual
    )
    # Relationsips:
    user_reminders = relationship(
        "Reminder",
        back_populates="author",
        cascade="all, delete-orphan",
    )

    @validates("email")
    def validate_email(self, _, value) -> str | None:
        if value is None and self.registration_source is not None:
            raise UserValidationException("Email required field on manual registration")
        elif value is None:
            return None
        validated_email = validate_user_email(value)
        return validated_email

    @validates("password")
    def validate_password(self, _, value) -> str | None:
        if value is None and self.registration_source is not None:
            raise UserValidationException("Password required field on manual registration")
        return value

    @validates("telegram_id")
    def validate_telegram_id(self, _, value) -> int | None:
        if value is None and self.registration_source is RegistationSource.telegram.value:
            raise UserValidationException("TG registration must provide TG-id")
        return value
