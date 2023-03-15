# Refreshing Tokens

Since JWTs have a strict `exp` Expiration Time, a long session might result in multiple logouts and `401 Authentication` errors. To avoid such bahvior, refresh tokens are used to enable the generation of additional access token without the need to log in again.

## Implicit refresh with Cookies

!!! warning "WIP"
    This section is work in progress

## Explicit refresh

When your application cannot use implicit refresh because cookies are not an option _(mobile application, SDKs, APIs,...)_, you might need to declare explicitly the refresh logic on you application.

```py linenums="1" hl_lines="27-34"
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException
from fastjwt import FastJWT
from fastjwt import TokenPayload

app = FastAPI()
security = FastJWT()

class LoginForm(BaseModel):
    username: str
    password: str

@app.post('/login')
def login(data: LoginForm):
    if data.username == "test" and data.password == "test":
        access_token = security.create_access_token(data.username)
        refresh_token = security.create_refresh_token(data.username)
        return {
            "access_token": access_token, 
            "refresh_token": refresh_token
        }
    raise HTTPException(401, "Bad username/password")


# We use the FastJWT.refresh_token_required method to enforce
# the refresh token validation.
@app.post('/refresh')
def refresh(
    refresh_payload: TokenPayload = Depends(security.refresh_token_required)
):
    access_token = security.create_access_token(refresh_payload.sub)
    return {"access_token": access_token}


@app.get('/protected', dependencies=[Depends(security.access_token_required)])
def protected():
    return "You have access to this protected resource"
```

On this example, the `/refresh` route will only look for a valid refresh token in request. Once verified, it generates a new access token to be used to extend the session. 

This example is a very basic implementation of an explicit refresh mechanism. On a production case you might want to retrieve the current access token to revoke it. Hence avoiding to generate infinite valid access token.

=== "1. Login"

    ```shell
    # We login to obtain a token
    $ curl -s -X POST --json '{"username":"test", "password":"test"}' http://0.0.0.0:8000/login
    {"access_token": $TOKEN, "refresh_token": $REFRESH_TOKEN}
    ```
=== "2. Sensitive Operation"

    ```shell
    # We request the protceted route with the token
    $ curl -s --oauth2-bearer $TOKEN http://0.0.0.0:8000/sensitive_operation
    "You have access to this sensitive operation"
    ```
=== "3. Refresh access token"

    ```shell
    # We refresh the access token to get a new one
    $ curl -s --oauth2-bearer $REFRESH_TOKEN http://0.0.0.0:8000/refresh
    {"access_token": $NEW_TOKEN}
    ```

As you can see on the last step, refreshing mechanism allow to obtain new tokens without the need to authenticate again.
