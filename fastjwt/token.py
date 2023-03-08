import datetime
from typing import Any
from typing import Dict
from typing import Union
from typing import Optional
from typing import Sequence

import jwt

from .types import StrOrSeq
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
    audience: Optional[StrOrSeq] = None,
    issuer: Optional[str] = None,
    additional_data: Optional[Dict[str, Any]] = None,
    not_before: Optional[Union[int, DateTimeExpression]] = None,
    ignore_errors: bool = True,
) -> str:
    """Encode a token

    Args:
        uid (str): The unique identifier to generate a token for
        key (str): secret key for token encoding
        type (TokenType): Token type
        jti (Optional[str], optional): JWT unique identifier. Defaults to None.
        expiry (Optional[DateTimeExpression], optional): Expiration time claim. Defaults to None.
        issued (Optional[DateTimeExpression], optional): Issued at claim. Defaults to None.
        fresh (bool, optional): Token freshness. Defaults to False.
        csrf (Union[str, bool], optional): CSRF Token. Defaults to True.
        algorithm (AlgorithmType, optional): Algorithm to use to encode token. Defaults to "HS256".
        headers (Optional[Dict[str, Any]], optional): TODO. Defaults to None.
        audience (Optional[StrOrSeq], optional): Audience claim. Defaults to None.
        issuer (Optional[str], optional): Issuer claim. Defaults to None.
        additional_data (Optional[Dict[str, Any]], optional): Custom claims. Defaults to None.
        not_before (Optional[Union[int, DateTimeExpression]], optional): Not before claim. Defaults to None.
        ignore_errors (bool, optional): Ignore errors from custom claims validation. Defaults to True.

    Raises:
        ValueError: Some custom claim tries to override standard JWT claims

    Returns:
        str: encoded token
    """
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
    algorithms: Sequence[AlgorithmType] = ["HS256"],
    audience: Optional[StrOrSeq] = None,
    issuer: Optional[str] = None,
    verify: bool = True,
) -> Dict[str, Any]:
    """Decode a token

    Args:
        token (str): Token to decode
        key (str): secret key for token decoding
        algorithms (Sequence[AlgorithmType], optional): Algorithms to use for decoding. Defaults to ["HS256"].
        audience (Optional[StrOrSeq], optional): Audiences to verify. Defaults to None.
        issuer (Optional[str], optional): Issuer to verify. Defaults to None.
        verify (bool, optional): Enable validation. Defaults to True.

    Raises:
        JWTDecodeError: The token decoding was not possible.
            Mostly due to verification error.
            Expiration
            Audience/Issuer not verified
            ...

    Returns:
        Dict[str, Any]: The decoded token
    """
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
