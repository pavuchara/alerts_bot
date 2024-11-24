from abc import ABC, abstractmethod


class AbstractReminderException(BaseException, ABC):

    def __init__(self, text_error: str | None = None) -> None:
        self.text_error = text_error

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError


class ReminderDoesNotExistException(AbstractReminderException):

    def __str__(self) -> str:
        return self.text_error or "Reminder does not exists."


class ReminderPermissionsException(AbstractReminderException):

    def __str__(self) -> str:
        return self.text_error or "Access only for the author."


class ReminderLimitException(AbstractReminderException):

    def __str__(self) -> str:
        return self.text_error or "Limit reminders, max 10"
