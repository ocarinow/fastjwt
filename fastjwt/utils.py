import uuid
import datetime

from .types import Numeric


def get_now() -> datetime.datetime:
    return datetime.datetime.now(tz=datetime.timezone.utc)


def get_now_ts() -> Numeric:
    return get_now().timestamp()


def get_uuid() -> str:
    return str(uuid.uuid4())
