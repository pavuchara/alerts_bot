from pydantic import (
    BaseModel,
    ConfigDict,
    ValidationInfo,
    Field,
    field_validator,
    model_validator,
)

from users.exceptions import UserValidationException
from users.utils import validate_user_email


class UserCreateSchema(BaseModel):
    email: str | None = Field(max_length=256)
    password: str | None = Field(max_length=50)
    telegram_id: int | None = Field(ge=1, le=99999999)
    first_name: str | None = Field(max_length=50)
    last_name: str | None = Field(max_length=50)

    @field_validator("email")
    @classmethod
    def validate_email_field(cls, value: str, info: ValidationInfo):
        if value is None:
            return None
        try:
            return validate_user_email(value)
        except UserValidationException as e:
            raise ValueError(str(e))

    @model_validator(mode="after")
    def validate_creation_info(self):
        if not self.email and not self.password and not self.telegram_id:
            raise ValueError(
                "User must provide either Telegram ID "
                "or both Email and Password for registration."
            )
        if self.email and not self.password:
            raise ValueError(
                "You provided an email but didn't set a password. "
                "Both are required for manual registration."
            )
        if self.password and not self.email:
            raise ValueError(
                "You provided a password but didn't set an email. "
                "Both are required for manual registration."
            )
        return self


class UserUpdateSchema(BaseModel):
    first_name: str | None
    last_name: str | None


class UserRetrieveSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str | None
    is_admin: bool
    first_name: str | None
    last_name: str | None
    telegram_id: int | None
