import logging
from typing import Any
from typing import Dict
from typing import Callable
from typing import Optional
from typing import Coroutine

from fastapi import Request

from ..types import RequestToken
from ..types import TokenLocations
from ..errors import NoAuthorizationError
from ..settings import FastJWTConfig


async def _get_token_in_header(
    request: Request, config: FastJWTConfig
) -> Optional[RequestToken]:
    """Get access token from header

    The usual header is of type 'Authorization: Bearer ...'

    Args:
        request (Request): the request containing (or not) the header
        config (FastJWTConfig): Configuration object regarding JWT management

    Raises:
        NoAuthorizationError: Raised when no token is available in headers

    Returns:
        Optional[RequestToken]: the token available in header
    """
    # Get Header
    auth_header: Optional[str] = request.headers.get(config.JWT_HEADER_NAME)
    # If Header is not None
    if auth_header and auth_header.startswith(f"{config.JWT_HEADER_TYPE} "):
        token = auth_header.replace(f"{config.JWT_HEADER_TYPE} ", "")
        return RequestToken(access_token=token, location="headers")
    raise NoAuthorizationError(f"Missing '{config.JWT_HEADER_TYPE}' header")


async def _get_token_in_cookies(
    request: Request, config: FastJWTConfig
) -> Optional[RequestToken]:
    """Get access token from cookies

    Args:
        request (Request): the request containing (or not) the cookie
        config (FastJWTConfig): Configuration object regarding JWT management

    Raises:
        NoAuthorizationError: Raised when no token is available in cookies

    Returns:
        Optional[RequestToken]: the token available in cookies
    """
    cookie_token = request.cookies.get(config.JWT_COOKIE_NAME)
    if cookie_token:
        return RequestToken(access_token=cookie_token, location="cookies")
    raise NoAuthorizationError(f"Missing '{config.JWT_COOKIE_NAME}' cookie")


async def _get_token_in_json(
    request: Request, config: FastJWTConfig
) -> Optional[RequestToken]:
    """Get access token from json payload

    Args:
        request (Request): the request containing (or not) the payload
        config (FastJWTConfig): Configuration object regarding JWT management

    Raises:
        NoAuthorizationError: Raised when no token is available in body

    Returns:
        Optional[RequestToken]: the token available in body
    """
    try:
        if (
            request.method == "POST"
            and request.headers.get("content-type") == "application/json"
        ):
            json_data: Dict[str, Any] = await request.json()
            json_token = json_data.get(config.JWT_JSON_ACCESS_KEY)
            if isinstance(json_token, str):
                return RequestToken(access_token=json_token, location="json")
    except Exception:
        ...
    raise NoAuthorizationError(
        f"Missing '{config.JWT_JSON_ACCESS_KEY}' key in json data"
    )


async def _get_token_in_query(
    request: Request, config: FastJWTConfig
) -> Optional[RequestToken]:
    """Get access token from query parameters

    Args:
        request (Request): the request containing (or not) the query params
        config (FastJWTConfig): Configuration object regarding JWT management

    Raises:
        NoAuthorizationError: Raised when no token is available in query

    Returns:
        Optional[RequestToken]: the token available in query
    """
    query_token = request.query_params.get(config.JWT_QUERY_STRING_NAME)
    if query_token:
        return RequestToken(access_token=query_token, location="query")
    raise NoAuthorizationError(
        f"Missing '{config.JWT_QUERY_STRING_NAME}' query parameter in request"
    )


TOKEN_GETTERS: Dict[
    str, Callable[[Request, FastJWTConfig], Coroutine[Any, Any, Optional[RequestToken]]]
] = {
    "json": _get_token_in_json,
    "headers": _get_token_in_header,
    "cookies": _get_token_in_cookies,
    "query": _get_token_in_query,
}


async def get_token_from_request(
    request: Request,
    config: FastJWTConfig,
    locations: TokenLocations = ["cookies", "headers", "json", "query"],
) -> Optional[RequestToken]:
    """Get the access token from a request

    Args:
        request (Request): the request to analyse
        config (FastJWTConfig): Configuration object regarding JWT management
        locations (TokenLocations, optional): Locations to look the token for. Defaults to ["cookies", "headers", "json", "query"].

    Returns:
        Optional[RequestToken]: The detected access token
    """
    for location in set(config.JWT_LOCATIONS).intersection(set(locations)):
        try:
            getter = TOKEN_GETTERS.get(location)
            return await getter(request, config=config) if getter else None
        except NoAuthorizationError as e:
            logging.error(e)
            continue
