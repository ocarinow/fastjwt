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


def test_is_model_callback_set(fjwt: FastJWT):
    def fake_model_handler(uid: str):
        return {"foo": "bar"}

    assert fjwt._check_model_callback_is_set(ignore_errors=True) is False
    with pytest.raises(AttributeError):
        fjwt._check_model_callback_is_set(ignore_errors=False)

    assert fjwt.is_model_callback_set is False
    fjwt.set_callback_get_model_instance(fake_model_handler)
    assert fjwt.is_model_callback_set is True
    assert fjwt._check_model_callback_is_set(ignore_errors=True) is True


def test_is_token_callback_set(fjwt: FastJWT):
    def fake_token_handler(token: str):
        return True

    assert fjwt._check_token_callback_is_set(ignore_errors=True) is False
    with pytest.raises(AttributeError):
        fjwt._check_token_callback_is_set(ignore_errors=False)

    assert fjwt.is_token_callback_set is False
    fjwt.set_callback_token_blocklist(fake_token_handler)
    assert fjwt.is_token_callback_set is True
    assert fjwt._check_token_callback_is_set(ignore_errors=True) is True


def test_is_token_in_blocklist(fjwt: FastJWT):
    @fjwt.set_callback_token_blocklist
    def fake_token_handler(token: str):
        return token.startswith("A")

    assert fjwt.is_token_callback_set is True

    assert fjwt.is_token_in_blocklist("Atchoum") is True
    assert fjwt.is_token_in_blocklist("Tchoum") is False


def test_get_current_subject(fjwt: FastJWT):
    DB = {
        "a": {"username": "a"},
    }

    @fjwt.set_callback_get_model_instance
    def fake_model_handler(uid: str):
        return DB.get(uid)

    assert fjwt.is_model_callback_set is True

    assert fjwt._get_current_subject("a") == {"username": "a"}
    assert fjwt._get_current_subject("Tchoum") is None
