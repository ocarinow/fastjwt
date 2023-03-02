from typing import Any
from typing import Dict
from typing import Union
from typing import Optional

from fastjwt.settings import FastJWTConfig
from fastjwt.settings import FastJWTConfigDict

FastJWTConfigType = Union[FastJWTConfigDict, FastJWTConfig, Dict[str, Any]]


def parse_config(config: Optional[FastJWTConfigType] = None, **kwargs) -> FastJWTConfig:
    if isinstance(config, dict):
        return FastJWTConfig.parse_obj({**config, **kwargs})
    elif isinstance(config, FastJWTConfig):
        return config
    else:
        return FastJWTConfig()
