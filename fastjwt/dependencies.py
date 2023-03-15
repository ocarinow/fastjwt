from typing import TYPE_CHECKING
from typing import Any
from typing import Dict
from typing import Generic
from typing import TypeVar
from typing import Optional

from fastapi import Request
from fastapi import Response

from .types import StrOrSeq
from .types import DateTimeExpression

if TYPE_CHECKING:
    from .fastjwt import FastJWT

T = TypeVar("T")


class FastJWTDeps(Generic[T]):
    def __init__(
        self,
        _from: "FastJWT[T]",
        request: Request = None,
        response: Response = None,
    ) -> None:
        self._response = response
        self._request = request
        self._security = _from

    @property
    def request(self):
        return self._request

    @property
    def response(self):
        return self._response

    def create_access_token(
        self,
        uid: str,
        fresh: bool = False,
        headers: Optional[Dict[str, Any]] = None,
        expiry: Optional[DateTimeExpression] = None,
        data: Optional[Dict[str, Any]] = None,
        audience: Optional[StrOrSeq] = None,
        *args,
        **kwargs
    ) -> str:
        return self._security.create_access_token(
            uid, fresh, headers, expiry, data, audience, *args, **kwargs
        )

    def create_refresh_token(
        self,
        uid: str,
        headers: Optional[Dict[str, Any]] = None,
        expiry: Optional[DateTimeExpression] = None,
        data: Optional[Dict[str, Any]] = None,
        audience: Optional[StrOrSeq] = None,
        *args: Any,
        **kwargs: Any
    ) -> str:
        return self._security.create_refresh_token(
            uid, headers, expiry, data, audience, *args, **kwargs
        )

    def set_access_cookies(
        self, token, response: Optional[Response] = None, max_age: Optional[int] = None
    ):
        self._security.set_access_cookies(
            token=token, response=(response or self._response), max_age=max_age
        )

    def set_refresh_cookies(
        self, token, response: Optional[Response] = None, max_age: Optional[int] = None
    ):
        self._security.set_refresh_cookies(
            token=token, response=(response or self._response), max_age=max_age
        )

    def unset_access_cookies(self, response: Optional[Response] = None):
        self._security.unset_access_cookies(response=(response or self._response))

    def unset_refresh_cookies(self, response: Optional[Response] = None):
        self._security.unset_access_cookies(response=(response or self._response))

    def unset_cookies(self, response: Optional[Response] = None):
        self._security.unset_cookies(response=(response or self._response))

    async def get_current_subject(self) -> Optional[T]:
        return await self._security.get_current_subject(request=self._request)
