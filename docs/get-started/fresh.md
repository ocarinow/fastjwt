# Token Freshness

Token freshness mechanisms enable additional protection for sensitive operations. 
Fresh tokens should only be generated when the user provides credentials information on a login operation.

Every time a user authenticates itself with credentials, it receives a `fresh` token. Every time, an access token is refreshed _(implicitly or explictly)_ the access token generated **SHOULD NOT** be `fresh`.

Most of  your protected endpoints should not consider the `fresh` state of the access token, but in specific application cases, the use of a `fresh` token enables an additional layer of protection by requiring the user to authenticate itself.

Such operations includes but are not limited to:

- Password update
- User information update
- Privilege/Permission management
- ...

## Combined with explicit refresh mechanism

Let's start from the example in the previous [Refreshing tokens](./refresh.md#explicit-refresh) section.

```py linenums="1"
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException
from fastjwt import FastJWT, TokenPayload

app = FastAPI()
security = FastJWT()

class LoginForm(BaseModel):
    username: str
    password: str

@app.post('/login')
def login(data: LoginForm):
    if data.username == "test" and data.password == "test":
        access_token = security.create_access_token(
            data.username, 
            fresh=True
        )
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
    refresh_payload: TokenPayload = Depends(security.refresh_token_required())
):
    access_token = security.create_access_token(
        refresh_payload.sub, 
        fresh=False
    )
    return {"access_token": access_token}


@app.get('/protected', dependencies=[Depends(security.access_token_required())])
def protected():
    return "You have access to this protected resource"

@app.get('/sensitive_operation', dependencies=[Depends(security.fresh_token_required())])
def sensitive_operation():
    return "You have access to this sensitive operation"
```

### Create fresh access tokens

To create `fresh` access token, use `fresh=True` argument in `FastJWT.create_access_token` method. 

On the `/login` route, we set the `fresh` argument to `True` because the token is generated after the user explicitly provided username/password combo.

```py linenums="12" hl_lines="4-7"
@app.post('/login')
def login(data: LoginForm):
    if data.username == "test" and data.password == "test":
        access_token = security.create_access_token(
            data.username, 
            fresh=True
        )
        refresh_token = security.create_refresh_token(data.username)
        return {
            "access_token": access_token, 
            "refresh_token": refresh_token
        }
    raise HTTPException(401, "Bad username/password")
```

### Refreshing tokens

When refreshing tokens, you should always generate **NOT** `fresh` tokens.
On the example below the `fresh` argument is set to `Fasle` explicitly, 
the default behavior for the `FastJWT.create_access_token` is to generate a NON `fresh` token.

```py linenums="29" hl_lines="5-8"
@app.post('/refresh')
def refresh(
    refresh_payload: TokenPayload = Depends(security.refresh_token_required())
):
    access_token = security.create_access_token(
        refresh_payload.sub, 
        fresh=False
    )
    return {"access_token": access_token}
```

### Requiring fresh tokens

The first `/protected` route acts as usual, regardless of the `fresh` token's state.

At the opposite, the `/sensitive_operation` route will now require a fresh token to be executed.
This behavior is defined by the `FastJWT.fresh_token_required` dependency

```py linenums="40" hl_lines="5-8"
@app.get('/protected', dependencies=[Depends(security.access_token_required())])
def protected():
    return "You have access to this protected resource"

@app.get('/sensitive_operation', dependencies=[Depends(security.fresh_token_required())])
def sensitive_operation():
    return "You have access to this sensitive operation"
```

=== "1. Login"

    ```shell
    # We login to obtain a fresh token
    $ curl -s -X POST --json '{"username":"test", "password":"test"}' http://0.0.0.0:8000/login
    {"access_token": $FRESH_TOKEN, "refresh_token": $REFRESH_TOKEN}
    ```
=== "2. Sensitive Operation"

    ```shell
    # We request the sensitive operation with the fresh token
    $ curl -s --oauth2-bearer $FRESH_TOKEN http://0.0.0.0:8000/sensitive_operation
    "You have access to this sensitive operation"
    ```
=== "3. Refresh access token"

    ```shell
    # We refresh the access token to get a new non fresh one
    $ curl -s --oauth2-bearer $REFRESH_TOKEN http://0.0.0.0:8000/refresh
    {"access_token": $NON_FRESH_TOKEN}
    ```
=== "4. Sensitive operation"

    ```shell
    # We request the sensitive operation with the non fresh token
    $ curl -s --oauth2-bearer $FRESH_TOKEN http://0.0.0.0:8000/sensitive_operation
    Interal server error
    ```

??? note "Note on Internal server error"

    As you might notice, the step 4 results in an 500 HTTP Internal Server Error. 
    This is the expected behavior, since error handling is by default disabled on FastJWT and should be enabled or
    handled by you to avoid errors