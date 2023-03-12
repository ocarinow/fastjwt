from typing import Any
from typing import Dict
from typing import List
from typing import Callable
from typing import Optional
from typing import Awaitable

try:
    from typing import ParamSpecKwargs
except Exception:
    from typing_extensions import ParamSpecKwargs

from fastapi import Request

from .types import TokenLocation
from .types import TokenLocations
from .config import FJWTConfig
from .models import RequestToken
from .exceptions import MissingTokenError
from .exceptions import MissingCSRFTokenError


async def _get_token_from_headers(
    request: Request, config: FJWTConfig, **kwargs
) -> RequestToken:
    """Get access token from header

    The usual header is of type 'Authorization: Bearer ...'

    Args:
        request (Request): the request containing (or not) the header
        header_name (str, optional): The Header name. Defaults to "Authorization".
        header_type (str, optional): The Header type. Defaults to "Bearer".

    Raises:
        MissingTokenError: Raised when no token is available in headers

    Returns:
        RequestToken: the token available in headers
    """
    # Get Header
    auth_header: Optional[str] = request.headers.get(config.JWT_HEADER_NAME)
    if auth_header is None:
        raise MissingTokenError(
            f"Missing '{config.JWT_HEADER_TYPE}' in '{config.JWT_HEADER_NAME}' header."
        )

    if config.JWT_HEADER_TYPE:
        # Authorization Header has a type
        # e.g '<HEADER_NAME>: <HEADER_TYPE> $TOKEN'
        # TODO Handle comma delimited header
        token = auth_header.replace(f"{config.JWT_HEADER_TYPE} ", "")
    else:
        # Authorization Header has no type
        # e.g '<HEADER_NAME>: $TOKEN'
        token = auth_header

    return RequestToken(token=token, csrf=None, location="headers")


async def _get_token_from_cookies(
    request: Request, config: FJWTConfig, refresh: bool = False, **kwargs
) -> RequestToken:
    """Get access token from cookies

    Args:
        request (Request): the request containing (or not) the cookie
        refresh (bool, optional): Whether to look for an access or refresh token. Defaults to False.
        cookie_key (str, optional): Cookie name of the token. Defaults to "access_token_cookie".
        csrf_header_key (str, optional): CSRF Header. Defaults to "csrf_access_token".
        csrf_field_key (str, optional): CSRF Form field name. Defaults to "csrf_token".
        csrf_protect (bool, optional): CSRF protection enabled. Defaults to True.
        csrf_in_form (bool, optional): Check for CSRF in potential form data. Defaults to True.
        csrf_methods (HTTPMethods, optional): Request methods to check for CSRF. Defaults to ["POST", "PUT", "PATCH", "DELETE"].

    Raises:
        MissingTokenError: Raised when no token is available in cookies
        MissingTokenError: Missing CSRF token

    Returns:
        RequestToken: the token available in cookies
    """
    cookie_key = config.JWT_ACCESS_COOKIE_NAME
    csrf_header_key = config.JWT_ACCESS_CSRF_HEADER_NAME
    csrf_field_key = config.JWT_ACCESS_CSRF_FIELD_NAME
    if refresh:
        cookie_key = config.JWT_REFRESH_COOKIE_NAME
        csrf_header_key = config.JWT_REFRESH_CSRF_HEADER_NAME
        csrf_field_key = config.JWT_REFRESH_CSRF_FIELD_NAME

    cookie_token = request.cookies.get(cookie_key)
    if not cookie_token:
        raise MissingTokenError(f"Missing cookie '{cookie_key}'.")

    csrf_token = None
    if (
        config.JWT_COOKIE_CSRF_PROTECT
        and request.method.upper() in config.JWT_CSRF_METHODS
    ):
        # If the CSRF cookie protection is enabled
        # and the request's method should enforce CSRF checking
        csrf_token = request.headers.get(csrf_header_key.lower())
        if not csrf_token and config.JWT_CSRF_CHECK_FORM:
            form_data = await request.form()
            if form_data is not None:
                csrf_token = form_data.get(csrf_field_key)
        if not csrf_token:
            raise MissingCSRFTokenError("Missing CSRF token")

    return RequestToken(
        token=cookie_token,
        csrf=csrf_token,
        type=("refresh" if refresh else "access"),
        location="cookies",
    )


async def _get_token_from_query(
    request: Request, config: FJWTConfig, **kwargs
) -> RequestToken:
    """Get access token from query parameters

    Args:
        request (Request): the request containing (or not) the query params
        param_name (str, optional): the parameter name for the token. Defaults to "token".

    Raises:
        MissingTokenError: Raised when no token is available in query

    Returns:
        RequestToken: the token available in query
    """
    query_token = request.query_params.get(config.JWT_QUERY_STRING_NAME)
    if query_token is None:
        raise MissingTokenError(
            f"Missing '{config.JWT_QUERY_STRING_NAME}' in query parameters"
        )

    return RequestToken(token=query_token, location="query")


async def _get_token_from_json(
    request: Request, config: FJWTConfig, refresh: bool = False, **kwargs
) -> RequestToken:
    """Get access token from json data

    Args:
        request (Request): the request containing (or not) the payload
        refresh (bool, optional): Whether to look for an access or refresh token. Defaults to False.
        key (str, optional): the json key containing the token. Defaults to "access_token".

    Raises:
        MissingTokenError: Invalid content-type. Must be application/json
        MissingTokenError: Missing token in json data

    Returns:
        Optional[RequestToken]: _description_
    """
    if not (request.headers.get("content-type") == "application/json"):
        raise MissingTokenError("Invalid content-type. Must be application/json")

    key = config.JWT_JSON_KEY
    token_type = "access"
    if refresh:
        token_type = "refresh"
        key = config.JWT_REFRESH_JSON_KEY

    try:
        json_data: Dict[str, Any] = await request.json()
        json_token = json_data.get(key)
        if isinstance(json_token, str):
            return RequestToken(
                token=json_token,
                type=token_type,
                location="json",
            )
    except Exception:
        raise MissingTokenError("Token is not parsable")
    raise MissingTokenError("Missing token in json data")


TOKEN_GETTERS: Dict[
    TokenLocation,
    Callable[[Request, FJWTConfig, ParamSpecKwargs], Awaitable[RequestToken]],
] = {
    "json": _get_token_from_json,
    "query": _get_token_from_query,
    "cookies": _get_token_from_cookies,
    "headers": _get_token_from_headers,
}


async def _get_token_from_request(
    request: Request,
    config: FJWTConfig,
    refresh: bool = False,
    locations: Optional[TokenLocations] = None,
    **kwargs,
) -> RequestToken:
    errors: List[MissingTokenError] = []

    if locations is None:
        locations = config.JWT_TOKEN_LOCATION

    for location in locations:
        try:
            getter = TOKEN_GETTERS[location]
            token = await getter(request, config=config, refresh=refresh)
            if token is not None:
                return token
        except MissingTokenError as e:
            errors.append(e)

    if errors:
        raise MissingTokenError(*(str(err) for err in errors))
    raise MissingTokenError(f"No token found in request from '{locations}'")
