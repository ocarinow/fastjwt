import datetime

import pytest
from fastapi import Response

from fastjwt import FastJWT
from fastjwt import FastJWTConfig
from fastjwt.utils.cookies import set_access_cookie
from fastjwt.utils.cookies import unset_access_cookie


@pytest.fixture(scope="function")
def config():
    config = FastJWTConfig()
    config.JWT_ALGORITHM = "HS256"
    config.JWT_SECRET_KEY = "QmFzZTY0IEVuY29kZWQgU3RyaW5n"
    return config


@pytest.fixture(scope="function")
def nocookie_config():
    config = FastJWTConfig()
    config.JWT_LOCATIONS = ["headers"]
    config.JWT_ALGORITHM = "HS256"
    config.JWT_SECRET_KEY = "QmFzZTY0IEVuY29kZWQgU3RyaW5n"
    return config


@pytest.fixture(scope="function")
def security(config: FastJWTConfig):
    security = FastJWT(config=config)
    return security


def test_set_access_cookie(config: FastJWTConfig):
    resp = Response()
    assert len(resp.headers.getlist("set-cookie")) == 0, "Cookies are already set"
    set_access_cookie(response=resp, token="TOKEN", config=config)
    assert len(resp.headers.getlist("set-cookie")) == 1, "Cookies are not set"
    assert f"{config.JWT_COOKIE_NAME}=TOKEN" in resp.headers.getlist("set-cookie")[0]


def test_set_access_cookie_for_nocookies(nocookie_config: FastJWTConfig):
    resp = Response()
    assert len(resp.headers.getlist("set-cookie")) == 0, "Cookies are set"
    set_access_cookie(response=resp, token="TOKEN", config=nocookie_config)
    assert len(resp.headers.getlist("set-cookie")) == 0, "Cookies are set"


def test_unset_access_cookie(config: FastJWTConfig):
    resp = Response()
    assert len(resp.headers.getlist("set-cookie")) == 0, "Cookies are already set"
    set_access_cookie(response=resp, token="TOKEN", config=config)
    assert len(resp.headers.getlist("set-cookie")) == 1, "Cookies are not set"
    assert f"{config.JWT_COOKIE_NAME}=TOKEN;" in resp.headers.getlist("set-cookie")[0]
    unset_access_cookie(response=resp, config=config)
    assert len(resp.headers.getlist("set-cookie")) == 2, "Cookies are not set"
    assert f'{config.JWT_COOKIE_NAME}="";' in resp.headers.getlist("set-cookie")[1]
