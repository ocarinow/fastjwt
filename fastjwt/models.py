import datetime
from hmac import compare_digest
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence

from pydantic import Extra
from pydantic import Field
from pydantic import BaseModel
from pydantic import ValidationError
from pydantic import validator

from .token import create_token
from .token import decode_token
from .types import Union
from .types import Numeric
from .types import StrOrSeq
from .types import TokenType
from .types import AlgorithmType
from .types import TokenLocation
from .types import DateTimeExpression
from .utils import get_now
from .utils import get_uuid
from .utils import get_now_ts
from .exceptions import CSRFError
from .exceptions import JWTDecodeError
from .exceptions import TokenTypeError
from .exceptions import FreshTokenRequiredError
from .exceptions import AccessTokenRequiredError
from .exceptions import RefreshTokenRequiredError


class TokenPayload(BaseModel):
    """JWT Payload base model

    Args:
        jti (Optional[str]): JWT unique identifier. Defaults to UUID4.
        iss (Optional[str]): JWT issuer. Defaults to None.
        sub (Optional[str]): JWT subject. Defaults to None.
        aud (Optional[str]): JWT audience. Defaults to None.
        exp (Numeric | DateTimeExpression | None): Expiry date claim. Defaults to None.
        nbf (Numeric | DateTimeExpression | None): Not before claim. Defaults to None.
        iat (Numeric | DateTimeExpression | None): Issued at claim. Defaults to None.
        type (Optional[str]): Token type. Default to None.
        csrf (Optional[str]): CSRF double submit token. Default to None.
        scopes (Optional[List[str]]): TODO.
        fresh (bool): Token freshness state. Defaults to False.
    """

    jti: Optional[str] = Field(default_factory=get_uuid)
    iss: Optional[str] = None
    sub: Optional[str] = None
    aud: Optional[str] = None
    exp: Optional[Union[Numeric, DateTimeExpression]] = None
    nbf: Optional[Union[Numeric, DateTimeExpression]] = None
    iat: Optional[Union[Numeric, DateTimeExpression]] = Field(
        default_factory=lambda: int(get_now_ts())
    )
    type: Optional[str] = None
    csrf: Optional[str] = None
    scopes: Optional[List[str]] = None
    fresh: bool = False

    class Config:
        extra = Extra.allow

    @property
    def _additional_fields(self) -> set[str]:
        return set(self.__dict__) - set(self.__fields__)

    @property
    def extra_dict(self):
        return self.dict(include=self._additional_fields)

    @property
    def issued_at(self) -> datetime.datetime:
        """Cast the 'iat' claim as a datetime.datetime

        Raises:
            TypeError: 'iat' claim is not of type float | int | datetime.datetime

        Returns:
            datetime.datetime: UTC Datetime token issued date
        """
        if isinstance(self.iat, (float, int)):
            return datetime.datetime.fromtimestamp(self.iat, tz=datetime.timezone.utc)
        elif isinstance(self.iat, datetime.datetime):
            return self.iat
        else:
            raise TypeError(
                "'iat' claim should be of type float | int | datetime.datetime"
            )

    @property
    def expiry_datetime(self) -> datetime.datetime:
        """Cast the 'exp' claim as a datetime.datetime

        Raises:
            TypeError: 'exp' claim is not of type float | int | datetime.datetime | datetime.timedelta

        Returns:
            datetime.datetime: UTC Datetime token expiry date
        """
        if isinstance(self.exp, datetime.datetime):
            return self.exp
        elif isinstance(self.exp, datetime.timedelta):
            return self.issued_at + self.exp
        elif isinstance(self.exp, (float, int)):
            return datetime.datetime.fromtimestamp(self.exp, tz=datetime.timezone.utc)
        else:
            raise TypeError(
                "'exp' claim should be of type float | int | datetime.datetime | datetime.timedelta"
            )

    @property
    def time_until_expiry(self) -> datetime.timedelta:
        """Return the time remaining until expiry

        Returns:
            datetime.timedelta: time remaining until expiry
        """
        return self.expiry_datetime - get_now()

    @property
    def time_since_issued(self) -> datetime.timedelta:
        """Return the time elapsed since token has been issued

        Returns:
            datetime.timedelta: time elapsed since token has been issued
        """
        return get_now() - self.issued_at

    @validator("exp", "nbf", always=True)
    def _set_default_ts(cls, value):
        if isinstance(value, datetime.datetime):
            return value.timestamp()
        elif isinstance(value, datetime.timedelta):
            return (get_now() + value).timestamp()
        return value

    def has_scopes(self, *scopes: Sequence[str]) -> bool:
        """Checks if a given scope is contained within TokenPayload scopes

        Args:
            *scopes (Sequence[str]): scopes to verify

        Returns:
            bool: Whether the scopes are contained in the payload scopes
        """
        return all([s in self.scopes for s in scopes])

    def encode(
        self,
        key: str,
        algorithm: str,
        ignore_errors: bool = True,
        headers: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Encode the payload

        Args:
            key (str): Secret key to encode the payload
            algorithm (str): Algorithm to use to encode the payload
            ignore_errors (bool, optional): Ignore validation errors. Defaults to True.
            headers (Optional[Dict[str, Any]], optional): TODO. Defaults to None.

        Returns:
            str: encoded token
        """
        # TODO Handle Headers
        # TODO Handle Extra fields
        return create_token(
            key=key,
            algorithm=algorithm,
            uid=self.sub,
            jti=self.jti,
            issued=self.iat,
            type=self.type,
            expiry=self.exp,
            fresh=self.fresh,
            csrf=self.csrf,
            audience=self.aud,
            issuer=self.iss,
            not_before=self.nbf,
            ignore_errors=ignore_errors,
            headers=headers,
        )

    @classmethod
    def decode(
        cls,
        token: str,
        key: str,
        algorithms: Sequence[AlgorithmType] = ["HS256"],
        audience: Optional[StrOrSeq] = None,
        issuer: Optional[str] = None,
        verify: bool = True,
    ) -> "TokenPayload":
        """Given a token returns the associated JWT payload

        Args:
            token (str): Token to decode
            key (str): Secret to decode the token
            algorithms (Sequence[AlgorithmType], optional): Algorithms to use to decode the token. Defaults to ["HS256"].
            audience (Optional[StrOrSeq], optional): Audience to verify. Defaults to None.
            issuer (Optional[str], optional): Issuer to verify. Defaults to None.
            verify (bool, optional): Enable verification. Defaults to True.

        Returns:
            TokenPayload: The decoded JWT payload
        """
        payload = decode_token(
            token=token,
            key=key,
            algorithms=algorithms,
            audience=audience,
            issuer=issuer,
            verify=verify,
        )
        return cls.parse_obj(payload)


class RequestToken(BaseModel):
    """Base model for token data retrieved from requests

    Args:
        type (TokenType): Type of token. Defaults to access.
        token (Optional[str]): The token retrieved from the request. Defaults to None.
        csrf (Optional[str]): CSRF Value in request if detailed. Defaults to None.
        location (TokenLocation): Where the token was found in request.
    """

    token: Optional[str] = None
    csrf: Optional[str] = None
    type: TokenType = "access"
    location: TokenLocation

    def verify(
        self,
        key: str,
        algorithms: Sequence[AlgorithmType] = ["HS256"],
        audience: Optional[StrOrSeq] = None,
        issuer: Optional[str] = None,
        verify_jwt: bool = True,
        verify_type: bool = True,
        verify_csrf: bool = True,
        verify_fresh: bool = False,
    ) -> TokenPayload:
        """Verify a RequestToken

        Args:
            key (str): Secret to decode the token
            algorithms (Sequence[AlgorithmType], optional): Algorithms to use to decode the token. Defaults to ["HS256"].
            audience (Optional[StrOrSeq], optional): Audience claim to verify. Defaults to None.
            issuer (Optional[str], optional): Issuer claim to verify. Defaults to None.
            verify_jwt (bool, optional): Enable base JWT verification. Defaults to True.
            verify_type (bool, optional): Enable token type verification. Defaults to True.
            verify_csrf (bool, optional): Enable CSRF verification. Defaults to True.
            verify_fresh (bool, optional): Enable token freshness verification. Defaults to False.

        Raises:
            JWTDecodeError: Error while decoding the token
            JWTDecodeError: The base JWT verification step has failed
            FreshTokenRequiredError: The token is not fresh
            CSRFError: A CSRF token is missing in the request
            CSRFError: No CSRF claim is contained in the token
            CSRFError: CSRF double submit does not match

        Returns:
            TokenPayload: The payload encoded in the token
        """
        # JWT Base Verification
        try:
            decoded_token = decode_token(
                token=self.token,
                key=key,
                algorithms=algorithms,
                verify=verify_jwt,
                audience=audience,
                issuer=issuer,
            )
            # Parse payload
            payload = TokenPayload.parse_obj(decoded_token)
        except JWTDecodeError as e:
            raise JWTDecodeError(*e.args)
        except ValidationError as e:
            raise JWTDecodeError(*e.args)

        # TODO Verify Headers

        if verify_type and (self.type != payload.type):
            error_msg = f"'{self.type}' token required, '{payload.type}' token received"
            if self.type == "access":
                raise AccessTokenRequiredError(error_msg)
            elif self.type == "refresh":
                raise RefreshTokenRequiredError(error_msg)
            raise TokenTypeError(error_msg)

        if verify_fresh and not payload.fresh:
            raise FreshTokenRequiredError("Fresh token required")

        if verify_csrf and self.location == "cookies":
            if self.csrf is None:
                raise CSRFError("Missing CSRF in request")
            if payload.csrf is None:
                raise CSRFError("Missing 'csrf' claim")
            if not compare_digest(self.csrf, payload.csrf):
                raise CSRFError("CSRF double submit does not match")

        return payload
