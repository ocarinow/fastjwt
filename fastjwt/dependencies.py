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
    """Bundle of FastJWT capabilities

    Note:
        This class is used to access FastJWT's capabilities within
        the scope of a FastAPI Request. It is accessible via the
        `FastJWT.BUNDLE` instance's attribute OR `FastJWT.get_dependency` method.

    Args:
        _from (FastJWT[T]): FastJWT instance
        request (Request, optional): FastAPI Request instance. Defaults to None.
        response (Response, optional): FastAPI Response instance. Defaults to None.

    Attributes:
        request (Request): FastAPI Request instance
        response (Response): FastAPI Response instance
        _security (FastJWT[T]): FastJWT instance
    """

    def __init__(
        self,
        _from: "FastJWT[T]",
        request: Request = None,
        response: Response = None,
    ) -> None:
        """See help(FastJWTDeps) for more info

        Args:
            _from (FastJWT[T]): FastJWT instance
            request (Request, optional): FastAPI Request instance. Defaults to None.
            response (Response, optional): FastAPI Response instance. Defaults to None.
        """
        self._response = response
        self._request = request
        self._security = _from

    @property
    def request(self) -> Request:
        """The FastAPI Request instance"""
        return self._request

    @property
    def response(self) -> Response:
        """The FastAPI Response instance"""
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
        """Create an access token

        Args:
            uid (str): Unique identifier to generate token for
            fresh (bool, optional): Generate fresh token. Defaults to False.
            headers (Dict[str, Any], optional): TODO. Defaults to None.
            expiry (DateTimeExpression, optional): User defined expiry claim.
                Defaults to None.
            data (Dict[str, Any], optional): Additional data store in token.
                Defaults to None.
            audience (StrOrSeq, optional): Audience claim. Defaults to None.

        Returns:
            str: Access Token
        """
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
        """Generate a refresh token

        Args:
            uid (str): Unique identifier to generate token for
            headers (Dict[str, Any], optional): TODO. Defaults to None.
            expiry (DateTimeExpression, optional): User defined expiry claim.
                Defaults to None.
            data (Dict[str, Any], optional): Additional data store in token.
                Defaults to None.
            audience (StrOrSeq, optional): Audience claim.
                Defaults to None.

        Returns:
            str: Refresh Token
        """
        return self._security.create_refresh_token(
            uid, headers, expiry, data, audience, *args, **kwargs
        )

    def set_access_cookies(
        self, token, response: Optional[Response] = None, max_age: Optional[int] = None
    ):
        """Add 'Set-Cookie' for access token in response header

        Args:
            token (str): Access token
            response (Response, optional): Response to set cookie on.
                Defaults to None
            max_age (int, optional): Max Age cookie paramater.
                Defaults to None

        Note:
            When `response` is not provided,
            the `FastJWTDeps.response` attribute is used.
        """
        self._security.set_access_cookies(
            token=token, response=(response or self._response), max_age=max_age
        )

    def set_refresh_cookies(
        self, token, response: Optional[Response] = None, max_age: Optional[int] = None
    ):
        """Add 'Set-Cookie' for refresh token in response header

        Args:
            token (str): Refresh token
            response (Response): Response to set cookie on.
                Defaults to None
            max_age (int, optional): Max Age cookie paramater.
                Defaults to None

        Note:
            When `response` is not provided,
            the `FastJWTDeps.response` attribute is used.
        """
        self._security.set_refresh_cookies(
            token=token, response=(response or self._response), max_age=max_age
        )

    def unset_access_cookies(self, response: Optional[Response] = None):
        """Remove 'Set-Cookie' for access token in response header

        Args:
            response (Response, optional): Response to remove cooke from.
                Defaults to None

        Note:
            When `response` is not provided,
            the `FastJWTDeps.response` attribute is used.
        """
        self._security.unset_access_cookies(response=(response or self._response))

    def unset_refresh_cookies(self, response: Optional[Response] = None):
        """Remove 'Set-Cookie' for refresh token in response header

        Args:
            response (Response, optional): Response to remove cooke from.
                Defaults to None

        Note:
            When `response` is not provided,
            the `FastJWTDeps.response` attribute is used.
        """
        self._security.unset_access_cookies(response=(response or self._response))

    def unset_cookies(self, response: Optional[Response] = None):
        """Remove 'Set-Cookie' for tokens from response headers

        Args:
            response (Response): Response to remove token cookies from.
                Defaults to None

        Note:
            When `response` is not provided,
            the `FastJWTDeps.response` attribute is used.
        """
        self._security.unset_cookies(response=(response or self._response))

    async def get_current_subject(self) -> Optional[T]:
        """Get the current subject instance

        Use the request's token to retrieve the subject instance.
        Enforce a validation step to ensure the token is valid.

        Returns:
            Optional[T]: Subject instance

        Note:
            This method will always return `None` if
            `FastJWT.set_subject_getter` has not been set first.
        """
        return await self._security.get_current_subject(request=self._request)
