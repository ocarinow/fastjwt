import uuid
import datetime

from .types import Numeric


def get_now() -> datetime.datetime:
    """Returns the current UTC datetime

    Returns:
        datetime.datetime: Current datetime (UTC)
    """
    return datetime.datetime.now(tz=datetime.timezone.utc)


def get_now_ts() -> Numeric:
    """Returns the current UTC datetime as timestamp (float)

    Returns:
        Numeric: Current datetime (UTC)
    """
    return get_now().timestamp()


def get_uuid() -> str:
    """Generates a Universe Unique Identifier v4

    Returns:
        str: unique identifier
    """
    return str(uuid.uuid4())
