"""FastJWT Type Hints

        ## Numeric
            Union[float, int]
        Encapsulate numeric values.
        ## ObjOrSeq
            Union[T, Sequence[T]]
        Generic for instance or sequence of instance.
        ## StrOrSeq
            ObjOrSeq[str]
        String or sequence of string.
        ## DateTimeExpression
            Union[datetime.datetime, datetime.timedelta]
        Test.
        ## SymmetricAlgorithmType
            str
        Symmetric algorithm name.
        ## AsymmetricAlgorithmType
            str
        Asymmetric algorithm name.
        ## AlgorithmType
            Union[SymmetricAlgorithmType, AsymmetricAlgorithmType]
        Algorithm name.
        ## HTTPMethod
            Literal["GET", "HEAD", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
        HTTP Methods.
        ## HTTPMethods
            Sequence[HTTPMethod]
        Sequence of HTTP methods.
        ## SameSitePolicy
            Literal["None", "Lax", "Strict"]
        Cookie SameSite Policy.
        ## TokenType
            Literal["access", "refresh"]
        Type of token.
        ## TokenLocation
            Literal["headers", "cookies", "json", "query"]
        Location of token in request.
        ## TokenLocations
            Sequence[TokenLocation]
        List of TokenLocation.
        ## TokenCallback
            Callable[[str, ParamSpecKwargs], bool]
        Callback type for User Serialization.
        ## ModelCallback
            Callable[[str, ParamSpecKwargs], Optional[T]]
        Callback type for Revoked Token validation.

"""
import datetime
from typing import Union
from typing import Literal
from typing import TypeVar
from typing import Callable
from typing import Optional
from typing import Sequence

try:
    from typing import ParamSpecKwargs
except Exception:
    from typing_extensions import ParamSpecKwargs

# Helper types
T = TypeVar("T")
Numeric = Union[float, int]
ObjOrSeq = Union[T, Sequence[T]]
StrOrSeq = ObjOrSeq[str]


# Datetime
DateTimeExpression = Union[datetime.datetime, datetime.timedelta]

# Algorithm
SymmetricAlgorithmType = Literal[
    "HS256",
    "HS384",
    "HS512",
]
AsymmetricAlgorithmType = Literal[
    "ES256",
    "ES256K",
    "ES384",
    "ES512",
    "RS256",
    "RS384",
    "RS512",
    "PS256",
    "PS384",
    "PS512",
]
AlgorithmType = Union[SymmetricAlgorithmType, AsymmetricAlgorithmType]

# Literal Enums
HTTPMethod = Literal["GET", "HEAD", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
HTTPMethods = Sequence[HTTPMethod]
SameSitePolicy = Literal["None", "Lax", "Strict"]
TokenType = Literal["access", "refresh"]
TokenLocation = Literal["headers", "cookies", "json", "query"]
TokenLocations = Sequence[TokenLocation]

# Callbacks
TokenCallback = Callable[[str, ParamSpecKwargs], bool]
ModelCallback = Callable[[str, ParamSpecKwargs], Optional[T]]
