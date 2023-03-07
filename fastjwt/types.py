import datetime
from typing import Union
from typing import Generic
from typing import Literal
from typing import TypeVar
from typing import Callable
from typing import Iterable
from typing import Optional
from typing import Awaitable
from typing import ParamSpecKwargs

# Helper types
T = TypeVar("T")
Numeric = Union[float, int]
ObjOrIter = Union[T, Iterable[T]]
StrOrIter = ObjOrIter[str]


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
HTTPMethods = Iterable[HTTPMethod]
SameSitePolicy = Literal["None", "Lax", "Strict"]
TokenType = Literal["access", "refresh"]
TokenLocation = Literal["headers", "cookies", "json", "query"]
TokenLocations = Iterable[TokenLocation]
