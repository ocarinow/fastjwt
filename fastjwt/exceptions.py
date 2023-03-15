class FastJWTException(Exception):
    """Base FastJWT Exception"""

    pass


class BadConfigurationError(FastJWTException):
    """Exception raised when FastJWT configuration contains wrong parameters"""

    pass


class JWTDecodeError(FastJWTException):
    """Exception raised when decoding JSON Web Token fails"""

    pass


class NoAuthorizationError(FastJWTException):
    """Exception raised when no token can be parsed from request"""

    pass


class CSRFError(FastJWTException):
    """Exception raised when CSRF protection failed"""

    pass


# Token Exception


class TokenError(FastJWTException):
    """Base Exception for token related errors"""

    pass


class MissingTokenError(TokenError):
    """Exception raised when no token can be parsed from request"""

    pass


class MissingCSRFTokenError(MissingTokenError):
    """Exception raised when no CSRF token can be parsed from request"""

    pass


class TokenTypeError(TokenError):
    """Exception raised when a specific token type is expected"""

    pass


class RevokedTokenError(TokenError):
    """Exception raised when a revoked token has been used"""

    pass


class TokenRequiredError(TokenError):
    """Exception raised when no token was used in request"""

    pass


class FreshTokenRequiredError(TokenError):
    """Exception raised when a not fresh token was used in request"""

    pass


class AccessTokenRequiredError(TokenTypeError):
    """Exception raised when an `access` token is missing from request"""

    pass


class RefreshTokenRequiredError(TokenTypeError):
    """Exception raised when an `refresh` token is missing from request"""

    pass
