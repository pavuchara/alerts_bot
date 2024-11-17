from datetime import datetime

from sqlalchemy import (
    Integer,
    ForeignKey,
    DateTime,
    String,
)

import pytz

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from database.db import Base


class Reminder(Base):
    __tablename__ = "reminders"
    # Fields:
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )
    datetime_created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(pytz.timezone("Europe/Moscow")),
    )
    alert_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    # Relationsips:
    author = relationship(
        "User",
        back_populates="user_reminders",
        passive_deletes=True,
        lazy="joined",
    )
