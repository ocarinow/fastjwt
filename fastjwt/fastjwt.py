from typing import Any
from typing import Dict
from typing import Optional
from functools import partial

from fastapi import Request
from fastapi import Response

from .core import _get_token_from_request
from .types import StrOrSeq
from .types import TokenLocations
from .types import DateTimeExpression
from .utils import get_uuid
from .config import FJWTConfig
from .models import RequestToken
from .models import TokenPayload
from .exceptions import NoAuthorizationError


class FastJWTDeps:
    def __init__(self, request: Request = None, response: Response = None) -> None:
        self._response = response
        self._request = request


class FastJWT:
    """The base FastJWT object

    TODO

    """

    def __init__(self, config: FJWTConfig = FJWTConfig()) -> None:
        """see help(FastJWT)

        Args:
            config (FJWTConfig, optional): The configuration object to use. Defaults to FJWTConfig().
        """
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

    async def _get_token_from_request(
        self,
        request: Request,
        locations: Optional[TokenLocations] = None,
        refresh: bool = False,
    ) -> RequestToken:
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
                # header_name=self.config.JWT_HEADER_NAME,
                # header_type=self.config.JWT_HEADER_TYPE,
                # csrf_protect=self.config.JWT_COOKIE_CSRF_PROTECT,
                # csrf_in_form=self.config.JWT_CSRF_CHECK_FORM,
                # csrf_methods=self.config.JWT_CSRF_METHODS,
                # param_name=self.config.JWT_QUERY_STRING_NAME,
                # cookie_key=(
                #     self.config.JWT_REFRESH_COOKIE_NAME
                #     if refresh
                #     else self.config.JWT_ACCESS_COOKIE_NAME
                # ),
                # csrf_header_key=(
                #     self.config.JWT_REFRESH_CSRF_HEADER_NAME
                #     if refresh
                #     else self.config.JWT_ACCESS_CSRF_HEADER_NAME
                # ),
                # csrf_field_key=(
                #     self.config.JWT_REFRESH_CSRF_HEADER_NAME
                #     if refresh
                #     else self.config.JWT_ACCESS_CSRF_HEADER_NAME
                # ),
                # key=(
                #     self.config.JWT_REFRESH_JSON_KEY
                #     if refresh
                #     else self.config.JWT_JSON_KEY
                # ),
            )
            return token
        except NoAuthorizationError as e:
            raise e

    async def get_access_token_from_request(self, request: Request) -> RequestToken:
        """Dependency to retrieve access token from request

        Args:
            request (Request): Request to retrieve access token from

        Returns:
            RequestToken: Request Token instance for 'access' token type
        """
        return await self._get_token_from_request(request)

    async def get_refresh_token_from_request(self, request: Request) -> RequestToken:
        """Dependency to retrieve refresh token from request

        Args:
            request (Request): Request to retrieve refresh token from

        Returns:
            RequestToken: Request Token instance for 'refresh' token type
        """
        return await self._get_token_from_request(request, refresh=True)

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

        return self.verify_token(
            request_token,
            verify_type=verify_type,
            verify_fresh=verify_fresh,
            verify_csrf=verify_csrf,
        )

    def token_required(
        self,
        type: str = "access",
        verify_type: bool = True,
        verify_fresh: bool = False,
        verify_csrf: Optional[bool] = None,
    ) -> TokenPayload:
        """Dependency to enforce valid token availability in request

        Args:
            type (str, optional): Require a given token type. Defaults to "access".
            verify_type (bool, optional): Apply type verification. Defaults to True.
            verify_fresh (bool, optional): Require token freshness. Defaults to False.
            verify_csrf (Optional[bool], optional): Enable CSRF verification. Defaults to None.

        Returns:
            TokenPayload: Valid token Payload retrieved
        """
        return partial(
            self._auth_required,
            type=type,
            verify_csrf=verify_csrf,
            verify_fresh=verify_fresh,
            verify_type=verify_type,
        )

    def get_payload(self, token: str, verify: bool) -> TokenPayload:
        return self._decode_token(token=token, verify=verify)

    def get_uid(self) -> str:
        raise NotImplementedError

    def get_sub(self) -> str:
        raise NotImplementedError

    def get_subject(self) -> ...:
        raise NotImplementedError

    def get_user(self) -> ...:
        raise NotImplementedError

    def access_token_required(self) -> ...:
        raise NotImplementedError

    def refresh_token_required(self) -> ...:
        raise NotImplementedError
