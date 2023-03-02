import logging
import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Type
from typing import Generic
from typing import TypeVar
from typing import Callable
from typing import Optional

import jwt
from jwt import DecodeError
from jwt import ExpiredSignatureError
from jwt import InvalidSignatureError
from fastapi import Depends
from fastapi import Request
from fastapi import Response
from fastapi import HTTPException

import fastjwt.utils.http as HTTP_MSG

from .types import RequestToken
from .types import TokenLocations
from .payload import JWTPayload
from .settings import FastJWTConfig
from .utils.cookies import set_access_cookie
from .utils.cookies import unset_access_cookie
from .utils.parsers import FastJWTConfigType
from .utils.parsers import parse_config
from .utils._getters import get_token_from_request

P = TypeVar("P", bound=JWTPayload)
U = TypeVar("U")
JWTExecptions = (InvalidSignatureError, DecodeError, ValueError, ExpiredSignatureError)


class FastJWT(Generic[P, U]):
    """_summary_

    Args:
        Generic (JWTPayload): Payload model as a `pydantic.BaseModel`.
            Must be a child model of fastjwt.payload.JWTPayload
    """

    def __init__(
        self,
        *,
        config: FastJWTConfigType,
        user_model: Type[U] = dict,
        payload_model: Type[P] = JWTPayload,
        **kwargs
    ) -> None:
        """_summary_

        Args:
            config (FastJWTConfigType): _description_
            payload_model (Type[P], optional): _description_. Defaults to JWTPayload.
        """
        self._config: FastJWTConfig = parse_config(config=config, **kwargs)
        self._payload_model = payload_model
        self._user_model = user_model

        self.user_getter: Optional[Callable[[str], U]] = None
        self.token_blacklist_checker: Optional[Callable[[str], bool]] = None

    @property
    def config(self) -> FastJWTConfig:
        return self._config

    @classmethod
    def from_object(cls, config: FastJWTConfigType) -> "FastJWT":
        return cls(config=config)

    @classmethod
    def from_file(cls, file: str) -> "FastJWT":
        raise NotImplementedError

    def set_user_getter(self, callback: Callable[[str], U]) -> None:
        self.user_getter = callback

    def set_token_checker(self, callback: Callable[[str], bool]) -> None:
        self.token_blacklist_checker = callback

    def get_user_from_uid(self, uid: str) -> U:
        return self.user_getter(uid)

    def is_token_blacklisted(self, token: str) -> bool:
        if self.token_blacklist_checker is None:
            return False
        return self.token_blacklist_checker(token)

    def encode_jwt(self, payload: Dict[str, Any]) -> str:
        """Encode a payload as a JWT

        Args:
            payload (Dict[str, Any]): Payload to encode

        Returns:
            str: Encoded JWT
        """
        return jwt.encode(
            payload,
            key=self.config._JWT_PRIVATE_KEY,
            algorithm=self.config.JWT_ALGORITHM,
        )

    def decode_jwt(self, encoded_token: str) -> Dict[str, Any]:
        """Decode a JWT

        Args:
            encoded_token (str): JWT to decode

        Returns:
            Dict[str, Any]: Decoded payload
        """
        return jwt.decode(
            encoded_token,
            key=self.config._JWT_PUBLIC_KEY,
            algorithms=[self.config.JWT_ALGORITHM],
        )

    # region Time Ops
    @staticmethod
    def get_utcnow() -> datetime.datetime:
        return datetime.datetime.now(tz=datetime.timezone.utc)

    def get_payload_expiry(self, payload: P) -> datetime.datetime:
        if payload.exp is None:
            return payload.issued_date + self.config.JWT_EXPIRE_DELTATIME
        return datetime.datetime.fromtimestamp(payload.exp, tz=datetime.timezone.utc)

    def get_delta_until_expiry(self, payload: P) -> datetime.timedelta:
        return self.get_payload_expiry(payload) - self.get_utcnow()

    def is_payload_expired(self, payload: P) -> bool:
        return self.get_payload_expiry(payload) < self.get_utcnow()

    def verify_expiry(self, payload: P) -> bool:
        return not self.is_payload_expired(payload)

    # endregion

    def verify_token(self, token: str, require_fresh: bool = False) -> bool:
        """Verify if a token is genuine

        Check for the decoding ,the expiry time, the token blacklist and the freshness of the token.

        Args:
            token (str): Token
            require_fresh (bool): require the token to be fresh

        Returns:
            bool: Whether or not the token is valid
        """
        try:
            decoded_token: Dict = self.decode_jwt(token)
            payload = self._payload_model.parse_obj(decoded_token)
            # Check freshness
            if require_fresh and not payload.fresh:
                return False
            # Check if the token is still valid
            if self.config.JWT_IS_TOKEN_EXPIRABLE and self.is_payload_expired(payload):
                return False
            # Check if token in blacklist
            if self.is_token_blacklisted(token):
                return False
            return True
        except JWTExecptions as e:
            logging.error(e)
            return False
        except Exception as e:
            logging.error(e)
            return False

    def create_access_token(
        self,
        uid: str,
        permissions: Optional[List[str]] = None,
        expires_delta: Optional[datetime.timedelta] = None,
        fresh: bool = False,
        **kwargs
    ) -> str:
        """Create an access token for a user

        Args:
            uid (str): User UID
            permissions (Optional[List[str]], optional): List of privileges. Defaults to None.
            expires_delta (Optional[datetime.timedelta], optional): JWT expiry time, if None will use the `config` expiry time.
                Defaults to None.
            fresh (bool): Whether to generate a fresh token or not. Defaults to False.

        Returns:
            str: Access token
        """
        iat = self.get_utcnow()
        # Compute Expiration
        if expires_delta:
            # Highest priority: Use the argument
            exp = iat + expires_delta
        elif self.config.JWT_IS_TOKEN_EXPIRABLE:
            # Lowest priority: Use the config expiration deltatime
            exp = iat + self.config.JWT_EXPIRE_DELTATIME
        else:
            # Set exp as None
            exp = None

        payload = self._payload_model(
            uid=uid,
            iat=int(iat.timestamp()),
            exp=int(exp.timestamp() if exp else None),
            permissions=permissions,
            fresh=fresh,
            **kwargs
        )

        access_token = self.encode_jwt(payload=payload.dict())
        return access_token

    def refresh_token(self, token: str, explicit: bool = False) -> Optional[str]:
        """Refresh an access token

        Args:
            token (str): Access token to refresh
            explicit (bool, optional): Enforce refresh if the implicit refresh is not enabled. Defaults to False.

        Returns:
            Optional[str]: Refreshed access token
        """
        if not self.config.JWT_EXPIRE_DELTATIME:
            # The expiration is set to False,
            # no need for refresh token
            return
        if not self.config.JWT_ENABLE_COOKIE_IMPLICIT_REFRESH and not explicit:
            # The automated refresh is disabled
            return
        try:
            decoded_token = self.decode_jwt(token)
            payload = self._payload_model.parse_obj(decoded_token)
            if (
                datetime.timedelta(seconds=0)
                < self.get_delta_until_expiry(payload)
                < self.config.JWT_REFRESH_DELTATIME
            ):
                # The token needs to be refreshed
                return self.create_access_token(
                    uid=payload.uid, permissions=payload.permissions, fresh=False
                )
            return
        except Exception as e:
            logging.error(e)
            return

    def set_access_cookie(self, response: Response, token: str) -> None:
        """Set access token cookie in response

        Args:
            response (Response): response
            token (str): access token
        """
        set_access_cookie(response=response, token=token, config=self.config)

    def unset_access_cookie(self, response: Response) -> None:
        """Remove access token in cookies

        Args:
            response (Response): reponse
        """
        unset_access_cookie(response=response, config=self.config)

    async def _auth_required(self, request: Request, require_fresh: bool) -> str:
        """Dependency for authentication requirement for routes

        Args:
            request (Request): request to authenticate
            require_fresh (bool): if True requires the token to be fresh

        Raises:
            HTTPException(401): Token is not available
            HTTPException(401): Token is not valid

        Returns:
            str: Current user UID
        """
        # Get token from request
        token = await get_token_from_request(request, config=self.config)
        if not token or not token.access_token:
            raise HTTPException(status_code=401, detail=HTTP_MSG.MSG_MISSING_TOKEN)
        try:
            if not self.verify_token(token.access_token, require_fresh=require_fresh):
                raise HTTPException(
                    status_code=401,
                    detail=HTTP_MSG.MSG_FRESH_TOKEN_REQUIRED
                    if require_fresh
                    else HTTP_MSG.MSG_401,
                )
            # Return User UID
            return self._payload_model.parse_obj(
                self.decode_jwt(token.access_token)
            ).uid
        except HTTPException as e:
            logging.error(e)
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        except Exception as e:
            logging.exception(e)
            raise HTTPException(status_code=401, detail=HTTP_MSG.MSG_401)

    async def auth_required(self, request: Request) -> str:
        """Dependency for authentication requirement for routes

        Args:
            request (Request): request to authenticate

        Raises:
            HTTPException(401): Token is not available
            HTTPException(401): Token is not valid

        Returns:
            str: Current user UID
        """
        return await self._auth_required(request=request, require_fresh=False)

    async def fresh_auth_required(self, request: Request) -> str:
        """Dependency for FRESH authentication requirement for routes

        Args:
            request (Request): request to authenticate

        Raises:
            HTTPException(401): Token is not available
            HTTPException(401): Token is not valid

        Returns:
            str: Current user UID
        """
        return await self._auth_required(request=request, require_fresh=True)

    async def get_token_from_request(
        self,
        request: Request,
        locations: TokenLocations = ["cookies", "headers", "json", "query"],
    ) -> Optional[RequestToken]:
        """Get the access token from a request

        Args:
            request (Request): the request to analyse
            locations (TokenLocations, optional): Locations to look the token for. Defaults to ["cookies", "headers", "json", "query"].

        Returns:
            Optional[RequestToken]: The detected access token
        """
        return await get_token_from_request(
            request=request, locations=locations, config=self.config
        )

    async def implicit_refresh_cookie_middleware(
        self, request: Request, call_next: Callable
    ) -> Response:
        """Refresh access token cookie after request middleware

        Args:
            request (Request): request
            call_next (Callable): route function

        Returns:
            Response: response
        """
        response = await call_next(request)
        if request.url.components.path in self.config.JWT_EXCLUDE_REFRESH_ROUTES:
            return response
        # Get token if available in "cookies"
        token = await self.get_token_from_request(
            request=request, locations=["cookies"]
        )
        # Refresh token if necessary
        try:
            new_token = (
                self.refresh_token(
                    token=token.access_token,
                    explicit=self._payload_model.parse_obj(
                        self.decode_jwt(token.access_token)
                    ).fresh,
                )
                if token
                and token.access_token
                and self.verify_token(token=token.access_token)
                else None
            )
        except Exception as e:
            logging.error(e)
            new_token = None
        # Set new token in cookie if necessary
        set_access_cookie(response=response, token=new_token) if new_token else None
        return response

    @property
    def get_current_user_callback(self) -> Callable[[str], U]:
        async def get_current_user(uid: str = Depends(self.auth_required)) -> U:
            """Returns user as model from its UID

            Args:
                uid (str): User UIS. Defaults to Depends(auth_required).

            Returns:
                User: User ORM instance
            """
            if self.user_getter is None:
                raise Exception(
                    "You must define an accessor via the `FastJWT.set_user_getter` method"
                )
            return self.get_user_from_uid(uid=uid)

        return get_current_user

    @property
    def get_current_fresh_user_callback(self) -> Callable[[str], U]:
        async def get_current_fresh_user(
            uid: str = Depends(self.fresh_auth_required),
        ) -> U:
            """Returns frehs user as model from its UID

            Args:
                uid (str): User UIS. Defaults to Depends(auth_required).

            Returns:
                User: User ORM instance
            """
            if self.user_getter is None:
                raise Exception(
                    "You must define an accessor via the `FastJWT.set_user_getter` method"
                )
            return self.get_user_from_uid(uid=uid)

        return get_current_fresh_user
