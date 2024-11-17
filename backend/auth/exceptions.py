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
        return self.text_error if self.text_error else "Could not validate credentials."
