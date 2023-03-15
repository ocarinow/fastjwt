# Main Dependencies

## Request token dependencies

Sometimes, you may need to access the data relative to JWT authentication in request. such data might include, the encoded JWT, the CSRF double submit token, the location of the JWT...

To retrieve these information from request, FastJWT provides a `FastJWT.get_token_from_request`

`get_token_from_request` allow you to specify the token type you wish to retrieve with the `type` argument and to enforce the token availability with the `optional` argument

```py linenums="1" hl_lines="9-17"
from fastjwt import FastJWT
from fastjwt import RequestToken

security = FastJWT()

TokenGetter = Callable[[Request], Awaitable[RequestToken]]
OptTokenGetter = Callable[[Request], Awaitable[RequestToken | None]]


get_access_from_request: TokenGetter = security.get_token_from_request(
    type: TokenType = "access",
    optional: bool = False
)

get_optional_refresh_from_request: OptTokenGetter = security.get_token_from_request(
    type: TokenType = "access",
    optional: bool = False
)

@app.get('/get_token')
async def get_token(token: RequestToken = Depends(get_access_from_request)):
    ...

```

Please note that even if `optional` is set to `False`. The route will raise an error only because no token is available in request and not because the token in request has been invalidated.

`get_token_from_request` dependencies does not provide token validation. This dependency only look for token's presence in request

## Token validation dependencies

FastJWT provides 3 main dependencies for token requirements

These methods are FastJWT properties returning a FastAPI dependency `Callable[[Request], TokenPayload]`. When these dependencies are resolved, they return a `TokenPayload`

### `FastJWT.access_token_required`

`access_token_required` is a property returning a FastAPI dependency to enforce the presence and validity of an `access` token in request. This dependency will apply the following verification:

- [X] JWT Validation: verify `exp`, `iat`, `nbf`, `iss`, `aud` claims
- [X] Token type verification: `access` only
- [X] CSRF double submit verification: if CSRF enabled and token location in cookies
- [ ] Token freshness: not required for this dependency

### `FastJWT.refresh_token_required`

`refresh_token_required` is a property returning a FastAPI dependency to enforce the presence and validity of a `refersh` token in request. This dependency will apply the following verification:

- [X] JWT Validation: verify `exp`, `iat`, `nbf`, `iss`, `aud` claims
- [X] Token type verification: `request` only
- [X] CSRF double submit verification: if CSRF enabled and token location in cookies
- [ ] Token freshness: not required for this dependency

### `FastJWT.fresh_token_required`

`access_token_required` is a property returning a FastAPI dependency to enforce the presence and validity of an `access` token in request. It also needs the token to be `fresh` This dependency will apply the following verification:

- [X] JWT Validation: verify `exp`, `iat`, `nbf`, `iss`, `aud` claims
- [X] Token type verification: `access` only
- [X] CSRF double submit verification: if CSRF enabled and token location in cookies
- [X] Token freshness: not required for this dependency

## Additional token dependency

In addition to the 3 dependencies specified above, FastJWT provides `FastJWT.token_required` as an additional layer of customization for token requirements

```py linenums="1" hl_lines="9-26"
from fastapi import FastAPI
from fastapi import Depends
from fastjwt import FastJWT
from fastjwt import TokenPayload

app = FastAPI()
security = FastJWT()

access_token_required = security.token_required(
    type: str = "access"
    verify_type: bool = True
    verify_fresh: bool = False
    verify_csrf: Optional[bool] = None
)
fresh_token_required = security.token_required(
    type: str = "access"
    verify_type: bool = True
    verify_fresh: bool = True
    verify_csrf: Optional[bool] = None
)
refresh_token_required = security.token_required(
    type: str = "refresh"
    verify_type: bool = True
    verify_fresh: bool = False
    verify_csrf: Optional[bool] = None
)

no_csrf_required = security.token_required(
    type: str = "access"
    verify_type: bool = True
    verify_fresh: bool = False
    verify_csrf: Optional[bool] = False
)

@app.post('/no_csrf')
def post_no_csrf(payload: TokenPayload = Depends(no_csrf_required)):
    # This function is protected but does not require
    # CSRF double submit token in case of authentication via Cookies
    ...
```

We have regenrated the main token dependencies from the `FastJWT.token_required` method in the highlighted. `FastJWT.token_required` returns a Callable to be used as a dependency.

`(str, bool, bool, Optional[bool]) -> Callable[[Request], TokenPayload]`

As a custom token validation dependency, we have created the `no_csrf_required`. This dependency requires a valid `access` token in request, but it will not execute CSRF validation if the token is located in cookies.

!!! note "WIP"
    The `verify_csrf` argument is a Optional boolean to enable/disable CSRF protection. If `None` it uses the default `FJWTConfig.JWT_COOKIE_CSRF_PROTECT` setting