import pytest
from httpx import Response
from fastapi.testclient import TestClient

import fastjwt.exceptions as exc
from fastjwt import FJWTConfig

from .utils_app import init_app
from .utils_app import create_securities
from .utils_app import create_token_routes
from .utils_app import create_secure_routes
from .utils_app import create_subject_routes
from .utils_app import create_blocklist_routes
from .utils_app import create_get_token_routes
from .utils_app import create_protected_routes

# region Base Fixtures


@pytest.fixture(scope="function")
def config():
    """Fixture for FastJWT Configuration"""

    return FJWTConfig(
        JWT_SECRET_KEY="secret",
        JWT_TOKEN_LOCATION=["headers", "json", "query", "cookies"],
    )


@pytest.fixture(scope="function")
def api(config: FJWTConfig):
    """Fixture for FastAPI TestClient"""

    app, security = init_app(config=config)
    create_protected_routes(app, security)
    create_token_routes(app, security)
    create_blocklist_routes(app, security)
    create_get_token_routes(app, security)
    create_subject_routes(app, security)
    create_secure_routes(app, create_securities(security))
    client = TestClient(app)
    return client


@pytest.fixture(scope="function")
def no_csrf_api():
    """Fixture for FastAPI TestClient with CSRF Protection disabled"""
    app, security = init_app(
        config=FJWTConfig(
            JWT_COOKIE_CSRF_PROTECT=False,
            JWT_SECRET_KEY="secret",
            JWT_TOKEN_LOCATION=["headers", "json", "query", "cookies"],
        )
    )
    create_protected_routes(app, security)
    create_token_routes(app, security)
    create_blocklist_routes(app, security)
    create_get_token_routes(app, security)
    create_subject_routes(app, security)
    create_secure_routes(app, create_securities(security))
    client = TestClient(app)
    return client


# endregion


# region Token Fixtures


@pytest.fixture(scope="function")
def access_response(api: TestClient):
    """Fixture for Access Token Response"""
    return api.get("/token/access")


@pytest.fixture(scope="function")
def access_token(access_response: Response) -> str:
    """Fixture for Access Token"""
    assert access_response.status_code == 200
    return access_response.json()["token"]


@pytest.fixture(scope="function")
def access_csrf_token(access_response: Response, config: FJWTConfig) -> str:
    """Fixture for Access CSRF Token"""
    assert access_response.status_code == 200
    return access_response.cookies.get(config.JWT_ACCESS_CSRF_COOKIE_NAME)


@pytest.fixture(scope="function")
def refresh_response(api: TestClient):
    """Fixture for Refresh Token Response"""
    return api.get("/token/refresh")


@pytest.fixture(scope="function")
def refresh_token(refresh_response: Response) -> str:
    """Fixture for Refresh Token"""
    assert refresh_response.status_code == 200
    return refresh_response.json()["token"]


@pytest.fixture(scope="function")
def refresh_csrf_token(refresh_response: Response, config: FJWTConfig) -> str:
    """Fixture for Refresh CSRF Token"""
    assert refresh_response.status_code == 200
    return refresh_response.cookies.get(config.JWT_REFRESH_CSRF_COOKIE_NAME)


@pytest.fixture(scope="function")
def fresh_response(api: TestClient) -> Response:
    """Fixture for Fresh Token Response"""
    return api.get("/token/fresh")


@pytest.fixture(scope="function")
def fresh_token(fresh_response: Response) -> str:
    """Fixture for Fresh Token"""
    assert fresh_response.status_code == 200
    return fresh_response.json()["token"]


@pytest.fixture(scope="function")
def fresh_csrf_token(fresh_response: Response, config: FJWTConfig) -> str:
    """Fixture for Fresh CSRF Token"""
    assert fresh_response.status_code == 200
    return fresh_response.cookies.get(config.JWT_ACCESS_CSRF_COOKIE_NAME)


# endregion


# region Test Cases - Locations


def test_access_location_headers(api: TestClient, access_token: str):
    """Test Access Token Location in Headers"""

    response = api.post(
        "/read/access", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.json()["location"] == "headers"
    assert response.json()["type"] == "access"


def test_access_location_json(api: TestClient, access_token: str, config: FJWTConfig):
    """Test Access Token Location in JSON Body"""

    response = api.post("/read/access", json={config.JWT_JSON_KEY: access_token})
    assert response.json()["location"] == "json"
    assert response.json()["type"] == "access"


def test_access_location_query(api: TestClient, access_token: str, config: FJWTConfig):
    """Test Access Token Location in Query Parameters"""

    response = api.post(
        "/read/access", params={config.JWT_QUERY_STRING_NAME: access_token}
    )
    assert response.json()["location"] == "query"
    assert response.json()["type"] == "access"


def test_access_location_cookies(
    api: TestClient, access_token: str, access_csrf_token: str, config: FJWTConfig
):
    """Test Access Token Location in Cookies"""

    response = api.post(
        "/read/access",
        cookies={config.JWT_ACCESS_COOKIE_NAME: access_token},
        headers={config.JWT_ACCESS_CSRF_HEADER_NAME: access_csrf_token},
    )
    assert response.json()["location"] == "cookies"
    assert response.json()["type"] == "access"


def test_access_location_cookies_no_csrf(
    api: TestClient, access_token: str, config: FJWTConfig
):
    """Test Access Token Location in Cookies without CSRF Token"""

    response = api.post(
        "/read/access",
        cookies={config.JWT_ACCESS_COOKIE_NAME: access_token},
    )
    assert response.json() is None


def test_access_location_cookies_disabled_csrf(
    no_csrf_api: TestClient, config: FJWTConfig
):
    """Test Access Token Location in Cookies when CSRF Token is disabled"""

    response = no_csrf_api.get("/token/access")

    access_token = response.json()["token"]

    response = no_csrf_api.post(
        "/read/access",
        cookies={config.JWT_ACCESS_COOKIE_NAME: access_token},
    )
    assert response.json()["location"] == "cookies"
    assert response.json()["type"] == "access"


# endregion

# region Test Cases - Access Routes


def test_no_token_protected_access(api: TestClient):
    """Test Protected (Access Token) Route with no token provided

    Expected:
        401: Unauthorized
        message: "Missing JWT in request
    """
    with pytest.raises(exc.MissingTokenError):
        api.post("/protected/access")


def test_fresh_token_protected_access_headers(api: TestClient, fresh_token: str):
    """Test Protected (Access Token) Route with fresh token provided in headers

    Expected:
        200: OK
    """

    response = api.post(
        "/protected/access", headers={"Authorization": f"Bearer {fresh_token}"}
    )
    assert response.status_code == 200


def test_refresh_token_protected_access_headers(api: TestClient, refresh_token: str):
    """Test Protected (Access Token) Route with refresh token provided in headers

    Expected:
        401: Unauthorized
        message: "Access token required"
    """

    with pytest.raises(exc.AccessTokenRequiredError):
        api.post(
            "/protected/access", headers={"Authorization": f"Bearer {refresh_token}"}
        )


def test_access_token_protected_access_headers(api: TestClient, access_token: str):
    """Test Protected (Access Token) Route with access token provided in headers

    Expected:
        200: OK
    """

    response = api.post(
        "/protected/access", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200


def test_access_token_protected_access_json(
    api: TestClient, config: FJWTConfig, access_token: str
):
    """Test Protected (Access Token) Route with access token provided in json

    Expected:
        200: OK
    """

    response = api.post("/protected/access", json={config.JWT_JSON_KEY: access_token})
    assert response.status_code == 200


def test_access_token_protected_access_query(
    api: TestClient, config: FJWTConfig, access_token: str
):
    """Test Protected (Access Token) Route with access token provided in query

    Expected:
        200: OK
    """

    response = api.post(
        "/protected/access", params={config.JWT_QUERY_STRING_NAME: access_token}
    )
    assert response.status_code == 200


def test_access_token_protected_access_cookies_no_csrf(
    api: TestClient, config: FJWTConfig
):
    """Test Protected (Access Token) Route with access token provided in cookies and
    no CSRF token

    Expected:
        401: Unauthorized
        message: "Missing CSRF double submit token in request"
    """

    response = api.get("/token/access")
    assert response.status_code == 200
    assert "token" in response.json()
    access_token = response.json()["token"]

    response = api.post(
        "/read/access", headers={"Authorization": f"Bearer {access_token}"}
    )

    with pytest.raises(exc.MissingTokenError) as err:
        api.post(
            "/protected/access",
            cookies={config.JWT_ACCESS_COOKIE_NAME: access_token},
            headers={"Content-Type": "application/json"},
        )

    assert "Missing CSRF token" in err.value.args


def test_access_token_protected_access_cookies_csrf_cookies(
    api: TestClient, config: FJWTConfig, access_token: str, access_csrf_token: str
):
    """Test Protected (Access Token) Route with access token provided in cookies
    and CSRF token

    Expected:
        200: OK
    """

    response = api.post(
        "/protected/access",
        cookies={
            config.JWT_ACCESS_COOKIE_NAME: access_token,
        },
        headers={config.JWT_ACCESS_CSRF_HEADER_NAME: access_csrf_token},
    )
    assert response.status_code == 200


# endregion

# region Test Cases - Fresh Routes


def test_no_token_protected_fresh(api: TestClient):
    """Test Protected (Fresh Token) Route with no token provided

    Expected:
        401: Unauthorized
        message: "Missing JWT in request
    """

    with pytest.raises(exc.MissingTokenError):
        api.post("/protected/fresh")


def test_access_fresh_token_protected_fresh(api: TestClient, access_token: str):
    """Test Protected (Fresh Token) Route with access token provided

    Expected:
        401: Unauthorized
        message: "Fresh token required"
    """

    with pytest.raises(exc.FreshTokenRequiredError):
        api.post(
            "/protected/fresh", headers={"Authorization": f"Bearer {access_token}"}
        )


def test_refresh_fresh_token_protected_fresh(api: TestClient, refresh_token: str):
    """Test Protected (Fresh Token) Route with refresh token provided

    Expected:
        401: Unauthorized
        message: "Access token required"
    """

    with pytest.raises(exc.AccessTokenRequiredError):
        api.post(
            "/protected/fresh", headers={"Authorization": f"Bearer {refresh_token}"}
        )


def test_fresh_token_protected_fresh_headers(api: TestClient, fresh_token: str):
    """Test Protected (Fresh Token) Route with fresh token provided in headers

    Expected:
        200: OK
    """

    response = api.post(
        "/protected/fresh", headers={"Authorization": f"Bearer {fresh_token}"}
    )
    assert response.status_code == 200


def test_fresh_token_protected_fresh_json(
    api: TestClient, config: FJWTConfig, fresh_token: str
):
    """Test Protected (Fresh Token) Route with fresh token provided in JSON Body

    Expected:
        200: OK
    """

    response = api.post("/protected/fresh", json={config.JWT_JSON_KEY: fresh_token})
    assert response.status_code == 200


def test_fresh_token_protected_fresh_query(
    api: TestClient, config: FJWTConfig, fresh_token: str
):
    """Test Protected (Fresh Token) Route with fresh token provided in Query Parameters

    Expected:
        200: OK
    """

    response = api.post(
        "/protected/fresh", params={config.JWT_QUERY_STRING_NAME: fresh_token}
    )
    assert response.status_code == 200


def test_fresh_token_protected_fresh_cookies_csrf_cookies(
    api: TestClient, config: FJWTConfig, fresh_token: str, fresh_csrf_token: str
):
    """Test Protected (Fresh Token) Route with fresh token provided in Cookies
    and CSRF token

    Expected:
        200: OK
    """

    response = api.post(
        "/protected/access",
        cookies={
            config.JWT_ACCESS_COOKIE_NAME: fresh_token,
        },
        headers={config.JWT_ACCESS_CSRF_HEADER_NAME: fresh_csrf_token},
    )
    assert response.status_code == 200


# endregion

# region Test Cases - Refresh Routes


def test_no_token_protected_refresh(api: TestClient):
    """Test Protected (Refresh Token) Route with no token provided

    Expected:
        401: Unauthorized
        message: "Missing JWT in request
    """
    with pytest.raises(exc.MissingTokenError):
        api.post("/protected/refresh")


def test_access_token_protected_refresh(
    api: TestClient, config: FJWTConfig, access_token: str, access_csrf_token: str
):
    """Test Protected (Refresh Token) Route with access token provided

    Expected:
        401: Unauthorized
        message: "Refresh token required"
    """

    with pytest.raises(exc.RefreshTokenRequiredError):
        api.post(
            "/protected/refresh",
            cookies={
                config.JWT_REFRESH_COOKIE_NAME: access_token,
            },
            headers={config.JWT_REFRESH_CSRF_HEADER_NAME: access_csrf_token},
        )


def test_fresh_token_protected_refresh(
    api: TestClient, config: FJWTConfig, fresh_token: str, fresh_csrf_token: str
):
    """Test Protected (Refresh Token) Route with fresh token provided

    Expected:
        401: Unauthorized
        message: "Refresh token required"
    """

    with pytest.raises(exc.RefreshTokenRequiredError):
        api.post(
            "/protected/refresh",
            cookies={
                config.JWT_REFRESH_COOKIE_NAME: fresh_token,
            },
            headers={config.JWT_REFRESH_CSRF_HEADER_NAME: fresh_csrf_token},
        )


def test_refresh_token_protected_refresh(
    api: TestClient, config: FJWTConfig, refresh_token: str, refresh_csrf_token: str
):
    """Test Protected (Refresh Token) Route with refresh token provided

    Expected:
        200: OK
    """
    response = api.post(
        "/protected/refresh",
        cookies={
            config.JWT_REFRESH_COOKIE_NAME: refresh_token,
        },
        headers={config.JWT_REFRESH_CSRF_HEADER_NAME: refresh_csrf_token},
    )
    assert response.status_code == 200


# endregion

# region Test Cases - Blocklist Routes


def test_blocklist_access_token(api: TestClient, access_token: str):
    """Test a blocklist related scenario with access token

    Scenario:
        1. Check token not in blocklist
            Expected: 200
        2. Check token works
            Expected: 200
        3. Block token
            Expected: 200
        4. Check token in blocklist
            Expected: 200
        5. Check token no longer works
            Expected: 401
    """

    # Check token not in list
    blocklist = api.get("/blocklist").json()["blocklist"]
    assert access_token not in blocklist

    # Check token works
    response = api.post(
        "/protected/access", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200

    # Check Block token
    response = api.post(
        "/token/block", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200

    # Check token in blocklist
    blocklist = api.get("/blocklist").json()["blocklist"]
    assert access_token in blocklist

    # Check token no longer works
    with pytest.raises(exc.RevokedTokenError):
        api.post(
            "/protected/access", headers={"Authorization": f"Bearer {access_token}"}
        )


def test_blocklist_refresh_token(
    api: TestClient, config: FJWTConfig, refresh_token: str, refresh_csrf_token: str
):
    """Test a blocklist related scenario with refresh token

    Scenario:
        1. Check token not in blocklist
            Expected: 200
        2. Check token works
            Expected: 200
        3. Block token
            Expected: 200
        4. Check token in blocklist
            Expected: 200
        5. Check token no longer works
            Expected: 401
    """

    # Check token not in list
    blocklist = api.get("/blocklist").json()["blocklist"]
    assert refresh_token not in blocklist

    # Check token works
    response = api.post(
        "/protected/refresh",
        cookies={
            config.JWT_REFRESH_COOKIE_NAME: refresh_token,
        },
        headers={config.JWT_REFRESH_CSRF_HEADER_NAME: refresh_csrf_token},
    )
    assert response.status_code == 200

    # Check Block token
    response = api.post(
        "/token/block", headers={"Authorization": f"Bearer {refresh_token}"}
    )
    assert response.status_code == 200

    # Check token in blocklist
    blocklist = api.get("/blocklist").json()["blocklist"]
    assert refresh_token in blocklist

    # Check token no longer works
    with pytest.raises(exc.RevokedTokenError):
        api.post(
            "/protected/refresh",
            cookies={
                config.JWT_REFRESH_COOKIE_NAME: refresh_token,
            },
            headers={config.JWT_REFRESH_CSRF_HEADER_NAME: refresh_csrf_token},
        )


# endregion

# region Test Cases - Subject Routes


def test_no_authorization_get_subject(api: TestClient):
    """Test Get Subject Route with no token provided

    Expected:
        401: Unauthorized
        message: "Missing JWT in request
    """
    with pytest.raises(exc.MissingTokenError):
        api.get("/entitiy/subject")


def test_get_subject_access_token(api: TestClient, access_token: str):
    """Test Get Subject Route with access token provided

    Expected:
        200: OK
    """
    response = api.get(
        "/entitiy/subject", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200


def test_get_subject_refresh_token(api: TestClient, refresh_token: str):
    """Test Get Subject Route with refresh token provided

    Expected:
        200: OK
    """

    with pytest.raises(exc.AccessTokenRequiredError):
        api.get(
            "/entitiy/subject", headers={"Authorization": f"Bearer {refresh_token}"}
        )


def test_get_subject(api: TestClient, access_token: str):
    """Test Get Subject Route with access token provided

    Check that the subject scope 'test' is reached when requested

    Expected:
        200: OK
    """
    response = api.get(
        "/entitiy/subject", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json()["subject"]["uid"] == "test"
    assert response.json()["subject"]["email"] == "test@test.com"


def test_get_subject_reources(api: TestClient, access_token: str):
    """Test Get Subject Route with access token provided

    Check that the subject scope 'test' is reached when requested

    Expected:
        200: OK
    """
    # Check no resources
    response = api.get(
        "/entity/subject/resources",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert len(response.json()["resources"]) == 0

    # Post Resource for Subject
    response = api.post(
        "/entity/resources",
        json={"subject": "test", "resource": "A dummy resources"},
    )

    # Check resource added
    response = api.get(
        "/entity/subject/resources",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert len(response.json()["resources"]) == 1

    # Post Resource for Other Subject
    response = api.post(
        "/entity/resources",
        json={"subject": "foo", "resource": "A dummy resources"},
    )

    # Check no resource added for subject
    response = api.get(
        "/entity/subject/resources",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert len(response.json()["resources"]) == 1

    # Check total resources count
    response = api.get("/entity/resources")
    assert response.status_code == 200
    assert len(response.json()["resources"]) == 2


# endregion
