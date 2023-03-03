import datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastjwt import FastJWT
from fastjwt import JWTPayload
from fastjwt import FastJWTConfig


@pytest.fixture(scope="function")
def symmetric_config():
    config = FastJWTConfig()
    config.JWT_ALGORITHM = "HS256"
    config.JWT_SECRET_KEY = "QmFzZTY0IEVuY29kZWQgU3RyaW5n"
    config.JWT_EXPIRE_DELTATIME = datetime.timedelta(minutes=30)
    config.JWT_REFRESH_DELTATIME = datetime.timedelta(minutes=10)
    return config


@pytest.fixture(scope="function")
def security(symmetric_config: FastJWTConfig):
    security = FastJWT(config=symmetric_config)
    return security


@pytest.fixture(scope="function")
def app(security: FastJWT[JWTPayload, dict]):
    app = FastAPI()

    @app.get("/")
    async def home():
        return "OK"

    return app


@pytest.fixture(scope="function")
def client(app: FastAPI):
    client = TestClient(app)
    return client


def test_fastjwt_symmetric_config(symmetric_config: FastJWTConfig):
    assert (
        symmetric_config._JWT_PRIVATE_KEY == symmetric_config._JWT_PUBLIC_KEY
    ), "Mismatch in Private/Public Keys with symmetric encryption"
    assert (
        symmetric_config._JWT_PUBLIC_KEY == "Base64 Encoded String"
    ), "Mismatch on decoding b64 string"
    assert isinstance(
        symmetric_config._JWT_LOCATIONS, list
    ), "_JWT_LOCATIONS is not a list"
    assert (
        len(symmetric_config._JWT_LOCATIONS) == 4
    ), "_JWT_LOCATIONS is not ['headers','cookies','query','json']"


def test_set_token_checker(security: FastJWT):
    token_checker = lambda string: False
    assert (
        security.token_blacklist_checker is None
    ), "Token blacklist callback is already set"
    security.set_token_checker(token_checker)
    assert (
        security.token_blacklist_checker == token_checker
    ), "Token blacklist callback is not expected function"
    assert id(security.token_blacklist_checker) == id(
        token_checker
    ), "Token blacklist callback is not expected function"


def test_set_user_getter(security: FastJWT):
    user_getter = lambda string: {"name": "User"}
    assert security.user_getter is None, "User callback is already set"
    security.set_user_getter(user_getter)
    assert security.user_getter == user_getter, "User callback is not expected function"
    assert id(security.user_getter) == id(
        user_getter
    ), "User callback is not expected function"


def test_encode_jwt(security: FastJWT):
    ENCODED = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmb28iOiJiYXIifQ.mKeXAm2xUfIffm7p1uGiYT85Rd4deJ8zHG0omKNC5RA"
    DECODED = {"foo": "bar"}

    assert security.encode_jwt(DECODED) == ENCODED, "Encoding JWT does not work"


def test_decode_jwt(security: FastJWT):
    ENCODED = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmb28iOiJiYXIifQ.mKeXAm2xUfIffm7p1uGiYT85Rd4deJ8zHG0omKNC5RA"
    DECODED = {"foo": "bar"}

    assert security.decode_jwt(ENCODED) == DECODED, "Decoding JWT does not work"


@pytest.mark.parametrize(
    "payload, expected",
    [
        (
            JWTPayload(
                uid="",
                fresh=False,
                exp=None,
                iat=int(
                    datetime.datetime(
                        2000,
                        1,
                        1,
                        1,
                        1,
                        tzinfo=datetime.timezone.utc,
                    ).timestamp()
                ),
            ),
            True,
        ),
        (
            JWTPayload(
                uid="iat2000-exp2200",
                fresh=False,
                exp=int(
                    datetime.datetime(
                        2200,
                        1,
                        1,
                        1,
                        1,
                        tzinfo=datetime.timezone.utc,
                    ).timestamp()
                ),
                iat=int(
                    datetime.datetime(
                        2000,
                        1,
                        1,
                        1,
                        1,
                        tzinfo=datetime.timezone.utc,
                    ).timestamp()
                ),
            ),
            False,
        ),
    ],
)
def test_is_payload_expired(security: FastJWT, payload: JWTPayload, expected: bool):
    assert (
        security.is_payload_expired(payload) == expected
    ), f"Payload {payload.uid} does not return the expected expiry response"


@pytest.mark.parametrize(
    "payload, expected",
    [
        (
            JWTPayload(
                uid="",
                fresh=False,
                exp=None,
                iat=int(
                    datetime.datetime(
                        2000,
                        1,
                        1,
                        1,
                        1,
                        tzinfo=datetime.timezone.utc,
                    ).timestamp()
                ),
            ),
            False,
        ),
        (
            JWTPayload(
                uid="iat2000-exp2200",
                fresh=False,
                exp=int(
                    datetime.datetime(
                        2200,
                        1,
                        1,
                        1,
                        1,
                        tzinfo=datetime.timezone.utc,
                    ).timestamp()
                ),
                iat=int(
                    datetime.datetime(
                        2000,
                        1,
                        1,
                        1,
                        1,
                        tzinfo=datetime.timezone.utc,
                    ).timestamp()
                ),
            ),
            True,
        ),
    ],
)
def test_verify_expiry(security: FastJWT, payload: JWTPayload, expected: bool):
    assert (
        security.verify_expiry(payload) == expected
    ), f"Payload {payload.uid} does not return the expected expiry response"


def test_create_access_token(security: FastJWT):
    kwargs = dict(uid="userId", fresh=True, permissions=["read", "write"])
    token = security.create_access_token(**kwargs)
    payload = JWTPayload.parse_obj(security.decode_jwt(token))
    assert hasattr(payload, "uid"), "Payload is missing 'uid' attribute"
    assert hasattr(payload, "iat"), "Payload is missing 'iat' attribute"
    assert hasattr(payload, "permissions"), "Payload is missing 'permissions' attribute"
    assert hasattr(payload, "exp"), "Payload is missing 'exp' attribute"
    assert hasattr(payload, "fresh"), "Payload is missing 'fresh' attribute"

    assert datetime.datetime.fromtimestamp(
        payload.iat, tz=datetime.timezone.utc
    ) + security.config.JWT_EXPIRE_DELTATIME == datetime.datetime.fromtimestamp(
        payload.exp, tz=datetime.timezone.utc
    ), "Expiry date is wrong"


def test_create_access_token_with_expiry(security: FastJWT):
    delta = datetime.timedelta(days=1)
    kwargs = dict(uid="userId", fresh=True, permissions=["read", "write"])
    token = security.create_access_token(expires_delta=delta, **kwargs)
    payload = JWTPayload.parse_obj(security.decode_jwt(token))

    assert datetime.datetime.fromtimestamp(
        payload.iat, tz=datetime.timezone.utc
    ) + delta == datetime.datetime.fromtimestamp(
        payload.exp, tz=datetime.timezone.utc
    ), "Expiry date is wrong"


def test_create_access_token_without_expiry(security: FastJWT):
    security._config.JWT_EXPIRE_DELTATIME = None
    kwargs = dict(uid="userId", fresh=True, permissions=["read", "write"])
    token = security.create_access_token(**kwargs)
    payload = JWTPayload.parse_obj(security.decode_jwt(token))
    assert payload.exp is None, "Expiry date is wrong"
    security._config.JWT_EXPIRE_DELTATIME = datetime.timedelta(minutes=30)


def test_refresh_token_implicit(security: FastJWT):
    delta = security._config.JWT_REFRESH_DELTATIME - datetime.timedelta(minutes=1)
    kwargs = dict(uid="userId", fresh=True, permissions=["read", "write"], foo="bar")
    token = security.create_access_token(expires_delta=delta, **kwargs)
    access_payload = JWTPayload.parse_obj(security.decode_jwt(token))
    new_token = security.refresh_token(token)
    assert new_token is not None, "Token was not refreshed"
    new_payload = JWTPayload.parse_obj(security.decode_jwt(new_token))

    assert access_payload.iat <= new_payload.iat, "Issue date has decreased"
    assert access_payload.exp <= new_payload.exp, "Expiry date has decreased"
    assert (
        access_payload.extra == new_payload.extra
    ), "Extra parameters were not conserved"


def test_verify_token(security: FastJWT):
    kwargs = dict(uid="userId", fresh=True, permissions=["read", "write"])
    token = security.create_access_token(**kwargs)
    assert security.verify_token(token), "Token is not Valid"
    assert security.verify_token(token, require_fresh=True), "Token is not Fresh"


def test_verify_unfresh_token(security: FastJWT):
    kwargs = dict(uid="userId", fresh=False, permissions=["read", "write"])
    token = security.create_access_token(**kwargs)

    assert security.verify_token(token, require_fresh=True) is False, "Token is Fresh"


def test_verify_expired_token(security: FastJWT):
    kwargs = dict(uid="userId", fresh=True, permissions=["read", "write"])
    token = security.create_access_token(
        expires_delta=datetime.timedelta(minutes=-1), **kwargs
    )
    assert security.verify_token(token) is False, "Token is valid"


def test_verify_blacklisted_token(security: FastJWT):
    security.set_token_checker(lambda x: True)
    kwargs = dict(uid="userId", fresh=True, permissions=["read", "write"])
    token = security.create_access_token(**kwargs)

    assert security.verify_token(token) is False, "Token is valid"
    security.set_token_checker(None)
