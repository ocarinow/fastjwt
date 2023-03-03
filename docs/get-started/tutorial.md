# Base Usage

## Setup

Let's build our first FastAPI application with FastJWT

```py linenums="1"
import base64
from fastapi import FastAPI, Depends
from fastjwt import FastJWT, FastJWTConfig

app = FastAPI(title="My Base App")

SECRET_KEY = "MY_SECRET_KEY"
B64_SECRET_KEY = base64.b64encode(SECRET_KEY.encode()).decode()

security_config = FastJWTConfig()
security_config.JWT_ALGORITHM = "HS256"
security_config.JWT_SECRET_KEY = B64_SECRET_KEY

security = FastJWT(config=security_config)
```

### Create the FastAPI application

As usual you create your application with the `fastapi.FastAPI` object

```py linenums="1" hl_lines="2 5"
import base64
from fastapi import FastAPI, Depends
from fastjwt import FastJWT, FastJWTConfig

app = FastAPI(title="My Base App")

SECRET_KEY = "MY_SECRET_KEY"
B64_SECRET_KEY = base64.b64encode(SECRET_KEY.encode()).decode()

security_config = FastJWTConfig()
security_config.JWT_ALGORITHM = "HS256"
security_config.JWT_SECRET_KEY = B64_SECRET_KEY

security = FastJWT(config=security_config)
```

### Handle the secrets

By construction JSON Web Token are not encrypted, you can try you own JWT on [https://jwt.io/](https://jwt.io/). However, you will need a secret key for your server to sign tokens.

```py linenums="1" hl_lines="1 7-8"
import base64
from fastapi import FastAPI, Depends
from fastjwt import FastJWT, FastJWTConfig

app = FastAPI(title="My Base App")

SECRET_KEY = "MY_SECRET_KEY"
B64_SECRET_KEY = base64.b64encode(SECRET_KEY.encode()).decode()

security_config = FastJWTConfig()
security_config.JWT_ALGORITHM = "HS256"
security_config.JWT_SECRET_KEY = B64_SECRET_KEY

security = FastJWT(config=security_config)
```

!!! warning "Base64 encoding"
    As for now, only `base64` encoded **strings** are allowed as SECRETS. Next release will allow for more flexibility and will implement automated encoding detection

### Configure the JWT behavior

```py linenums="1" hl_lines="3 10-12"
import base64
from fastapi import FastAPI, Depends
from fastjwt import FastJWT, FastJWTConfig

app = FastAPI(title="My Base App")

SECRET_KEY = "MY_SECRET_KEY"
B64_SECRET_KEY = base64.b64encode(SECRET_KEY.encode()).decode()

security_config = FastJWTConfig()
security_config.JWT_ALGORITHM = "HS256"
security_config.JWT_SECRET_KEY = B64_SECRET_KEY

security = FastJWT(config=security_config)
```

_FastJWT_ provides a `FastJWTConfig` object _(pydantic's BaseSetting)_ to customize the behavior of JWT management.
Here we choose a **symmetric** encryption algorith as `"HS256"` and we set the `SECRET_KEY` as the previously `base64` encoded string

!!! info "Future release"
    So far the `FastJWTConfig` creates additional code and avoidable instances. Next release will make the configuration easier and directly integrated within the `FastJWT` object

### Create the FastJWT instance

```py linenums="1" hl_lines="3 14"
import base64
from fastapi import FastAPI, Depends
from fastjwt import FastJWT, FastJWTConfig

app = FastAPI(title="My Base App")

SECRET_KEY = "MY_SECRET_KEY"
B64_SECRET_KEY = base64.b64encode(SECRET_KEY.encode()).decode()

security_config = FastJWTConfig()
security_config.JWT_ALGORITHM = "HS256"
security_config.JWT_SECRET_KEY = B64_SECRET_KEY

security = FastJWT(config=security_config)
```

## Authentication

### Authenticate user

To authenticate a user we create a `/login` route the usual way with FastAPI

```py linenums="14"
security = FastJWT(config=security_config)

@app.post('/login')
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

```py linenums="23" hl_lines="1"
@app.get('/protected_endpoint', dependencies=[Depends(security.auth_required)])
def get_protected_endpoint():
    ...
    return "This is a protected endpoint"

```

FastJWT is compliant with the FastAPI [dependency injection system](https://fastapi.tiangolo.com/tutorial/dependencies/). It provides a `FastJWT.auth_required` method to enforce this behavior.

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