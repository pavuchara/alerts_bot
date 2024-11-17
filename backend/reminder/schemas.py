from datetime import (
    datetime,
    timedelta,
)

from pydantic import (
    BaseModel,
    ConfigDict,
    ValidationInfo,
    Field,
    field_serializer,
    field_validator,
)

import pytz

from users.schemas import UserRetrieveSchema


class ReminderCreateSchema(BaseModel):
    alert_datetime: datetime
    description: str = Field(max_length=255)

    @field_validator("alert_datetime")
    @classmethod
    def validate_alert_datetime(cls, value: datetime, info: ValidationInfo):
        if (datetime.now(pytz.timezone("Europe/Moscow")) + timedelta(hours=1)) > value:
            raise ValueError("A reminder can be set for at least 1 hour")
        return value


class ReminderUpdateSchema(ReminderCreateSchema):
    pass


class ReminderRetriveSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    datetime_created: datetime
    alert_datetime: datetime
    description: str
    author: UserRetrieveSchema

    @field_serializer("datetime_created", "alert_datetime")
    @classmethod
    def convert_to_moscow(cls, value: datetime) -> str:
        moscow_tz = pytz.timezone("Europe/Moscow")
        return value.astimezone(moscow_tz).isoformat()
