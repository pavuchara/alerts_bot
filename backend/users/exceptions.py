from abc import ABC, abstractmethod


class AbstractException(BaseException, ABC):

    def __init__(self, text_error: str | None = None, *args) -> None:
        super().__init__(*args)
        self.text_error = text_error

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError


class UserValidationException(AbstractException):

    def __str__(self) -> str:
        return self.text_error or "User validation error."


class UserDoesNotExistException(AbstractException):

    def __str__(self) -> str:
        return self.text_error or "User does not exists."
