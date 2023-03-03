import datetime

import pytest

from fastjwt import JWTPayload


@pytest.fixture(scope="function")
def iat():
    return datetime.datetime(2023, 1, 1, 12, 0, tzinfo=datetime.timezone.utc)


@pytest.fixture(scope="function")
def payload_permission(iat: datetime.datetime):
    return JWTPayload(
        uid="userId",
        iat=int(iat.timestamp()),
        fresh=True,
        permissions=["read", "write"],
        foo="bar",
    )


@pytest.fixture(scope="function")
def payload_nopermission(iat: datetime.datetime):
    return JWTPayload(
        uid="userId",
        iat=int(iat.timestamp()),
        fresh=True,
        permissions=None,
    )


def test_payload_extra(payload_permission: JWTPayload):
    assert payload_permission.extra == {"foo": "bar"}
    assert JWTPayload.parse_obj(payload_permission.dict()).extra == {"foo": "bar"}


def test_payload_has_privilege(payload_permission: JWTPayload):
    assert payload_permission.has_permission("read") is True
    assert payload_permission.has_permission("read", "write") is True
    assert payload_permission.has_permission("admin") is False
    assert payload_permission.has_permission("admin", "write") is False


def test_payload_has_no_privilege(payload_nopermission: JWTPayload):
    assert payload_nopermission.has_permission("read") is False
    assert payload_nopermission.has_permission("read", "write") is False
    assert payload_nopermission.has_permission("admin") is False
    assert payload_nopermission.has_permission("admin", "write") is False
