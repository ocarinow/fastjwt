import datetime
from typing import Any
from typing import Dict
from typing import Union
from typing import Iterable
from typing import Optional

import jwt

from .types import StrOrIter
from .types import TokenType
from .types import AlgorithmType
from .types import DateTimeExpression
from .utils import get_now
from .utils import get_uuid
from .utils import get_now_ts
from .exceptions import JWTDecodeError

RESERVED_CLAIMS = set(
    ["fresh", "csrf", "iat", "exp", "iss", "aud", "type", "jti", "nbf", "sub"]
)


def create_token(
    uid: str,
    key: str,
    type: TokenType,
    jti: Optional[str] = None,
    expiry: Optional[DateTimeExpression] = None,
    issued: Optional[DateTimeExpression] = None,
    fresh: bool = False,
    csrf: Union[str, bool] = True,
    algorithm: AlgorithmType = "HS256",
    headers: Optional[Dict[str, Any]] = None,
    audience: Optional[StrOrIter] = None,
    issuer: Optional[str] = None,
    additional_data: Optional[Dict[str, Any]] = None,
    not_before: Optional[Union[int, DateTimeExpression]] = None,
    ignore_errors: bool = True,
) -> str:
    now = get_now()

    # Filter additional data to remove JWT claims
    additional_claims = {}
    if additional_data is not None:
        if (not ignore_errors) and (
            len(set(additional_data.keys()).intersection(RESERVED_CLAIMS)) > 0
        ):
            raise ValueError(f"{RESERVED_CLAIMS} are forbidden in additional claims")
        additional_claims = {
            k: v for k, v in additional_data.items() if k not in RESERVED_CLAIMS
        }

    jwt_claims = {"sub": uid, "jti": jti if jti else get_uuid(), "type": type}

    if type == "access":
        jwt_claims["fresh"] = fresh

    if csrf and not isinstance(csrf, str):
        jwt_claims["csrf"] = get_uuid()
    elif isinstance(csrf, str):
        jwt_claims["csrf"] = csrf

    if isinstance(issued, datetime.datetime):
        jwt_claims["iat"] = issued.timestamp()
    elif isinstance(issued, (float, int)):
        jwt_claims["iat"] = issued
    else:
        jwt_claims["iat"] = get_now_ts()

    if isinstance(expiry, datetime.datetime):
        jwt_claims["exp"] = expiry.timestamp()
    elif isinstance(expiry, datetime.timedelta):
        jwt_claims["exp"] = (now + expiry).timestamp()
    elif isinstance(expiry, (float, int)):
        jwt_claims["exp"] = expiry

    if audience:
        jwt_claims["aud"] = audience
    if issuer:
        jwt_claims["iss"] = issuer

    if isinstance(not_before, datetime.datetime):
        jwt_claims["nbf"] = not_before.timestamp()
    elif isinstance(not_before, datetime.timedelta):
        jwt_claims["nbf"] = (now + not_before).timestamp()
    elif isinstance(not_before, (int, float)):
        jwt_claims["nbf"] = not_before

    payload = {**additional_claims, **jwt_claims}

    return jwt.encode(payload=payload, key=key, algorithm=algorithm, headers=headers)


def decode_token(
    token: str,
    key: str,
    algorithms: Iterable[AlgorithmType] = ["HS256"],
    audience: Optional[StrOrIter] = None,
    issuer: Optional[str] = None,
    verify: bool = True,
) -> Dict[str, Any]:
    try:
        return jwt.decode(
            jwt=token,
            key=key,
            algorithms=algorithms,
            audience=audience,
            issuer=issuer,
            options={"verify_signature": verify},
        )
    except Exception as e:
        raise JWTDecodeError(*e.args)
