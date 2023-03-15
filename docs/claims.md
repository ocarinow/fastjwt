# Claims

The JSON Web Tokens might contain the following **claims** _(json keys)_. You can find additional details on the [official standard specification](https://www.rfc-editor.org/rfc/rfc7519).
All the following claims are the standard JWT claims and are handled by fastjwt during execution. You must avoid interacting with these values manually.

## Standard JWT Claims

### `iss`

`Optional[str]`

**Issuer** claim identifying the principal that issued the JWT

### `sub`

`Optional[str]`

**Subject** claim identifying the principal that is the subject of the JWT

### `aud`

`Optional[str | List[str]]`

**Audience** claim identifying the recipients that the JWT is intended for.

### `exp`

`Optional[float | int] as datetime`

**Expiration Time** claim identifying the datetime **after** which the JWT must NOT be accepted by the server.

### `nbf`

`Optional[float | int] as datetime`

**Not Before** claim identifying the datetime **before** which the JWT must NOT be accepted by the server.

### `iat`

`Optional[float | int] as datetime`

**Issued at** claim identifying the datetime at which the JWT was issued.

### `jti`

`Optional[str]`

**JWT ID** claim is a unique identifier for the JWT.

## FastJWT Claims

In addition to the standard claims fastjwt adds custom claims to handle the following features:

- Access/Refresh token specification
- CSRF protection for authentication with cookies
- Token freshness for operation where login step is required
- Scopes for privileges management

!!! info "Info on Scopes"
    Scopes are not available in the current version of fastjwt. The claim exists in the `TokenPayload` object for next feature anticipation.

### `fresh`

`bool`

Claim to indicate if the token is fresh. Fresh token are usually required when sensitive operation are done by the user _(e.g password update, privilege management...)_

### `csrf`

`Optional[str]`

Claim containing a double submit token that must be compared to a request CSRF token when authenticating with cookies. Check [Cross-Site Request Forgery](https://developer.mozilla.org/docs/Glossary/CSRF) for additional details.

### `type`

`Literal["access"] | Literal["refresh"]`

Claim identifying the type of the token. Some operation require refresh token _-usually to refresh an access token-_ while other are strictly tied to access tokens

### `scopes`

`Optional[List[str]]`

Claim containing a list of permissions/privileges for additional route restriction. The system also allows for scoped rights on server.

## Used defined claims

While JWTs should avoid containing sensitive information since JWTs are easyly readable _(base64 encoded)_, you can provide additional data to a JWT.

To add additional claims to a token use the `FastJWT.create_access_token` and `FastJWT.create_refresh_token` keyword arguments.

```py
from fastjwt import FastJWT
from fastjwt import TokenPayload

security = FastJWT(...)
token = security.create_access_token("unique_identifier", foo="bar")
payload = TokenPayload.decode(token, verify=False)

print(payload.sub)
>>> "unique_identifier"
print(payload.foo)
>>> "bar"
```

!!! warning "Reserved claims"
    Do not use the standard claims as keyword arguments in the methods above to avoid undesired behavior

!!! warning "JSON serializable python object"
    Do not in order to encode a token the `json` package from the standard library is used. 
    Therefore, you won't be able to serialize object that are not supported by the `json` library

    ```py
    from fastjwt import FastJWT
    from fastjwt import TokenPayload
    from datetime import datetime

    security = FastJWT(...)
    # The following lie will raise an error since datetime.datetime is not `json` serializable
    token = security.create_access_token("unique_identifier", foo=datetime(2023, 1, 1, 12, 0))
    ```