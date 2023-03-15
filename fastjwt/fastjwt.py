from typing import Any
from typing import Dict
from typing import Literal
from typing import TypeVar
from typing import Callable
from typing import Optional
from typing import Coroutine
from typing import overload

from fastapi import Request
from fastapi import Response

from .core import _get_token_from_request
from .types import StrOrSeq
from .types import TokenType
from .types import TokenLocations
from .types import DateTimeExpression
from .utils import get_uuid
from .config import FJWTConfig
from .models import RequestToken
from .models import TokenPayload
from ._errors import _ErrorHandler
from ._callback import _CallbackHandler
from .exceptions import FastJWTException
from .exceptions import MissingTokenError
from .exceptions import RevokedTokenError
from .dependencies import FastJWTDeps

T = TypeVar("T")


class FastJWT(_CallbackHandler[T], _ErrorHandler):
    """The base FastJWT object

    FastJWT enables JWT management within a FastAPI application.
    Its main purpose is to provide a reusable & simple syntax to protect API
    with JSON Web Token authentication.

    Args:
        config (FJWTConfig, optional): Configuration instance to use. Defaults to FJWTConfig().
        model (Optional[T], optional): Model type hint. Defaults to Dict[str, Any].

    Note:
        FastJWT is a Generic python object.
        Its TypeVar is not mandatory but helps type hinting furing development

    """

    def __init__(
        self, config: FJWTConfig = FJWTConfig(), model: Optional[T] = Dict[str, Any]
    ) -> None:
        """FastJWT base object

        Args:
            config (FJWTConfig, optional): Configuration instance to use. Defaults to FJWTConfig().
            model (Optional[T], optional): Model type hint. Defaults to Dict[str, Any].
        """
        super().__init__(model=model)
        super(_CallbackHandler, self).__init__()
        self._config = config

    def load_config(self, config: FJWTConfig) -> None:
        """Loads a FJWTConfig as the new configuration

        Args:
            config (FJWTConfig): Configuration to load
        """
        self._config = config

    @property
    def config(self) -> FJWTConfig:
        """FastJWT Configuration getter

        Returns:
            FJWTConfig: Configuration BaseSettings
        """
        return self._config

    # region Core methods

    def _create_payload(
        self,
        uid: str,
        type: str,
        fresh: bool = False,
        expiry: Optional[DateTimeExpression] = None,
        data: Optional[Dict[str, Any]] = None,
        audience: Optional[StrOrSeq] = None,
        **kwargs
    ) -> TokenPayload:
        # Handle additional data
        if data is None:
            data = {}
        # Handle expiry date
        exp = expiry
        if exp is None:
            exp = (
                self.config.JWT_ACCESS_TOKEN_EXPIRES
                if type == "access"
                else self.config.JWT_REFRESH_TOKEN_EXPIRES
            )
        # Handle CSRF
        csrf = None
        if self.config.has_location("cookies") and self.config.JWT_COOKIE_CSRF_PROTECT:
            csrf = get_uuid()
        # Handle audience
        aud = audience
        if aud is None:
            aud = self.config.JWT_ENCODE_AUDIENCE
        payload = TokenPayload(
            sub=uid,
            fresh=fresh,
            exp=exp,
            type=type,
            iss=self.config.JWT_ENCODE_ISSUER,
            aud=aud,
            csrf=csrf,
            # Handle NBF
            nbf=None,
            **data
        )
        return payload

    def _create_token(
        self,
        uid: str,
        type: str,
        fresh: bool = False,
        headers: Optional[Dict[str, Any]] = None,
        expiry: Optional[DateTimeExpression] = None,
        data: Optional[Dict[str, Any]] = None,
        audience: Optional[StrOrSeq] = None,
        **kwargs
    ) -> str:
        payload = self._create_payload(
            uid=uid,
            type=type,
            fresh=fresh,
            expiry=expiry,
            data=data,
            audience=audience,
            **kwargs
        )
        token = payload.encode(
            key=self.config.PRIVATE_KEY,
            algorithm=self.config.JWT_ALGORITHM,
            headers=headers,
        )

        return token

    def _decode_token(
        self,
        token: str,
        verify: bool = True,
        audience: Optional[StrOrSeq] = None,
        issuer: Optional[str] = None,
    ) -> TokenPayload:
        return TokenPayload.decode(
            token=token,
            key=self.config.PUBLIC_KEY,
            algorithms=[self.config.JWT_ALGORITHM],
            verify=verify,
            audience=audience if audience else self.config.JWT_DECODE_AUDIENCE,
            issuer=issuer if issuer else self.config.JWT_DECODE_ISSUER,
        )

    def _set_cookies(
        self,
        token: str,
        type: str,
        response: Response,
        max_age: Optional[int] = None,
        *args,
        **kwargs
    ) -> None:
        if type == "access":
            token_key = self.config.JWT_ACCESS_COOKIE_NAME
            token_path = self.config.JWT_ACCESS_COOKIE_PATH
            csrf_key = self.config.JWT_ACCESS_CSRF_COOKIE_NAME
            csrf_path = self.config.JWT_ACCESS_CSRF_COOKIE_PATH
        elif type == "refresh":
            token_key = self.config.JWT_REFRESH_COOKIE_NAME
            token_path = self.config.JWT_REFRESH_COOKIE_PATH
            csrf_key = self.config.JWT_REFRESH_CSRF_COOKIE_NAME
            csrf_path = self.config.JWT_REFRESH_CSRF_COOKIE_PATH
        else:
            raise ValueError("Token type must be 'access' | 'refresh'")

        # Set cookie
        response.set_cookie(
            key=token_key,
            value=token,
            path=token_path,
            domain=self.config.JWT_COOKIE_DOMAIN,
            samesite=self.config.JWT_COOKIE_SAMESITE,
            secure=self.config.JWT_COOKIE_SECURE,
            httponly=True,
            max_age=max_age if max_age else self.config.JWT_COOKIE_MAX_AGE,
        )
        # Set CSRF
        if self.config.JWT_COOKIE_CSRF_PROTECT and self.config.JWT_CSRF_IN_COOKIES:
            response.set_cookie(
                key=csrf_key,
                value=self._decode_token(token=token, verify=True).csrf,
                path=csrf_path,
                domain=self.config.JWT_COOKIE_DOMAIN,
                samesite=self.config.JWT_COOKIE_SAMESITE,
                secure=self.config.JWT_COOKIE_SECURE,
                httponly=False,
                max_age=max_age if max_age else self.config.JWT_COOKIE_MAX_AGE,
            )

    def _unset_cookies(
        self,
        type: str,
        response: Response,
    ) -> None:
        if type == "access":
            token_key = self.config.JWT_ACCESS_COOKIE_NAME
            token_path = self.config.JWT_ACCESS_COOKIE_PATH
            csrf_key = self.config.JWT_ACCESS_CSRF_COOKIE_NAME
            csrf_path = self.config.JWT_ACCESS_CSRF_COOKIE_PATH
        elif type == "refresh":
            token_key = self.config.JWT_REFRESH_COOKIE_NAME
            token_path = self.config.JWT_REFRESH_COOKIE_PATH
            csrf_key = self.config.JWT_REFRESH_CSRF_COOKIE_NAME
            csrf_path = self.config.JWT_REFRESH_CSRF_COOKIE_PATH
        else:
            raise ValueError("Token type must be 'access' | 'refresh'")
        # Unset cookie
        response.delete_cookie(
            key=token_key,
            path=token_path,
            domain=self.config.JWT_COOKIE_DOMAIN,
        )
        if self.config.JWT_COOKIE_CSRF_PROTECT and self.config.JWT_CSRF_IN_COOKIES:
            response.delete_cookie(
                key=csrf_key,
                path=csrf_path,
                domain=self.config.JWT_COOKIE_DOMAIN,
            )

    @overload
    async def _get_token_from_request(
        self,
        request: Request,
        locations: Optional[TokenLocations] = None,
        refresh: bool = False,
        optional: Literal[False] = False,
    ) -> RequestToken:
        ...

    @overload
    async def _get_token_from_request(
        self,
        request: Request,
        locations: Optional[TokenLocations] = None,
        refresh: bool = False,
        optional: Literal[True] = True,
    ) -> Optional[RequestToken]:
        ...

    async def _get_token_from_request(
        self,
        request: Request,
        locations: Optional[TokenLocations] = None,
        refresh: bool = False,
        optional: bool = False,
    ) -> Optional[RequestToken]:
        if refresh and locations is None:
            locations = list(
                set(self.config.JWT_TOKEN_LOCATION).intersection(["cookies", "json"])
            )
        elif (not refresh) and locations is None:
            locations = list(self.config.JWT_TOKEN_LOCATION)
        try:
            token = await _get_token_from_request(
                request=request,
                refresh=refresh,
                locations=locations,
                config=self.config,
            )
            return token
        except MissingTokenError as e:
            if optional:
                return None
            raise e

    async def get_access_token_from_request(self, request: Request) -> RequestToken:
        """Dependency to retrieve access token from request

        Args:
            request (Request): Request to retrieve access token from

        Raises:
            MissingTokenError: When no `access` token is available in request

        Returns:
            RequestToken: Request Token instance for `access` token type
        """
        return await self._get_token_from_request(request, optional=False)

    async def get_refresh_token_from_request(self, request: Request) -> RequestToken:
        """Dependency to retrieve refresh token from request

        Args:
            request (Request): Request to retrieve refresh token from

        Raises:
            MissingTokenError: When no `refresh` token is available in request

        Returns:
            RequestToken: Request Token instance for `refresh` token type
        """
        return await self._get_token_from_request(request, refresh=True, optional=False)

    async def _auth_required(
        self,
        request: Request,
        type: str = "access",
        verify_type: bool = True,
        verify_fresh: bool = False,
        verify_csrf: Optional[bool] = None,
    ) -> TokenPayload:
        if type == "access":
            method = self.get_access_token_from_request
        elif type == "refresh":
            method = self.get_refresh_token_from_request
        else:
            ...
        if verify_csrf is None:
            verify_csrf = self.config.JWT_COOKIE_CSRF_PROTECT and (
                request.method.upper() in self.config.JWT_CSRF_METHODS
            )

        request_token = await method(
            request=request,
        )

        if self.is_token_in_blocklist(request_token.token):
            raise RevokedTokenError("Token has been revoked")

        return self.verify_token(
            request_token,
            verify_type=verify_type,
            verify_fresh=verify_fresh,
            verify_csrf=verify_csrf,
        )

    # endregion

    # region Token methods

    def verify_token(
        self,
        token: RequestToken,
        verify_type: bool = True,
        verify_fresh: bool = False,
        verify_csrf: bool = True,
    ) -> TokenPayload:
        """Verify a request token

        Args:
            token (RequestToken): RequestToken instance
            verify_type (bool, optional): Apply token type verification. Defaults to True.
            verify_fresh (bool, optional): Apply token freshness verification. Defaults to False.
            verify_csrf (bool, optional): Apply token CSRF verification. Defaults to True.

        Returns:
            TokenPayload: _description_
        """
        return token.verify(
            key=self.config.PUBLIC_KEY,
            algorithms=[self.config.JWT_ALGORITHM],
            verify_fresh=verify_fresh,
            verify_type=verify_type,
            verify_csrf=verify_csrf,
        )

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
        """Generate an Access Token

        Args:
            uid (str): Unique identifier to generate token for
            fresh (bool, optional): Generate fresh token. Defaults to False.
            headers (Optional[Dict[str, Any]], optional): TODO. Defaults to None.
            expiry (Optional[DateTimeExpression], optional): Use a user defined expiry claim. Defaults to None.
            data (Optional[Dict[str, Any]], optional): Additional data to store in token. Defaults to None.
            audience (Optional[StrOrSeq], optional): Audience claim. Defaults to None.

        Returns:
            str: Access Token
        """
        return self._create_token(
            uid=uid,
            type="access",
            fresh=fresh,
            headers=headers,
            expiry=expiry,
            data=data,
            audience=audience,
        )

    def create_refresh_token(
        self,
        uid: str,
        headers: Optional[Dict[str, Any]] = None,
        expiry: Optional[DateTimeExpression] = None,
        data: Optional[Dict[str, Any]] = None,
        audience: Optional[StrOrSeq] = None,
        *args,
        **kwargs
    ) -> str:
        """Generate a Refresh Token

        Args:
            uid (str): Unique identifier to generate token for
            headers (Optional[Dict[str, Any]], optional): TODO. Defaults to None.
            expiry (Optional[DateTimeExpression], optional): Use a user defined expiry claim. Defaults to None.
            data (Optional[Dict[str, Any]], optional): Additional data to store in token. Defaults to None.
            audience (Optional[StrOrSeq], optional): Audience claim. Defaults to None.

        Returns:
            str: Refresh Token
        """
        return self._create_token(
            uid=uid,
            type="refresh",
            headers=headers,
            expiry=expiry,
            data=data,
            audience=audience,
        )

    # endregion

    # region Cookie methods

    def set_access_cookies(
        self,
        token: str,
        response: Response,
        max_age: Optional[int] = None,
    ) -> None:
        """Add 'Set-Cookie' for access token in response header

        Args:
            token (str): Access token
            response (Response): response to set cookie on
            max_age (Optional[int], optional): Max Age cookie paramater. Defaults to None.
        """
        self._set_cookies(
            token=token, type="access", response=response, max_age=max_age
        )

    def set_refresh_cookies(
        self,
        token: str,
        response: Response,
        max_age: Optional[int] = None,
    ) -> None:
        """Add 'Set-Cookie' for refresh token in response header

        Args:
            token (str): Refresh token
            response (Response): response to set cookie on
            max_age (Optional[int], optional): Max Age cookie paramater. Defaults to None.
        """
        self._set_cookies(
            token=token, type="refresh", response=response, max_age=max_age
        )

    def unset_access_cookies(
        self,
        response: Response,
    ) -> None:
        """Remove 'Set-Cookie' for access token in response header

        Args:
            response (Response): response to remove cooke from
        """
        self._unset_cookies("access", response=response)

    def unset_refresh_cookies(
        self,
        response: Response,
    ) -> None:
        """Remove 'Set-Cookie' for refresh token in response header

        Args:
            response (Response): response to remove cooke from
        """
        self._unset_cookies("refresh", response=response)

    def unset_cookies(self, response: Response) -> None:
        """Remove 'Set-Cookie' for tokens from response headers

        Args:
            response (Response): response to remove token cookies from
        """
        self.unset_access_cookies(response)
        self.unset_refresh_cookies(response)

    # endregion

    # region Dependencies

    def get_dependency(self, request: Request, response: Response) -> FastJWTDeps:
        """FastAPI Dependency to return a FastJWT sub-object within the route context

        Args:
            request (Request): Request context managed by FastAPI
            response (Response): Response context managed by FastAPI

        Note:
            The FastJWTDeps is a utility class, to enable quick token operations
            within the route logic. It provides methods to avoid addtional code
            in your route that would be outside of the route logic

            Such methods includes setting and unsetting cookies without the need
            to generate a response object beforhand

        Returns:
            FastJWTDeps: The contextful FastJWT object
        """
        return FastJWTDeps(self, request=request, response=response)

    def token_required(
        self,
        type: str = "access",
        verify_type: bool = True,
        verify_fresh: bool = False,
        verify_csrf: Optional[bool] = None,
    ) -> Callable[[Request], TokenPayload]:
        """Dependency to enforce valid token availability in request

        Args:
            type (str, optional): Require a given token type. Defaults to "access".
            verify_type (bool, optional): Apply type verification. Defaults to True.
            verify_fresh (bool, optional): Require token freshness. Defaults to False.
            verify_csrf (Optional[bool], optional): Enable CSRF verification. Defaults to None.

        Returns:
            Callable[[Request], TokenPayload]: Dependency for Valid token Payload retrieval
        """

        async def _auth_required(request: Request):
            return await self._auth_required(
                request=request,
                type=type,
                verify_csrf=verify_csrf,
                verify_type=verify_type,
                verify_fresh=verify_fresh,
            )

        return _auth_required

    @property
    def fresh_token_required(self) -> Callable[[Request], TokenPayload]:
        """FastAPI Dependency to enforce presence of a `fresh` `access` token in request"""
        return self.token_required(
            type="access",
            verify_csrf=None,
            verify_fresh=True,
            verify_type=True,
        )

    @property
    def access_token_required(self) -> Callable[[Request], TokenPayload]:
        """FastAPI Dependency to enforce presence of an `access` token in request"""
        return self.token_required(
            type="access",
            verify_csrf=None,
            verify_fresh=False,
            verify_type=True,
        )

    @property
    def refresh_token_required(self) -> Callable[[Request], TokenPayload]:
        """FastAPI Dependency to enforce presence of a `refresh` token in request"""
        return self.token_required(
            type="refresh",
            verify_csrf=None,
            verify_fresh=False,
            verify_type=True,
        )

    async def get_current_subject(self, request: Request) -> Optional[T]:
        token: TokenPayload = await self._auth_required(request=request)
        uid = token.sub
        return self._get_current_subject(uid=uid)

    def get_token_from_request(
        self, type: TokenType = "access", optional: bool = True
    ) -> Optional[RequestToken]:
        """Return token from response if available

        Args:
            type (TokenType, optional): The type of token to retrieve from request.
                Defaults to "access".
            optional (bool, optional): Whether or not to enforce token presence in request.
                Defaults to True.

        Note:
            When `optional=True`, the return value might be `None`
            if no token is available in request

            When `optional=False`, raises a MissingTokenError

        Returns:
            Optional[RequestToken]: The RequestToken if available
        """

        async def _token_getter(request: Request):
            return await self._get_token_from_request(
                request, optional=optional, refresh=(type == "refresh")
            )

        return _token_getter

    # endregion

    # region Middlewares

    def _implicit_refresh_enabled_for_request(self, request: Request) -> bool:
        """Check if a request should implement implicit token refresh

        Args:
            request (Request): Request to check

        Returns:
            bool: True if request allows for refreshing access token
        """
        if (
            request.url.components.path
            in self.config.JWT_IMPLICIT_REFRESH_ROUTE_EXCLUDE
        ):
            refresh = False
        elif (
            request.url.components.path
            in self.config.JWT_IMPLICIT_REFRESH_ROUTE_INCLUDE
        ):
            refresh = True
        elif request.method in self.config.JWT_IMPLICIT_REFRESH_METHOD_EXCLUDE:
            refresh = False
        elif request.method in self.config.JWT_IMPLICIT_REFRESH_METHOD_INCLUDE:
            refresh = False
        else:
            refresh = True
        return refresh

    async def implicit_refresh_middleware(
        self, request: Request, call_next: Coroutine
    ) -> Response:
        """FastAPI Middleware to enable token refresh for an APIRouter

        Args:
            request (Request): Incoming request
            call_next (Coroutine): Endpoint logic to be called

        Note:
            This middleware is only based on `access` tokens.
            Using implicit refresh mechanism makes use of `refresh`
            tokens unnecessary.

        Note:
            The refreshed `access` token will not be considered as
            `fresh`

        Note:
            The implicit refresh mechanism is only enabled
            for authorization through cookies.

        Returns:
            Response: Response with update access token cookie if relevant
        """
        response = await call_next(request)

        request_condition = self.config.has_location(
            "cookies"
        ) and self._implicit_refresh_enabled_for_request(request)

        if request_condition:
            try:
                # Refresh mechanism
                token = await self._get_token_from_request(
                    request=request,
                    locations=["cookies"],
                    refresh=False,
                    optional=False,
                )
                payload = self.verify_token(token, verify_fresh=False)
                if (
                    payload.time_until_expiry
                    < self.config.JWT_IMPLICIT_REFRESH_DELTATIME
                ):
                    new_token = self.create_access_token(
                        uid=payload.sub, fresh=False, data=payload.extra_dict
                    )
                    self.set_access_cookies(new_token, response=response)
            except FastJWTException:
                pass

        return response

    # endregion
