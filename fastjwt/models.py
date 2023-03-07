import datetime
from hmac import compare_digest
from typing import Any
from typing import Dict
from typing import List
from typing import Iterable
from typing import Optional

from pydantic import Extra
from pydantic import Field
from pydantic import BaseModel
from pydantic import ValidationError
from pydantic import validator

from .token import create_token
from .token import decode_token
from .types import Union
from .types import Numeric
from .types import StrOrIter
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


class TokenPayload(BaseModel):
    """_summary_"""

    jti: Optional[str] = Field(default_factory=get_uuid)
    iss: Optional[str] = None
    sub: Optional[str] = None
    aud: Optional[str] = None
    exp: Optional[Union[Numeric, DateTimeExpression]] = None
    nbf: Optional[Union[Numeric, DateTimeExpression]] = None
    iat: Optional[Union[Numeric, DateTimeExpression]] = Field(
        default_factory=get_now_ts
    )
    type: Optional[str] = None
    csrf: Optional[str] = None
    scopes: Optional[List[str]] = None
    fresh: bool = False

    class Config:
        extra = Extra.allow

    @property
    def additional_fields(self) -> set[str]:
        return set(self.__dict__) - set(self.__fields__)

    @validator("exp", "nbf", always=True)
    def set_default_ts(cls, value):
        if isinstance(value, datetime.datetime):
            return value.timestamp()
        elif isinstance(value, datetime.timedelta):
            return (get_now() + value).timestamp()
        return value

    def has_scopes(self, *scopes: Iterable[str]) -> bool:
        return all([s in self.scopes for s in scopes])

    def encode(
        self,
        key: str,
        algorithm: str,
        ignore_errors: bool = True,
        headers: Optional[Dict[str, Any]] = None,
    ) -> str:
        # TODO
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
        algorithms: Iterable[AlgorithmType] = ["HS256"],
        audience: Optional[StrOrIter] = None,
        issuer: Optional[str] = None,
        verify: bool = True,
    ) -> "TokenPayload":
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
    token: Optional[str] = None
    csrf: Optional[str] = None
    type: TokenType = "access"
    location: TokenLocation

    def verify(
        self,
        key: str,
        algorithms: Iterable[AlgorithmType] = ["HS256"],
        audience: Optional[StrOrIter] = None,
        issuer: Optional[str] = None,
        verify_jwt: bool = True,
        verify_type: bool = True,
        verify_csrf: bool = True,
        verify_fresh: bool = False,
    ) -> TokenPayload:
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
            print("JWTERROR", e.args)
            raise JWTDecodeError(e.args[0])
        except ValidationError as e:
            raise JWTDecodeError(e.args[0])

        # TODO Verify Headers

        if verify_type and (self.type != payload.type):
            raise TokenTypeError(
                f"'{self.type}' token required, '{payload.type}' token received"
            )

        if verify_fresh and not payload.fresh:
            raise FreshTokenRequiredError("Fresh token required")

        if verify_csrf:
            if self.csrf is None:
                raise CSRFError("Missing CSRF in request")
            if payload.csrf is None:
                raise CSRFError("Missing 'csrf' claim")
            if not compare_digest(self.csrf, payload.csrf):
                raise CSRFError("CSRF double submit does not match")

        return payload
