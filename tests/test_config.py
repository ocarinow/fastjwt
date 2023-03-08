import pytest

from fastjwt.config import FJWTConfig
from fastjwt.exceptions import BadConfigurationError


# region Fixtures
@pytest.fixture(scope="function")
def config() -> FJWTConfig:
    config = FJWTConfig()
    config.JWT_ALGORITHM = "HS256"
    config.JWT_SECRET_KEY = "QmFzZTY0IEVuY29kZWQgU3RyaW5n"
    config.JWT_TOKEN_LOCATION = ["headers", "cookies", "json", "query"]
    config.JWT_CSRF_METHODS = ["POST", "DELETE", "PUT"]
    config.JWT_REFRESH_CSRF_HEADER_NAME = "X-REFRESH-CSRF-TOKEN"
    return config


# endregion


def test_bad_algorithm_config_exception():
    config = FJWTConfig()
    config.JWT_ALGORITHM = "BAD_ALGO"
    config.JWT_SECRET_KEY = "QmFzZTY0IEVuY29kZWQgU3RyaW5n"

    with pytest.raises(BadConfigurationError):
        config.PRIVATE_KEY


def test_none_secret_config_exception():
    config = FJWTConfig()
    config.JWT_ALGORITHM = "HS256"
    config.JWT_SECRET_KEY = None

    with pytest.raises(BadConfigurationError):
        config.PRIVATE_KEY


def test_config_symmetric_key():
    config = FJWTConfig()
    config.JWT_ALGORITHM = "HS256"
    config.JWT_SECRET_KEY = "SYMMETRIC_KEY"
    config.JWT_PUBLIC_KEY = "ASYMMETRIC_PUBLIC_KEY"
    config.JWT_PRIVATE_KEY = "ASYMMETRIC_PRIVATE_KEY"

    assert config.PRIVATE_KEY == config.JWT_SECRET_KEY
    assert config.PUBLIC_KEY == config.JWT_SECRET_KEY


def test_config_asymmetric_key():
    config = FJWTConfig()
    config.JWT_ALGORITHM = "RS256"
    config.JWT_SECRET_KEY = "SYMMETRIC_KEY"
    config.JWT_PUBLIC_KEY = "ASYMMETRIC_PUBLIC_KEY"
    config.JWT_PRIVATE_KEY = "ASYMMETRIC_PRIVATE_KEY"

    assert config.PRIVATE_KEY == config.JWT_PRIVATE_KEY
    assert config.PUBLIC_KEY == config.JWT_PUBLIC_KEY


def test_config_has_location():
    config = FJWTConfig()

    print(config.JWT_TOKEN_LOCATION)

    assert config.has_location("headers")
    assert config.has_location("headers")
    assert config.has_location("cookies") is False


def test_config__get_key():
    config = FJWTConfig()
    config.JWT_SECRET_KEY = "SECRET"
    config.JWT_ALGORITHM = "RS256"

    assert config._get_key("TEST") == "TEST"

    config.JWT_ALGORITHM = "HS256"
    assert config._get_key("TEST") == "SECRET"
