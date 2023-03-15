# Base Usage

FastJWT core concept relies in generating access tokens and protecting routes. The following examples demonstrates how to use FastJWT to quickly integrate those system within you FastAPI application.

```py linenums="1"
from fastapi import FastAPI
from fastapi import Depends
from fastjwt import FastJWT
from fastjwt import FJWTConfig

app = FastAPI(title="My Base App")

config = FJWTConfig()
config.JWT_ALGORITHM = "HS256"
config.JWT_SECRET_KEY = "SECRET_KEY"

security = FastJWT(config=config)

@app.get('/login')
def login(username: str, password: str):
    if username == "test" and password == "test":
        token = security.create_access_token(uid=username)
        return {"access_token": token}
    raise HTTPException(401, detail={"message": "Bad credentials"})

@app.get("/protected", dependencies=[Depends(security.access_token_required)])
def get_protected():
    ...
    return "You have access to a protected endpoint"
```

## Setup

Let's build our first FastAPI application with FastJWT

```py linenums="1"
from fastapi import FastAPI
from fastapi import Depends
from fastjwt import FastJWT
from fastjwt import FJWTConfig

app = FastAPI(title="My Base App")

config = FJWTConfig()
config.JWT_ALGORITHM = "HS256"
config.JWT_SECRET_KEY = "SECRET_KEY"

security = FastJWT(config=config)
```

### Create the FastAPI application

As usual, you create your application with the `fastapi.FastAPI` object

```py linenums="1" hl_lines="1 6"
from fastapi import FastAPI
from fastapi import Depends
from fastjwt import FastJWT
from fastjwt import FJWTConfig

app = FastAPI(title="My Base App")

config = FJWTConfig()
config.JWT_ALGORITHM = "HS256"
config.JWT_SECRET_KEY = "SECRET_KEY"

security = FastJWT(config=config)
```

### Configure the JWT behavior

```py linenums="1" hl_lines="4 8-10"
from fastapi import FastAPI
from fastapi import Depends
from fastjwt import FastJWT
from fastjwt import FJWTConfig

app = FastAPI(title="My Base App")

config = FJWTConfig()
config.JWT_ALGORITHM = "HS256"
config.JWT_SECRET_KEY = "SECRET_KEY"

security = FastJWT(config=config)
```

FastJWT provides a `FJWTConfig` object _(pydantic's BaseSetting)_ to customize the behavior of JWT management.
Here we enforce a **symmetric** encryption algorithm as `"HS256"` and we set the `SECRET_KEY` as the encoding/decoding key.

### Handle secrets

By construction, JSON Web Tokens are not encrypted, you can try your own JWT on [https://jwt.io/](https://jwt.io/).
However, you will need secrets for your server to sign tokens.

```py linenums="1" hl_lines="10"
from fastapi import FastAPI
from fastapi import Depends
from fastjwt import FastJWT
from fastjwt import FJWTConfig

app = FastAPI(title="My Base App")

config = FJWTConfig()
config.JWT_ALGORITHM = "HS256"
config.JWT_SECRET_KEY = "SECRET_KEY"

security = FastJWT(config=config)
```

!!! warning "Secrets location"
    As a best practice do not use explicit secrets within your code. It is recommended to use environment variables to avoid any credentials leakage
    ```py
    import os
    config.JWT_SECRET_KEY = os.getenv("SECRET_KEY")
    ```
!!! info "Note on Algorithm"
    For demonstration ease, we use a **symmetric** algorithm. Note that **asymmetric** algorithm offers additional layers of protection.
    `"RS256"` is the recommended algorithm when signing JWTs

### Create the FastJWT instance

You can now instantiate the `FastJWT` object with the your configuration

```py linenums="1" hl_lines="12"
from fastapi import FastAPI
from fastapi import Depends
from fastjwt import FastJWT
from fastjwt import FJWTConfig

app = FastAPI(title="My Base App")

config = FJWTConfig()
config.JWT_ALGORITHM = "HS256"
config.JWT_SECRET_KEY = "SECRET_KEY"

security = FastJWT(config=config)
```

??? tip "Loading configuration after `FastJWT.__init__`"
    The `config` argument in the `FastJWT.__init__` is optional, you can use the `FastJWT.load_config` method after
    initialisation to apply your configuration

    ```py
    config = FJWTConfig()
    config.JWT_SECRET_KEY = "SECRET_KEY"

    security = FastJWT()
    security.load_config(config)
    ```

## Authentication

### Create the access token

To authenticate a user we create a `/login` route the usual way with FastAPI.

```py linenums="14" hl_lines="4"
@app.get('/login')
def login(username: str, password: str):
    if username == "test" and password == "test":
        token = security.create_access_token(uid=username)
        return {"access_token": token}
    raise HTTPException(401, detail={"message": "Bad credentials"})
```

Once a user has provided good credentials, we use the `FastJWT.create_access_token` method to generate a signed token.
To tie the user to the token, we use the `uid` argument.

!!! info "Note on PRIVACY"
    Using PIDs _(Personal Identification Data)_ should also be avoided in the JWT since its content is fully readable.
    As a best practice `uid` should usually be a user database index _(not ordered)_. Check **UUIDs** for addtitional details.

!!! info "Note on login protection"
    The `/login` route above is a dummy example. **Credentials should not be carried through query paramaters**.
    The appropriate logic should implement deeper checks with regard to authentication.

=== "Request Access Token"

    ```shell
    $ curl -s -X POST http://0.0.0.0:8000/login?username=test&password=test
     {"access_token": $TOKEN}
    ```

### Protect a route

Let's work on a simple `GET` route that can only be accessed by authenticated users.

```py linenums="21"
@app.get("/protected", dependencies=[Depends(security.access_token_required)])
def get_protected():
    ...
    return "You have access to a protected endpoint"
```

FastJWT is compliant with the FastAPI [dependency injection system](https://fastapi.tiangolo.com/tutorial/dependencies/).
It provides a `FastJWT.access_token_required` method to enforce this behavior.

Whether we provide a bad token or no token at all, the server will forbid the route logic defined in `/protected` to be executed. 

=== "curl without JWT"

    ```shell
    $ curl -s http://0.0.0.0:8000/protected
     {"detail":"Missing JWT in request"}
    ```
=== "curl with bad JWT"

    ```shell
    $ curl -s --oauth2-bearer "dummytoken" http://0.0.0.0:8000/protected
     {"detail":"Unauthorized"}
    ```
=== "curl with good JWT"

    ```shell
    $ curl -s --oauth2-bearer $TOKEN http://0.0.0.0:8000/protected
     "You have access to a protected endpoint"
    ```

!!! failure "Default exception behavior"
    In the curl requests above a `401` HTTP Error is raised when the token is not valid.
    Without addtional setup, the expected behavior from FastJWT is an `500 Internal Server Error` HTTP Error.
    For ease of demonstration, we do not dive into error handling in this section.