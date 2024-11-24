from abc import ABC, abstractmethod


class AbstractException(BaseException, ABC):

    def __init__(self, text_error: str | None = None, *args) -> None:
        super().__init__(*args)
        self.text_error = text_error

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError


class AuthUserException(AbstractException):

    def __str__(self) -> str:
        return self.text_error or "Could not validate credentials."


class RegistrationUserException(AbstractException):

    def __str__(self) -> str:
        return self.text_error or "Wrong registration data."


class TokenExpireException(AbstractException):

    def __str__(self) -> str:
        return self.text_error or "Token Expire."


class ReminderServiceException(AbstractException):

    def __str__(self) -> str:
        return self.text_error or "Reminder exception..."


class ReminderLimitException(AbstractException):

    def __str__(self) -> str:
        return self.text_error or "Limit reminders, max 10"
