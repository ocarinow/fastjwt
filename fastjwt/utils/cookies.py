from fastapi import Response

from fastjwt.settings import FastJWTConfig


def set_access_cookie(response: Response, token: str, config: FastJWTConfig) -> None:
    """Set access token cookie in response

    Args:
        response (Response): response
        token (str): access token
        config (FastJWTConfig): Configuration object regarding JWT management
    """
    if "cookies" in config._JWT_LOCATIONS:
        # Make cookie set op. only possible
        # if "cookies" is a Config TokenLocation
        response.set_cookie(
            key=config.JWT_COOKIE_NAME,
            value=token,
            max_age=None,
            expires=None,
            path=config.JWT_COOKIE_PATH,
            domain=config.JWT_COOKIE_DOMAIN,
            secure=config.JWT_COOKIE_SECURE,
            httponly=config.JWT_COOKIE_HTTPONLY,
            samesite=config.JWT_COOKIE_SAMESITE,
        )


def unset_access_cookie(response: Response, config: FastJWTConfig) -> None:
    """Remove access token in cookies

    Args:
        response (Response): reponse
        config (FastJWTConfig): Configuration object regarding JWT management
    """
    response.set_cookie(
        key=config.JWT_COOKIE_NAME,
        value="",
        max_age=None,
        expires=None,
        path=config.JWT_COOKIE_PATH,
        domain=config.JWT_COOKIE_DOMAIN,
        secure=config.JWT_COOKIE_SECURE,
        httponly=config.JWT_COOKIE_HTTPONLY,
        samesite=config.JWT_COOKIE_SAMESITE,
    )
