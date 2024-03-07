# Dependency Aliases

If you are familiar with [FastAPI Dependency Injection system](https://fastapi.tiangolo.com/tutorial/dependencies/),
you know you need to import the `Depends` object to declare a dependency.
Since FastJWT is designed to work with FastAPI, we provide quick aliases to get the most accessed dependencies.

The following example demonstrate how FastJWT aliases can help you reduce verbosity.

=== "Without aliases"

    ```py
    from fastapi import FastAPI
    from fastapi import Depends
    import fastjwt

    app = FastAPI()
    security = FastJWT()
    security.handle_errors(app)

    @app.route('/', dependencies=[Depends(security.access_token_required)])
    def root(subject = Depends(security.get_current_subject), token = Depends(security.get_token_dep)):
        ...
    ```

=== "With aliases"

    ```py
    from fastapi import FastAPI
    from fastapi import Depends
    import fastjwt

    app = FastAPI()
    security = FastJWT()
    security.handle_errors(app)

    @app.route('/', dependencies=[security.ACCESS_REQUIRED])
    def root(subject = security.CURRENT_SUBJECT, token = security.RAW_ACCESS_TOKEN):
        ...
    ```

## Aliases

### `ACCESS_REQUIRED`

Type: [`TokenPayload`](../api/token_payload.md)

Returns the access token payload if valid. Enforce the access token validation

??? example

    ```py hl_lines="8"
    from fastapi import FastAPI
    import fastjwt

    app = FastAPI()
    security = FastJWT()

    @app.route('/protected')
    def protected(payload = security.ACCESS_REQUIRED):
        return f"Your Access Token Payload is {payload}"
    ```

### `ACCESS_TOKEN`

Type: [`RequestToken`](../api/token_payload.md)

Returns the encoded access token. **DOES NOT** Enforce the access token validation

??? example

    ```py hl_lines="9"
    from fastapi import FastAPI
    import fastjwt

    app = FastAPI()
    security = FastJWT()

    # Use route dependency to enforce validation in conjunction with ACCESS_TOKEN
    @app.route('/protected', dependencies=[security.ACCESS_REQUIRED])
    def protected(token = security.ACCESS_TOKEN):
        return f"Your Access Token is {token}"
    ```

### `REFRESH_REQUIRED`

Type: [`TokenPayload`](../api/token_payload.md)

Returns the refresh token payload if valid. Enforce the refresh token validation

??? example

    ```py hl_lines="8"
    from fastapi import FastAPI
    import fastjwt

    app = FastAPI()
    security = FastJWT()

    @app.route('/refresh')
    def refresh(payload = security.REFRESH_REQUIRED):
        return f"Your Refresh Token Payload is {payload}"
    ```

### `REFRESH_TOKEN`

Type: [`RequestToken`](../api/token_payload.md)

Returns the encoded refresh token. **DOES NOT** Enforce the refresh token validation

??? example

    ```py hl_lines="9"
    from fastapi import FastAPI
    import fastjwt

    app = FastAPI()
    security = FastJWT()

    # Use route dependency to enforce validation in conjunction with REFRESH_TOKEN
    @app.route('/refresh', dependencies=[security.REFRESH_REQUIRED])
    def refresh(token = security.REFRESH_TOKEN):
        return f"Your Refresh Token is {token}"
    ```

### `FRESH_REQUIRED`

Type: [`TokenPayload`](../api/token_payload.md)

Returns the access token payload if valid & **FRESH**. Enforce the access token validation

??? example

    ```py hl_lines="8"
    from fastapi import FastAPI
    import fastjwt

    app = FastAPI()
    security = FastJWT()

    @app.route('/protected', dependencies=[security.FRESH_REQUIRED])
    def protected():
        return "Congratulations! Your have a fresh and valid access token."
    ```

### `CURRENT_SUBJECT`

Type: `Any`

Returns the current subject. Enforce the access token validation

!!! note
    You must set a subject getter to use this dependency. See [Custom Callbacks > User Serialization](../callbacks/user.md)

??? example

    ```py hl_lines="8"
    from fastapi import FastAPI
    import fastjwt

    app = FastAPI()
    security = FastJWT()

    @app.route('/whoami')
    def whoami(subject = security.CURRENT_SUBJECT):
        return f"You are: {subject}"
    ```

### `BUNDLE` / `DEPENDENCY`

Type: [`FastJWTDeps`](../api/deps.md)

Returns the [`FastJWTDeps`](./bundle.md) dependency bundle to be used within the route

??? example

    ```py hl_lines="8"
    from fastapi import FastAPI
    import fastjwt

    app = FastAPI()
    security = FastJWT()

    @app.route('/create_token')
    def create_token(fjwt = security.BUNDLE):
        token = fjwt.create_access_token(uid="test")
        fjwt.set_access_cookie(token)
        return "OK"
    ```
