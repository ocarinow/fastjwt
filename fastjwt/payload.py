import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Union
from typing import Optional

from pydantic import BaseModel
from pydantic import root_validator


class JWTPayload(BaseModel):
    uid: str
    iat: Union[int, float]
    permissions: Optional[List[str]] = None
    exp: Optional[Union[int, float]] = None
    fresh: bool
    extra: Dict[str, Any]

    @root_validator(pre=True)
    def build_extra(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        all_required_field_names = {
            field.alias for field in cls.__fields__.values() if field.alias != "extra"
        }  # to support alias

        extra: Dict[str, Any] = {}
        for field_name in list(values):
            if field_name not in all_required_field_names:
                if field_name == "extra":
                    extra_value = values.pop(field_name)
                    if isinstance(extra_value, dict):
                        for key, val in extra_value.items():
                            extra[key] = val
                else:
                    extra[field_name] = values.pop(field_name)
        values["extra"] = extra
        return values

    @property
    def issued_date(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.iat, tz=datetime.timezone.utc)

    def has_permission(self, *permissions) -> bool:
        if self.permissions is None:
            return False
        return all([p in self.permissions for p in permissions])
