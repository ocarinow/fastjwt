# Token Blocklist

For token without expiry date, or even token are revoked, the standard JWT validation will pass. Hence the need to check if the token provided in request is revoked. Usually we confront the token with a blocklist of non-expired revoked token.

FastJWT enables this revoked token check by using a custom callback system.

```py linenums="1"
from typing import Optional
from fastapi import FastAPI, Depends
from fastjwt import FastJWT, RequestToken

app = FastAPI()

# This list mockups a store for bloked tokens
REVOKED_TOKEN = []


def is_token_revoked(token:str) -> bool:
    """Check if given token is revoked"""
    return token in REVOKED_TOKEN

security = FastJWT()
security.set_token_checker(is_token_revoked)

# We define dependency here to avoid repeated code
auth_required_dep = Depends(security.auth_required)
get_token_dep = Depends(security.get_token_from_request)

@app.get("/login")
def login():
    token = security.create_access_token(uid="john.doe@fastwt.com")
    return {"access_token": token}

@app.get("/get_token")
def get_token(token: Optional[RequestToken] = get_token_dep):
    if token is not None
        return f"Your token is: {token} and is located in {token.location}"
    else:
        return "No token found"

@app.get("/logout", dependencies=[auth_required_dep])
def logout(token: RequestToken = get_token_dep):
    REVOKED_TOKEN.append(token)
    return {"access_token": token}

@app.get("/profile", dependencies=[auth_required_dep])
def profile():
    return "You are authenticated"

```

## Setup

### Define the callback

First we need to create a function with a first `token` _str_ positional argument.
This function should return `True` is the token is considered **revoked**, `False` otherwise.

```py linenums="1" hl_lines="11-13"
from typing import Optional
from fastapi import FastAPI, Depends
from fastjwt import FastJWT, RequestToken

app = FastAPI()

# This list mockups a store for bloked tokens
REVOKED_TOKEN = []


def is_token_revoked(token:str) -> bool:
    """Check if given token is revoked"""
    return token in REVOKED_TOKEN

security = FastJWT()
security.set_token_checker(is_token_revoked)

# We define dependency here to avoid repeated code
auth_required_dep = Depends(security.auth_required)
get_token_dep = Depends(security.get_token_from_request)

@app.get("/login")
def login():
    token = security.create_access_token(uid="john.doe@fastwt.com")
    return {"access_token": token}

@app.get("/get_token")
def get_token(token: Optional[RequestToken] = get_token_dep):
    if token is not None
        return f"Your token is: {token} and is located in {token.location}"
    else:
        return "No token found"

@app.get("/logout", dependencies=[auth_required_dep])
def logout(token: RequestToken = get_token_dep):
    REVOKED_TOKEN.append(token)
    return {"access_token": token}

@app.get("/profile", dependencies=[auth_required_dep])
def profile():
    return "You are authenticated"

```

### Assign the callback

Once defined you only need to assign this callback to the `FastJWT` instance wiht the `FastJWT.set_token_checker` method

```py linenums="1" hl_lines="15-16"
from typing import Optional
from fastapi import FastAPI, Depends
from fastjwt import FastJWT, RequestToken

app = FastAPI()

# This list mockups a store for bloked tokens
REVOKED_TOKEN = []


def is_token_revoked(token:str) -> bool:
    """Check if given token is revoked"""
    return token in REVOKED_TOKEN

security = FastJWT()
security.set_token_checker(is_token_revoked)

# We define dependency here to avoid repeated code
auth_required_dep = Depends(security.auth_required)
get_token_dep = Depends(security.get_token_from_request)

@app.get("/login")
def login():
    token = security.create_access_token(uid="john.doe@fastwt.com")
    return {"access_token": token}

@app.get("/get_token")
def get_token(token: Optional[RequestToken] = get_token_dep):
    if token is not None
        return f"Your token is: {token} and is located in {token.location}"
    else:
        return "No token found"

@app.get("/logout", dependencies=[auth_required_dep])
def logout(token: RequestToken = get_token_dep):
    REVOKED_TOKEN.append(token)
    return {"access_token": token}

@app.get("/profile", dependencies=[auth_required_dep])
def profile():
    return "You are authenticated"

```

### Dependencies

To retrieve a token you can use the `FastJWT.get_token_from_request` dependency. This dependency returns a `fastjwt.RequestToken` instance if a token was detected in the request

!!! note
    The `FastJWT.get_token_from_request` dependency **does not check** the token validity, it only returns the token
    if found in request. If no token appears in the request the dependency will return a `None` value.

    If you need to ensure a token is available use this dependency in conjunction with the `FastJWT.auth_required` dependency

```py linenums="1" hl_lines="19-20"
from typing import Optional
from fastapi import FastAPI, Depends
from fastjwt import FastJWT, RequestToken

app = FastAPI()

# This list mockups a store for bloked tokens
REVOKED_TOKEN = []


def is_token_revoked(token:str) -> bool:
    """Check if given token is revoked"""
    return token in REVOKED_TOKEN

security = FastJWT()
security.set_token_checker(is_token_revoked)

# We define dependency here to avoid repeated code
auth_required_dep = Depends(security.auth_required)
get_token_dep = Depends(security.get_token_from_request)

@app.get("/login")
def login():
    token = security.create_access_token(uid="john.doe@fastwt.com")
    return {"access_token": token}

@app.get("/get_token")
def get_token(token: Optional[RequestToken] = get_token_dep):
    if token is not None
        return f"Your token is: {token} and is located in {token.location}"
    else:
        return "No token found"

@app.get("/logout", dependencies=[auth_required_dep])
def logout(token: RequestToken = get_token_dep):
    REVOKED_TOKEN.append(token)
    return {"access_token": token}

@app.get("/profile", dependencies=[auth_required_dep])
def profile():
    return "You are authenticated"

```

### Revoke a token

Once the setup is done, you can use the `FastJWT.get_token_from_request` dependency as a route dependency to get access to the `token`

```py linenums="1" hl_lines="22-41"
from typing import Optional
from fastapi import FastAPI, Depends
from fastjwt import FastJWT, RequestToken

app = FastAPI()

# This list mockups a store for bloked tokens
REVOKED_TOKEN = []


def is_token_revoked(token:str) -> bool:
    """Check if given token is revoked"""
    return token in REVOKED_TOKEN

security = FastJWT()
security.set_token_checker(is_token_revoked)

# We define dependency here to avoid repeated code
auth_required_dep = Depends(security.auth_required)
get_token_dep = Depends(security.get_token_from_request)

@app.get("/login")
def login():
    token = security.create_access_token(uid="john.doe@fastwt.com")
    return {"access_token": token}

@app.get("/get_token")
def get_token(token: Optional[RequestToken] = get_token_dep):
    if token is not None
        return f"Your token is: {token} and is located in {token.location}"
    else:
        return "No token found"

@app.get("/logout", dependencies=[auth_required_dep])
def logout(token: RequestToken = get_token_dep):
    REVOKED_TOKEN.append(token)
    return "OK"

@app.get("/profile", dependencies=[auth_required_dep])
def profile():
    return "You are authenticated"

```

!!! example
    In this example we implement a "dummy" login/logout logic. The main feature in this example is the ability to revoke a token and showcase how the protected route behave

=== "1. Get Profile"

    ```shell
    # No credential is provided
    $ curl -s http://0.0.0.0:8000/profile
     {"detail": "Unauthorized"}
    ```
=== "2. Get Token"

    ```shell
    # No token is available in request
    $ curl -s http://0.0.0.0:8000/get_token
     "No token found"
    ```
=== "3. Login"

    ```shell
    # A token is generated
    $ curl -s http://0.0.0.0:8000/login
     {"access_token": $TOKEN}
    ```
=== "4. Get Profile"

    ```shell
    # A valid token is provided
    $ curl -s --oauth2-bearer $TOKEN http://0.0.0.0:8000/profile
     "You are authenticated"
    ```
=== "5. Logout"

    ```shell
    # A valid token is provided
    $ curl -s --oauth2-bearer $TOKEN http://0.0.0.0:8000/logout
     "OK"
    ```
=== "6. Get Profile"

    ```shell
    # A revoked token is provided
    $ curl -s --oauth2-bearer $TOKEN http://0.0.0.0:8000/profile
     {"detail": "Unauthorized"}
    ```
=== "7. Get Token"

    ```shell
    # A revoked token is provided but no validation is required for /get_token
    $ curl -s --oauth2-bearer $TOKEN http://0.0.0.0:8000/get_token
     "Your token is: $TOKEN and is located in headers"
    ```


## With a database <small>(sqlalchemy)</small>

!!! warning "WIP"
    This section is work in progress