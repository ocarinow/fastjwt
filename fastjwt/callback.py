import inspect
from typing import Generic
from typing import TypeVar
from typing import Optional

from .types import ModelCallback
from .types import TokenCallback

T = TypeVar("T")


class _CallbackHandler(Generic[T]):
    def __init__(self, model: T) -> None:
        # Attributes
        self._model: T = model
        # Callbcaks
        self.callback_get_model_instance: Optional[ModelCallback[T]] = None
        self.callback_is_token_in_blocklist: Optional[TokenCallback] = None

        # Exceptions
        self._callback_model_set_exception = AttributeError(
            f"No callback function is set for model retrieval. Use `{self.__class__.__name__}.set_callback_get_model_instance` before"
        )
        self._callback_token_set_exception = AttributeError(
            f"No callback function is set for token in blocklist checks. Use `{self.__class__.__name__}.set_callback_token_blocklist` before"
        )

    @property
    def is_model_callback_set(self) -> bool:
        return self.callback_get_model_instance is not None

    @property
    def is_token_callback_set(self) -> bool:
        return self.callback_get_model_instance is not None

    def _check_model_callback_is_set(self, ignore_errors: bool = True) -> bool:
        if self.is_model_callback_set:
            return True
        if ignore_errors:
            raise self._callback_model_set_exception
        return False

    def _check_token_callback_is_set(self, ignore_errors: bool = True) -> bool:
        if self.is_token_callback_set:
            return True
        if ignore_errors:
            raise self._callback_token_set_exception
        return False

    def set_callback_get_model_instance(self, callback: ModelCallback[T]) -> None:
        self.callback_get_model_instance = callback

    def set_callback_token_blocklist(self, callback: TokenCallback) -> None:
        self.callback_is_token_in_blocklist = callback

    def _get_current_subject(self, uid: str, **kwargs) -> T:
        self._check_model_callback_is_set()
        callback: ModelCallback[T] = self.callback_get_model_instance
        return callback(uid, **kwargs)

    def is_token_in_blocklist(self, token: str, **kwargs) -> bool:
        self._check_token_callback_is_set()
        callback: TokenCallback = self.callback_is_token_in_blocklist
        return callback(token, **kwargs)
