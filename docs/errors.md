# Error Handling

FastJWT provides multiple exceptions to handle JWT specific errors

## FastJWT Exceptions


### `FastJWTException`

**PARENT**: `Exception`

The Base FastJWT Exception. 

!!! note
    This exception is never raised directly in the code but is used to group all FastJWT exceptions under a same namespace.

### `BadConfigurationError`

**PARENT**: `FastJWTException`

Exception raised when FastJWT configuration contains wrong parameters. This exceptions might be raised when no secrets are sets, when a single secret is used with an asymmetric algorithm...

### `JWTDecodeError`

**PARENT**: `FastJWTException`

Exception raised when decoding JSON Web Token fails. This exception is raised when the token is not a proper JWT or when a `jwt` claim validation is not met.  

### `CSRFError`

**PARENT**: `FastJWTException`

Exception raised when CSRF protection failed. This exception is raised when the CSRF validation has failed. Mostly due to failing double submit token comparison.

### `TokenError`

**PARENT**: `FastJWTException`

Base Exception for token related errors. 

!!! note
    This exception is never raised directly in the code but is used to group all FastJWT token exceptions under a same namespace.

### `MissingTokenError`

**PARENT**: `TokenError`

Exception raised when no token can be parsed from request. This exception is raised when a token is required and not available.

### `MissingCSRFTokenError`

**PARENT**: `MissingTokenError`

Exception raised when no CSRF token can be parsed from request. This exception is raised when a CSRF token is required and not available. Only raised with authentication via Cookies.

### `RevokedTokenError`

**PARENT**: `TokenError`

Exception raised when a revoked token has been used. This exception can only be raised if a revoked token callback has been set. See [Custom Callbacks > Token Revokation](./callbacks/token.md)

### `FreshTokenRequiredError`

**PARENT**: `TokenError`

Exception raised when a not fresh token was used in request.

### `TokenTypeError`

**PARENT**: `TokenError`

Exception raised when a specific token type is expected.

!!! note
    This exception is never raised directly in the code but is used to group all FastJWT token type exceptions under a same namespace.

### `AccessTokenRequiredError`

**PARENT**: `TokenTypeError`

Exception raised when an `access` token is missing from request

### `RefreshTokenRequiredError`

**PARENT**: `TokenTypeError`

Exception raised when an `refresh` token is missing from request

## Automatic Error Handling

FastJWT provides a simple way to handle these exceptions. By default, no exception is handled by FastJWT, and when raised, results in a `500 Internal Server Error` HTTP Code

`FastJWT.handle_errors` method provides automatic error handlers for a FastAPI application.

```py linenums="1" hl_lines="7"
from fastapi import FastAPI, Depends
from fastjwt import FastJWT

app = FastAPI()
security = FastJWT()

security.handle_errors(app)

@app.get('/protected', dependencies=[Depends(security.access_token_required)])
def protected():
    return "OK"

```

=== "without Error Handling"
    ```shell
    $ curl http://0.0.0.0:8000/protected
    500 Internal Server Error
    ```
=== "with Error Handling"
    ```shell
    $ curl http://0.0.0.0:8000/protected
    401 {"message": "Missing JWT in request"}
    ```

All the predefined message are `FastJWT` properties and can be set as regular python properties.
Here is a list of all the property names and default value.

```py
MSG_DEFAULT = "FastJWTException"
MSG_TOKEN_ERROR = "Token Error"
MSG_MISSING_TOKEN_ERROR = "Missing JWT in request"
MSG_MISSING_CSRF_ERROR = "Missing CSRF double submit token in request"
MSG_TOKEN_TYPE_ERROR = "Bad token type"
MSG_REVOKED_TOKEN_ERROR = "Invalid token"
MSG_TOKEN_REQUIRED_ERROR = "Token required"
MSG_FRESH_TOKEN_REQUIRED_ERROR = "Fresh token required"
MSG_ACCESS_TOKEN_REQUIRED_ERROR = "Access token required"
MSG_REFRESH_TOKEN_REQUIRED_ERROR = "Refresh token required"
MSG_CSRF_ERROR = "CSRF double submit does not match"
MSG_DECODE_JWT_ERROR = "Invalid Token"
```

## Custom Error Handling

If you need to enable a custom behavior on a specific error you can use the `FastAPI.exception_handler`. See [FastAPI Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/)

```py linenums="1" hl_lines="9-14"
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastjwt import FastJWT
import fastjwt.exceptions as fexc

app = FastAPI()
security = FastJWT()

@app.exception_handler(fexc.MissingTokenError)
async def missing_token_exception_handler(
    request: Request, 
    exc: fexc.MissingTokenError
):
    return JSONResponse(
        status_code=401,
        content={"message": "Please provide an authentication token"}
    )

@app.get('/protected', dependencies=[Depends(security.access_token_required)])
def protected():
    return "OK"

```