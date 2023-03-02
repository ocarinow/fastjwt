import os
import datetime
from typing import List
from typing import Union
from typing import Literal
from typing import Optional
from typing import TypedDict
from distutils.util import strtobool

from pydantic import BaseSettings

from .types import SamesiteType
from .types import AlgorithmType
from .types import TokenLocations
from .errors import BadConfigurationError
from .utils.secrets import decode_base64_key


class FastJWTConfigDict(TypedDict):
    _JWT_SECRET_KEY: Optional[str]
    _JWT_PUBLIC_KEY: Optional[str]
    _JWT_PRIVATE_KEY: Optional[str]
    JWT_ALGORITHM: Optional[AlgorithmType]
    _JWT_LOCATIONS: Optional[Union[str, TokenLocations]]
    _JWT_EXCLUDE_REFRESH_ROUTES: Optional[Union[str, List[str]]]
    JWT_EXPIRE_DELTATIME: Optional[datetime.timedelta]
    JWT_REFRESH_DELTATIME: Optional[datetime.timedelta]
    JWT_HEADER_NAME: Optional[str]
    JWT_HEADER_TYPE: Optional[str]
    JWT_COOKIE_PATH: Optional[str]
    JWT_COOKIE_DOMAIN: Optional[str]
    JWT_COOKIE_SECURE: Optional[bool]
    JWT_COOKIE_HTTPONLY: Optional[bool]
    JWT_COOKIE_MAX_AGE: Optional[Optional[str]]
    JWT_COOKIE_EXPIRES: Optional[Optional[str]]
    JWT_COOKIE_SAMESITE: Optional[SamesiteType]
    JWT_JSON_ACCESS_KEY: Optional[str]
    JWT_JSON_REFRESH_KEY: Optional[str]
    JWT_QUERY_STRING_NAME: Optional[str]


class FastJWTConfig(BaseSettings):
    """Configuration object"""

    # Secret Keys & Algorithm
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "")
    JWT_PUBLIC_KEY: str = os.getenv("JWT_PUBLIC_KEY", "")
    JWT_PRIVATE_KEY: str = os.getenv("JWT_PRIVATE_KEY", "")
    JWT_ALGORITHM: AlgorithmType = os.getenv("JWT_ALGORITHM", "RS256")

    # JWT Base Configuration
    _JWT_LOCATIONS: Union[str, TokenLocations] = os.getenv(
        "JWT_LOCATIONS", "cookies,headers,json,query"
    )
    _JWT_EXCLUDE_REFRESH_ROUTES: Union[str, List[str]] = os.getenv(
        "JWT_EXCLUDE_REFRESH_ROUTES", "/logout,/login"
    )
    JWT_EXPIRE_DELTATIME: datetime.timedelta = datetime.timedelta(minutes=15)
    JWT_REFRESH_DELTATIME: datetime.timedelta = datetime.timedelta(minutes=10)

    # JWT Header Configuration
    JWT_HEADER_NAME: str = os.getenv("JWT_HEADER_NAME", "Authorization")
    JWT_HEADER_TYPE: str = os.getenv("JWT_HEADER_TYPE", "Bearer")

    # JWT Cookie Configuration
    JWT_COOKIE_PATH: str = os.getenv("JWT_COOKIE_PATH", "/")
    JWT_COOKIE_NAME: str = os.getenv("JWT_COOKIE_NAME", "access_token_cookie")
    JWT_COOKIE_DOMAIN: str = os.getenv("JWT_COOKIE_DOMAIN", "")
    JWT_COOKIE_SECURE: bool = strtobool(os.getenv("JWT_COOKIE_SECURE", "true"))
    JWT_COOKIE_HTTPONLY: bool = strtobool(os.getenv("JWT_COOKIE_HTTPONLY", "true"))
    JWT_COOKIE_MAX_AGE: Optional[str] = os.getenv("JWT_COOKIE_MAX_AGE", None)
    JWT_COOKIE_EXPIRES: Optional[str] = os.getenv("JWT_COOKIE_EXPIRES", None)
    JWT_COOKIE_SAMESITE: SamesiteType = os.getenv("JWT_COOKIE_SAMESITE", "lax")

    # JWT JSON Configuration
    JWT_JSON_ACCESS_KEY: str = os.getenv("JWT_JSON_ACCESS_KEY", "access_token")
    JWT_JSON_REFRESH_KEY: str = os.getenv("JWT_JSON_REFRESH_KEY", "refresh_token")

    # JWT Query Configuration
    JWT_QUERY_STRING_NAME: str = os.getenv("JWT_QUERY_STRING_NAME", "token")

    # Properties
    @property
    def JWT_EXCLUDE_REFRESH_ROUTES(self) -> List[str]:
        return self._JWT_EXCLUDE_REFRESH_ROUTES.split(",")

    @property
    def JWT_ENABLE_COOKIE_IMPLICIT_REFRESH(self) -> bool:
        return bool(self.JWT_REFRESH_DELTATIME)

    @property
    def JWT_IS_TOKEN_EXPIRABLE(self) -> bool:
        return isinstance(self.JWT_EXPIRE_DELTATIME, datetime.timedelta)

    @property
    def JWT_LOCATIONS(self) -> TokenLocations:
        if isinstance(self._JWT_LOCATIONS, str):
            return self._JWT_LOCATIONS.split(",")
        else:
            return self._JWT_LOCATIONS

    @property
    def _JWT_PUBLIC_KEY(self) -> str:
        if self.JWT_ALGORITHM == "RS256":
            return decode_base64_key(self.JWT_PUBLIC_KEY)
        elif self.JWT_ALGORITHM == "HS256":
            return decode_base64_key(self.JWT_SECRET_KEY)
        else:
            raise BadConfigurationError("Algorithm is not valid")

    @property
    def _JWT_PRIVATE_KEY(self) -> str:
        if self.JWT_ALGORITHM == "RS256":
            return decode_base64_key(self.JWT_PRIVATE_KEY)
        elif self.JWT_ALGORITHM == "HS256":
            return decode_base64_key(self.JWT_SECRET_KEY)
        else:
            raise BadConfigurationError("Algorithm is not valid")
