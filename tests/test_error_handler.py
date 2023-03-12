import json

import pytest
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

import fastjwt.exceptions as exc
from fastjwt.fastjwt import FastJWT


@pytest.fixture(scope="function")
def fjwt():
    fjwt = FastJWT()
    return fjwt


@pytest.fixture(scope="function")
def app():
    app = FastAPI()
    return app


@pytest.mark.asyncio
async def test__error_handler(fjwt: FastJWT):
    error_handler = fjwt._error_handler(
        ValueError, status_code=100, message="Sample Message"
    )
    try:
        raise ValueError("Execution Message")
    except ValueError as e:
        req = Request(scope={"type": "http", "method": "GET"})
        resp = await error_handler(req, e)

    assert isinstance(resp, JSONResponse)
    assert resp.status_code == 100
    assert json.loads(resp.body.decode()) == {
        "message": "Sample Message",
        "error_type": ValueError.__name__,
    }


@pytest.mark.asyncio
async def test__error_handler_without_message(fjwt: FastJWT):
    error_handler = fjwt._error_handler(ValueError, status_code=100, message=None)
    try:
        raise ValueError("Execution Message")
    except ValueError as e:
        req = Request(scope={"type": "http", "method": "GET"})
        resp = await error_handler(req, e)

    assert isinstance(resp, JSONResponse)
    assert resp.status_code == 100
    assert json.loads(resp.body.decode()) == {
        "message": "Execution Message",
        "error_type": ValueError.__name__,
    }


def test_handle_app_errors(app: FastAPI, fjwt: FastJWT):
    fjwt.handle_errors(app)

    assert exc.JWTDecodeError in app.exception_handlers
    assert exc.MissingTokenError in app.exception_handlers
    assert exc.MissingCSRFTokenError in app.exception_handlers
    assert exc.TokenTypeError in app.exception_handlers
    assert exc.RevokedTokenError in app.exception_handlers
    assert exc.TokenRequiredError in app.exception_handlers
    assert exc.FreshTokenRequiredError in app.exception_handlers
    assert exc.AccessTokenRequiredError in app.exception_handlers
    assert exc.RefreshTokenRequiredError in app.exception_handlers
    assert exc.CSRFError in app.exception_handlers
