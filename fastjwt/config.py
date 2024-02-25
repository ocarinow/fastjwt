from typing import List
from typing import Optional
from typing import Sequence
from datetime import timedelta

from pydantic import Field
from jwt.algorithms import requires_cryptography
from jwt.algorithms import get_default_algorithms
from pydantic_settings import BaseSettings

from .types import StrOrSeq
from .types import HTTPMethods
from .types import AlgorithmType
from .types import SameSitePolicy
from .types import TokenLocations
from .exceptions import BadConfigurationError


class FJWTConfig(BaseSettings):
    """FastJWT Base Configuration Object"""

    # General Options
    JWT_ACCESS_TOKEN_EXPIRES: Optional[timedelta] = timedelta(minutes=15)
    JWT_ALGORITHM: AlgorithmType = "HS256"
    JWT_DECODE_ALGORITHMS: Sequence[AlgorithmType] = Field(
        default_factory=lambda: ["HS256"]
    )
    JWT_DECODE_AUDIENCE: Optional[StrOrSeq] = None
    JWT_DECODE_ISSUER: Optional[str] = None
    JWT_DECODE_LEEWAY: Optional[int] = 0
    JWT_ENCODE_AUDIENCE: Optional[StrOrSeq] = None
    JWT_ENCODE_ISSUER: Optional[str] = None
    JWT_ENCODE_NBF: bool = True
    JWT_ERROR_MESSAGE_KEY: str = "msg"
    JWT_IDENTITY_CLAIM: str = "sub"
    JWT_PRIVATE_KEY: Optional[str] = None
    JWT_PUBLIC_KEY: Optional[str] = None
    JWT_REFRESH_TOKEN_EXPIRES: Optional[timedelta] = timedelta(days=20)
    JWT_SECRET_KEY: Optional[str] = None
    JWT_TOKEN_LOCATION: TokenLocations = Field(["headers"])
    # Header Options
    JWT_HEADER_NAME: str = "Authorization"
    JWT_HEADER_TYPE: str = "Bearer"
    # Cookies Options
    JWT_ACCESS_COOKIE_NAME: str = "access_token_cookie"
    JWT_ACCESS_COOKIE_PATH: str = "/"
    JWT_COOKIE_CSRF_PROTECT: bool = True
    JWT_COOKIE_DOMAIN: Optional[str] = None
    JWT_COOKIE_MAX_AGE: Optional[int] = None
    JWT_COOKIE_SAMESITE: SameSitePolicy = "Lax"
    JWT_COOKIE_SECURE: bool = True
    JWT_REFRESH_COOKIE_NAME: str = "refresh_token_cookie"
    JWT_REFRESH_COOKIE_PATH: str = "/"
    JWT_SESSION_COOKIE: bool = True
    # CSRF Options
    JWT_ACCESS_CSRF_COOKIE_NAME: str = "csrf_access_token"
    JWT_ACCESS_CSRF_COOKIE_PATH: str = "/"
    JWT_ACCESS_CSRF_FIELD_NAME: str = "csrf_token"
    JWT_ACCESS_CSRF_HEADER_NAME: str = "X-CSRF-TOKEN"
    JWT_CSRF_CHECK_FORM: bool = False
    JWT_CSRF_IN_COOKIES: bool = True
    JWT_CSRF_METHODS: HTTPMethods = Field(
        default_factory=lambda: ["POST", "PUT", "PATCH", "DELETE"]
    )
    JWT_REFRESH_CSRF_COOKIE_NAME: str = "csrf_refresh_token"
    JWT_REFRESH_CSRF_COOKIE_PATH: str = "/"
    JWT_REFRESH_CSRF_FIELD_NAME: str = "csrf_token"
    JWT_REFRESH_CSRF_HEADER_NAME: str = "X-CSRF-TOKEN"
    # Query Options
    JWT_QUERY_STRING_NAME: str = "token"
    # JSON Option
    JWT_JSON_KEY: str = "access_token"
    JWT_REFRESH_JSON_KEY: str = "refresh_token"

    # Implicit Refresh Options
    JWT_IMPLICIT_REFRESH_ROUTE_EXCLUDE: List[str] = Field(default_factory=list)
    JWT_IMPLICIT_REFRESH_ROUTE_INCLUDE: List[str] = Field(default_factory=list)
    JWT_IMPLICIT_REFRESH_METHOD_EXCLUDE: HTTPMethods = Field(default_factory=list)
    JWT_IMPLICIT_REFRESH_METHOD_INCLUDE: HTTPMethods = Field(default_factory=list)
    JWT_IMPLICIT_REFRESH_DELTATIME: timedelta = timedelta(minutes=10)

    @property
    def is_algo_symmetric(self) -> bool:
        """Check if the JWT_ALGORITHM is a symmetric encryption algorithm

        Returns:
            bool: Whether or not the algorithm is symmetric
        """
        return (
            self.JWT_ALGORITHM in get_default_algorithms()
            and self.JWT_ALGORITHM not in requires_cryptography
        )

    @property
    def is_algo_asymmetric(self) -> bool:
        """Check if the JWT_ALGORITHM is an asymmetric encryption algorithm

        Returns:
            bool: Whether or not the algorithm is asymmetric
        """
        return (
            self.JWT_ALGORITHM in get_default_algorithms()
            and self.JWT_ALGORITHM in requires_cryptography
        )

    def _get_key(self, crypto_value: str) -> str:
        if self.is_algo_symmetric:
            key = self.JWT_SECRET_KEY
        elif self.is_algo_asymmetric:
            key = crypto_value
        else:
            raise BadConfigurationError(
                f"Bad Algorithm. Value allowed are '{get_default_algorithms()}'"
            )

        if key is None:
            raise BadConfigurationError(
                "SECRET is None.",
                "Be sure to check the algorithm and to set JWT_SECRET_KEY | JWT_PUBLIC_KEY | JWT_PRIVATE_KEY accordingly",
            )
        return key

    def has_location(self, location: str) -> bool:
        """Check if a given token location is allowed by the configuration

        Args:
            location (str): Token location

        Returns:
            bool: Whether or not the location is contained in JWT_TOKEN_LOCATION
        """
        return location in self.JWT_TOKEN_LOCATION

    @property
    def PRIVATE_KEY(self) -> str:
        """Private key to encode token

        Returns:
            str: Private key
        """
        return self._get_key(self.JWT_PRIVATE_KEY)

    @property
    def PUBLIC_KEY(self) -> str:
        """Public key to decode token

        Returns:
            str: Public key
        """
        return self._get_key(self.JWT_PUBLIC_KEY)
