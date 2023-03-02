from typing import List
from typing import Literal
from typing import Optional

from pydantic import BaseModel

AlgorithmType = Literal["RS256", "HS256"]
SamesiteType = Literal["lax", "strict", "none"]
TokenLocation = Literal["json", "headers", "cookies", "query"]
TokenLocations = List[TokenLocation]


class RequestToken(BaseModel):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    csrf_token: Optional[str] = None
    location: TokenLocation
