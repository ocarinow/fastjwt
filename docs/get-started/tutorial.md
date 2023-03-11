# Base Usage

```py linenums="1"
from fastapi import FastAPI, Depends
from fastjwt import FastJWT, FastJWTConfig

app = FastAPI(title="My Base App")

security_config = FJWTConfig()
security_config.JWT_ALGORITHM = "HS256"
security_config.JWT_SECRET_KEY = "SECRET_KEY"

security = FastJWT(config=security_config)

@app.get('/login')
def login(email: str, password: str):
    if email == "john.doe@fastjwt.com" and password == "abcd":
        token = security.create_access_token(uid=email)
        return {"access_token": token}
    raise fastapi.HTTPException(401, detail={"message": "Bad credentials"})

@app.get('/protected_endpoint', dependencies=[Depends(security.token_required())])
def get_protected_endpoint():
    ...
    return "This is a protected endpoint"
```

## Setup

Let's build our first FastAPI application with FastJWT

```py linenums="1"
from fastapi import FastAPI, Depends
from fastjwt import FastJWT, FastJWTConfig

app = FastAPI(title="My Base App")

security_config = FJWTConfig()
security_config.JWT_ALGORITHM = "HS256"
security_config.JWT_SECRET_KEY = "SECRET_KEY"

security = FastJWT(config=security_config)
```

### Create the FastAPI application

As usual you create your application with the `fastapi.FastAPI` object

```py linenums="1" hl_lines="1 4"
from fastapi import FastAPI, Depends
from fastjwt import FastJWT, FastJWTConfig

app = FastAPI(title="My Base App")

security_config = FJWTConfig()
security_config.JWT_ALGORITHM = "HS256"
security_config.JWT_SECRET_KEY = "SECRET_KEY"

security = FastJWT(config=security_config)
```

### Configure the JWT behavior

```py linenums="1" hl_lines="2 6-8"
from fastapi import FastAPI, Depends
from fastjwt import FastJWT, FastJWTConfig

app = FastAPI(title="My Base App")

security_config = FJWTConfig()
security_config.JWT_ALGORITHM = "HS256"
security_config.JWT_SECRET_KEY = "SECRET_KEY"

security = FastJWT(config=security_config)
```

_FastJWT_ provides a `FJWTConfig` object _(pydantic's BaseSetting)_ to customize the behavior of JWT management.
Here we choose a **symmetric** encryption algorith as `"HS256"` and we set the `SECRET_KEY` as the encoding/decoding key.

!!! info "Future release"
    So far the `FJWTConfig` creates additional code and avoidable instances. Next release will make the configuration easier and directly integrated within the `FastJWT` object

### Handle the secrets

By construction JSON Web Token are not encrypted, you can try you own JWT on [https://jwt.io/](https://jwt.io/). However, you will need a secret key for your server to sign tokens.

```py linenums="1" hl_lines="8"
from fastapi import FastAPI, Depends
from fastjwt import FastJWT, FastJWTConfig

app = FastAPI(title="My Base App")

security_config = FJWTConfig()
security_config.JWT_ALGORITHM = "HS256"
security_config.JWT_SECRET_KEY = "SECRET_KEY"

security = FastJWT(config=security_config)
```

!!! warning "Secrets location"
    As a best practice do not use explicit secrets within your code. It is recommended to use environment variables to avoid any credentials leakage
    ```py
    import os
    security_config.JWT_SECRET_KEY = os.getenv("SECRET_KEY")
    ```

### Create the FastJWT instance

```py linenums="1" hl_lines="10"
from fastapi import FastAPI, Depends
from fastjwt import FastJWT, FastJWTConfig

app = FastAPI(title="My Base App")

security_config = FJWTConfig()
security_config.JWT_ALGORITHM = "HS256"
security_config.JWT_SECRET_KEY = "SECRET_KEY"

security = FastJWT(config=security_config)
```

## Authentication

### Authenticate user

To authenticate a user we create a `/login` route the usual way with FastAPI

```py linenums="10"
security = FastJWT(config=security_config)

@app.get('/login')
def login(email: str, password: str):
    if email == "john.doe@fastjwt.com" and password == "abcd":
        token = security.create_access_token(uid=email)
        return {"access_token": token}
    raise fastapi.HTTPException(401, detail={"message": "Bad credentials"})

```

!!! example 
    The `/login` route above is a dummy example. Email/password combo should not be carried through query parameters.
    The appropriate logic should also implement deeper checks with regard to the authentication. 

    Using PIDs _(Personal Identification Data)_ should also be avoided in the JWT since its content is fully readable.

The `FastJWT` object provides a `create_access_token` method that given a unique user identifier `uid` creates a signed token.

=== "Request Access Token"

    ```shell
    $ curl -s -X POST http://0.0.0.0:8000/login?email=john.doe@fastjwt.com&password=abcd
     {"access_token": $TOKEN}
    ```


### Protected routes

Let's work on a simple `GET` route that can only be accessed by authenticated users.

```py linenums="19" hl_lines="1"
@app.get('/protected_endpoint', dependencies=[Depends(security.token_required())])
def get_protected_endpoint():
    ...
    return "This is a protected endpoint"

```

FastJWT is compliant with the FastAPI [dependency injection system](https://fastapi.tiangolo.com/tutorial/dependencies/). It provides a `FastJWT.token_required` method to enforce this behavior.

Whether we provide a bad token or no token at all, the response from the server will be a `401` HTTP Code when we request `/protected_endpoint`

=== "curl without JWT"

    ```shell
    $ curl -s http://0.0.0.0:8000/protected_endpoint
     {"detail":"Missing JWT in request"}
    ```
=== "curl with bad JWT"

    ```shell
    $ curl -s --oauth2-bearer "dummytoken" http://0.0.0.0:8000/protected_endpoint
     {"detail":"Unauthorized"}
    ```
=== "curl with good JWT"

    ```shell
    $ curl -s --oauth2-bearer $TOKEN http://0.0.0.0:8000/protected_endpoint
     "This is a protected endpoint"
    ```