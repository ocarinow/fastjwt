import datetime

import pytest
from fastapi import Request
from fastapi.responses import JSONResponse

from fastjwt.models import RequestToken
from fastjwt.models import TokenPayload
from fastjwt.fastjwt import FastJWT
from fastjwt.exceptions import MissingTokenError


@pytest.fixture(scope="function")
def fjwt():
    fjwt = FastJWT()
    fjwt._config.JWT_SECRET_KEY = "SECRET"
    fjwt._config.JWT_TOKEN_LOCATION = ["headers", "json", "cookies"]
    return fjwt


@pytest.fixture(scope="function")
def access_token(fjwt: FastJWT):
    return fjwt.create_access_token(uid="hello", fresh=True)


@pytest.fixture(scope="function")
def refresh_token(fjwt: FastJWT):
    return fjwt.create_refresh_token(uid="hello")


# region Token


def test_create_access_token(fjwt: FastJWT):
    token = fjwt.create_access_token(uid="ocarinow", fresh=True)
    assert isinstance(token, str)
    payload = fjwt._decode_token(token, verify=False)
    assert payload.fresh
    assert payload.sub == "ocarinow"
    assert payload.type == "access"


def test_create_refresh_token(fjwt: FastJWT):
    token = fjwt.create_refresh_token(uid="ocarinow", fresh=True)
    assert isinstance(token, str)
    payload = fjwt._decode_token(token, verify=False)
    assert payload.fresh is not True
    assert payload.sub == "ocarinow"
    assert payload.type == "refresh"


def test_verify_token(fjwt: FastJWT):
    token = fjwt.create_access_token(uid="ocarinow", fresh=True)
    payload = fjwt._decode_token(token, verify=False)
    request_token = RequestToken(
        token=token, csrf=None, location="headers", type="access"
    )
    payload = fjwt.verify_token(request_token, verify_csrf=False)
    assert payload.fresh
    assert payload.sub == "ocarinow"


# endregion

# region Cookies


def test_set_wrong_token_type_cookie_exception(fjwt: FastJWT):
    response = JSONResponse(content={"foo": "bar"})
    token = fjwt.create_access_token(uid="ocarinow", fresh=True)

    with pytest.raises(ValueError):
        fjwt._set_cookies(token=token, type="bad_type", response=response)


def test_unset_wrong_token_type_cookie_exception(fjwt: FastJWT):
    response = JSONResponse(content={"foo": "bar"})
    token = fjwt.create_access_token(uid="ocarinow", fresh=True)
    fjwt.set_access_cookies(token=token, response=response)

    with pytest.raises(ValueError):
        fjwt._unset_cookies(type="bad_type", response=response)


def test_set_access_cookies(fjwt: FastJWT):
    response = JSONResponse(content={"foo": "bar"})
    token = fjwt.create_access_token(uid="ocarinow", fresh=True)
    fjwt.set_access_cookies(token, response=response)

    assert all(
        [
            cookie.startswith(fjwt.config.JWT_ACCESS_COOKIE_NAME)
            or cookie.startswith(fjwt.config.JWT_ACCESS_CSRF_COOKIE_NAME)
            for cookie in response.headers.getlist("set-cookie")
        ]
    )


def test_set_refresh_cookies(fjwt: FastJWT):
    response = JSONResponse(content={"foo": "bar"})
    token = fjwt.create_refresh_token(uid="ocarinow", fresh=True)
    fjwt.set_refresh_cookies(token, response=response)

    assert all(
        [
            cookie.startswith(fjwt.config.JWT_REFRESH_COOKIE_NAME)
            or cookie.startswith(fjwt.config.JWT_REFRESH_CSRF_COOKIE_NAME)
            for cookie in response.headers.getlist("set-cookie")
        ]
    )


def test_unset_access_cookies(fjwt: FastJWT):
    response = JSONResponse(content={"foo": "bar"})
    fjwt.unset_access_cookies(response=response)

    assert all(
        [
            cookie.startswith(f'{fjwt.config.JWT_ACCESS_COOKIE_NAME}=""')
            or cookie.startswith(f'{fjwt.config.JWT_ACCESS_CSRF_COOKIE_NAME}=""')
            for cookie in response.headers.getlist("set-cookie")
        ]
    )


def test_unset_refresh_cookies(fjwt: FastJWT):
    response = JSONResponse(content={"foo": "bar"})
    fjwt.unset_refresh_cookies(response=response)

    assert all(
        [
            cookie.startswith(f'{fjwt.config.JWT_REFRESH_COOKIE_NAME}=""')
            or cookie.startswith(f'{fjwt.config.JWT_REFRESH_CSRF_COOKIE_NAME}=""')
            for cookie in response.headers.getlist("set-cookie")
        ]
    )


def test_unset_cookies(fjwt: FastJWT):
    response = JSONResponse(content={"foo": "bar"})
    fjwt.unset_cookies(response=response)

    assert all(
        [
            cookie.startswith(f'{fjwt.config.JWT_REFRESH_COOKIE_NAME}=""')
            or cookie.startswith(f'{fjwt.config.JWT_REFRESH_CSRF_COOKIE_NAME}=""')
            or cookie.startswith(f'{fjwt.config.JWT_ACCESS_COOKIE_NAME}=""')
            or cookie.startswith(f'{fjwt.config.JWT_ACCESS_CSRF_COOKIE_NAME}=""')
            for cookie in response.headers.getlist("set-cookie")
        ]
    )


# endregion

# region Request


@pytest.mark.asyncio
async def test_get_token_from_request_without_auth(fjwt: FastJWT):
    req = Request(
        scope={
            "method": "GET",
            "type": "http",
            "headers": [],
        }
    )
    with pytest.raises(MissingTokenError):
        await fjwt._get_token_from_request(
            request=req, refresh=False, locations=["headers"]
        )


@pytest.mark.asyncio
async def test_get_token_from_request_access(fjwt: FastJWT, access_token: str):
    req = Request(
        scope={
            "method": "GET",
            "type": "http",
            "headers": [[b"authorization", f"Bearer {access_token}".encode()]],
        }
    )
    request_token = await fjwt.get_access_token_from_request(request=req)
    assert request_token.token == access_token
    assert request_token.location == "headers"
    assert request_token.csrf is None
    assert request_token.type == "access"


@pytest.mark.asyncio
async def test_get_token_from_request_refresh(fjwt: FastJWT, refresh_token: str):
    req = Request(
        scope={
            "method": "GET",
            "type": "http",
            "headers": [
                [
                    b"cookie",
                    f"{fjwt.config.JWT_REFRESH_COOKIE_NAME}={refresh_token};".encode(),
                ]
            ],
        }
    )
    request_token = await fjwt.get_refresh_token_from_request(request=req)
    assert request_token.token == refresh_token
    assert request_token.location == "cookies"
    assert request_token.csrf is None
    assert request_token.type == "refresh"


# endregion

# region Authentication


@pytest.mark.asyncio
async def test__auth_required(fjwt: FastJWT, refresh_token: str, access_token: str):
    req = Request(
        scope={
            "method": "GET",
            "type": "http",
            "headers": [
                [b"content-type", b"application/json"],
                [b"authorization", f"Bearer {access_token}".encode()],
                [
                    b"cookie",
                    f"{fjwt.config.JWT_REFRESH_COOKIE_NAME}={refresh_token};".encode(),
                ],
            ],
        }
    )

    refresh_token: TokenPayload = await fjwt._auth_required(
        request=req, verify_fresh=False, type="refresh"
    )
    assert refresh_token.type == "refresh"
    access_token: TokenPayload = await fjwt._auth_required(
        request=req, verify_fresh=True, type="access"
    )
    assert access_token.type == "access"


@pytest.mark.asyncio
async def test_token_required(fjwt: FastJWT, access_token: str):
    req = Request(
        scope={
            "method": "GET",
            "type": "http",
            "headers": [
                [b"content-type", b"application/json"],
                [b"authorization", f"Bearer {access_token}".encode()],
                [
                    b"cookie",
                    f"{fjwt.config.JWT_REFRESH_COOKIE_NAME}={refresh_token};".encode(),
                ],
            ],
        }
    )

    dependency = fjwt.token_required()
    access_token: TokenPayload = await dependency(
        request=req, verify_fresh=True, type="access"
    )
    assert access_token.type == "access"


# endregion
