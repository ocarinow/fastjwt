import datetime
from typing import Union
from typing import Literal
from typing import TypeVar
from typing import Sequence

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
