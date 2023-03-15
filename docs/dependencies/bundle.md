# Dependency Bundle

In order to avoid redundant or outside of logic code, FastJWT provides a way to inject a dependency bundle in route's function with `FastJWT.get_dependency`.

`FastJWT.get_dependency` returns a `FastJWTDeps` instance that is tied to the request and response of the route. This object includes all the dependency available in `FastJWT`

To show how `FastJWTDeps` can help reduce code complexity let's focus on authentication via Cookies

=== "With Bundle"
    ```py linenums="1" hl_lines="16 22"
    from pydantic import BaseModel
    from fastapi import FastAPI, Depends
    from fastjwt import FastJWT, FastJWTDeps

    app = FastAPI()
    security = FastJWT()

    class LoginData:
        username: str
        password: str

    @app.post('/login')
    def login(data: LoginData, fjwt: FastJWTDeps = Depends(security.get_dependency)):
        if data.username == "test" and data.password == "test":
            token = fjwt.create_access_token(uid="test")
            fjwt.set_access_cookie(token)
            return "CONNECTED"
        return "NOT CONNECTED"

    @app.post('/logout', dependencies=[Depends(security.access_token_required)])
    def logout(fjwt: FastJWTDeps = Depends(security.get_dependency)):
        fjwt.unset_access_cookies()
        return "DISCONNECTED"
    ```
=== "Without Bundle"
    ```py linenums="1" hl_lines="17 18 24 25"
    from pydantic import BaseModel
    from fastapi import FastAPI, Depends
    from fastapi.responses import JSONResponse
    from fastjwt import FastJWT

    app = FastAPI()
    security = FastJWT()

    class LoginData:
        username: str
        password: str

    @app.post('/login')
    def login(data: LoginData):
        if data.username == "test" and data.password == "test":
            token = security.create_access_token(uid="test")
            response = JSONResponse(status_code=200, content="CONNECTED")
            security.set_access_cookie(token, response)
            return response
        return "NOT CONNECTED"

    @app.post('/logout', dependencies=[Depends(security.access_token_required)])
    def logout():
        response = JSONResponse(status_code=200, content="DISCONNECTED")
        security.unset_access_cookies(response)
        return response
    ```

The main difference in those 2 snippets is the implicit context grapped by `FastJWTDeps`. You don't need to generate get access to the request or create a response object to set/unset cookies for example. This allows for less code, but mostly prevents you to handle `fastapi.Response` objects that might be outside of your function logic.