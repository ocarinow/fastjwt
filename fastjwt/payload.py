import datetime
from typing import Any
from typing import List
from typing import Union
from typing import Optional

from pydantic import BaseModel


class JWTPayload(BaseModel):
    uid: str
    iat: Union[int, float]
    permissions: Optional[List[str]]
    exp: Optional[Union[int, float]]
    fresh: bool

    @property
    def issued_date(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.iat, tz=datetime.timezone.utc)

    def has_permission(self, *permissions) -> bool:
        if self.permissions is None:
            return False
        return all([p in self.permissions for p in permissions])
