import json

import pytest
from fastapi import Request

from fastjwt import FastJWTConfig
from fastjwt.errors import NoAuthorizationError
from fastjwt.utils._getters import _get_token_in_json
from fastjwt.utils._getters import _get_token_in_query
from fastjwt.utils._getters import _get_token_in_header
from fastjwt.utils._getters import _get_token_in_cookies
from fastjwt.utils._getters import get_token_from_request


@pytest.fixture(scope="function")
def config():
    config = FastJWTConfig()
    config.JWT_ALGORITHM = "HS256"
    config.JWT_SECRET_KEY = "QmFzZTY0IEVuY29kZWQgU3RyaW5n"
    return config


@pytest.fixture(scope="function")
def headers(config: FastJWTConfig):
    return [
        [
            f"{config.JWT_HEADER_NAME.lower()}".encode(),
            f"{config.JWT_HEADER_TYPE} TOKEN".encode(),
        ]
    ]


@pytest.fixture(scope="function")
def cookies(config: FastJWTConfig):
    return [
        [b"content-type", b"application/json"],
        [b"cookie", f"{config.JWT_COOKIE_NAME}=TOKEN;".encode()],
    ]


@pytest.fixture(scope="function")
def query(config: FastJWTConfig):
    return {f"{config.JWT_QUERY_STRING_NAME}": "TOKEN"}


@pytest.fixture(scope="function")
def body(config: FastJWTConfig):
    async def receiver():
        return {
            "type": "http.request",
            "body": json.dumps(
                {
                    config.JWT_JSON_ACCESS_KEY: "TOKEN",
                    config.JWT_JSON_REFRESH_KEY: "REFRESH_TOKEN",
                }
            ).encode(),
        }

    return receiver


@pytest.fixture(scope="function")
def req(headers, cookies, query, body):
    req = Request(
        scope={
            "type": "http",
            "method": "POST",
            "headers": [*headers, *cookies],
            "query_string": query,
        },
        receive=body,
    )
    return req


@pytest.fixture(scope="function")
def req_null():
    async def receiver():
        return {
            "type": "http.request",
            "body": json.dumps({}).encode(),
        }

    req = Request(
        scope={
            "type": "http",
            "method": "POST",
            "headers": [[b"content-type", b"application/json"], [b"cookie", b""]],
            "query_string": {},
        },
        receive=receiver,
    )
    return req


@pytest.fixture(scope="function")
def req_error():
    async def receiver():
        return {
            "type": "http.request",
            "body": json.dumps({}).encode(),
        }

    req = Request(
        scope={
            "type": "http",
            "method": "POST",
            "headers": [[b"content-type", b"application/json"], [b"cookie", b""]],
            "query_string": {},
        },
    )
    return req


@pytest.fixture(scope="function")
def req_header(headers):
    req = Request(
        scope={
            "type": "http",
            "headers": headers,
        },
    )
    return req


@pytest.fixture(scope="function")
def req_cookie(cookies):
    req = Request(
        scope={
            "type": "http",
            "headers": cookies,
        },
    )
    return req


@pytest.fixture(scope="function")
def req_body(body):
    req = Request(
        scope={
            "type": "http",
            "method": "POST",
            "headers": [
                [b"content-type", b"application/json"],
            ],
        },
        receive=body,
    )
    return req


@pytest.fixture(scope="function")
def req_query(query):
    req = Request(
        scope={
            "type": "http",
            "query_string": query,
        },
    )
    return req


@pytest.mark.asyncio
async def test_get_token_from_cookie(config: FastJWTConfig, req_cookie: Request):
    request_token = await _get_token_in_cookies(request=req_cookie, config=config)
    assert request_token is not None
    assert request_token.location == "cookies"
    assert request_token.access_token == "TOKEN"


@pytest.mark.asyncio
async def test_get_token_from_query(config: FastJWTConfig, req_query: Request):
    request_token = await _get_token_in_query(request=req_query, config=config)
    assert request_token is not None
    assert request_token.location == "query"
    assert request_token.access_token == "TOKEN"


@pytest.mark.asyncio
async def test_get_token_from_json(config: FastJWTConfig, req_body: Request):
    request_token = await _get_token_in_json(request=req_body, config=config)
    assert request_token is not None
    assert request_token.location == "json"
    assert request_token.access_token == "TOKEN"


@pytest.mark.asyncio
async def test_get_token_from_headers(config: FastJWTConfig, req_header: Request):
    request_token = await _get_token_in_header(request=req_header, config=config)
    assert request_token is not None
    assert request_token.location == "headers"
    assert request_token.access_token == "TOKEN"


@pytest.mark.parametrize("location", ["headers", "query", "cookies", "json"])
@pytest.mark.asyncio
async def test_get_token(config: FastJWTConfig, req: Request, location: str):
    request_token = await get_token_from_request(
        request=req, config=config, locations=[location]
    )
    assert request_token is not None
    assert request_token.location == location
    assert request_token.access_token == "TOKEN"


@pytest.mark.asyncio
async def test_raise_error_on_get_token(config: FastJWTConfig, req_null: Request):
    assert await get_token_from_request(request=req_null, config=config) is None
    assert (
        await get_token_from_request(request=req_null, config=config, locations=[])
        is None
    )


@pytest.mark.asyncio
async def test_raise_error_on_get_token(
    config: FastJWTConfig, req_null: Request, req_error: Request
):
    with pytest.raises(NoAuthorizationError):
        await _get_token_in_header(request=req_null, config=config)
    with pytest.raises(NoAuthorizationError):
        await _get_token_in_query(request=req_null, config=config)
    with pytest.raises(NoAuthorizationError):
        await _get_token_in_json(request=req_null, config=config)
    with pytest.raises(NoAuthorizationError):
        await _get_token_in_cookies(request=req_null, config=config)
    with pytest.raises(NoAuthorizationError):
        await _get_token_in_json(request=req_error, config=config)
