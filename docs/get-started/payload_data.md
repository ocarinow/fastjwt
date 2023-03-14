# Access Payload Data

You might need to access the data from a payload in tour route logic. Let's figure how to do this with FastJWT

FastJWT introduce a `TokenPayload` pydantic's BaseModel to handle JWT claims and operations.
When FastJWt generates a token it can be serialized to an easy to use `TokenPayload` instance.

## Storing additional data

By default the `FastJWT.create_[access|refresh]_token` methods handles the standard JWT claims. These claims are related to issue date, expiry time, issuer identity...

**TODO Add link to TokenPayload deep dive**

The only claim set by the user is contained in the `uid` parameter of these methods.

```py
token = security.create_access_token(uid="USER_UNIQUE_IDENTIFIER")
```

In specific cases, you might want to store additional information, to do so use you can add keyword arguments to this method as follow.

```py
token = security.create_access_token(uid="USER_UNIQUE_IDENTIFIER", foo="bar")
```

???+ failure "Non JSON serializable data"
    The `FastJWT.create_[access|refresh]_token` methods use the `json` package from python standard library. Therefore, additional data passed as keyword arguments must be JSON serializable.

    The snippet below will result in a `TypeError: Object of type datetime is not JSON serializable`

    ```py
    from datetime import datetime
    security.create_access_token(uid="USER_UNIQUE_IDENTIFIER", foo=datetime(2023, 1, 1, 12, 0))
    ```

## Access data in routes

JWT authentication enables scoping an endpoint logic to a given user/recipient/subject without an explicit reference to it. Following endpoint's names illustrate this concept:

- [X] `/me`
- [X] `/profile`
- [ ] `/user/{user_id}`

Since our JWT is carriying a unique identifier as `sub` claim, we can create scoped endpoint as follow.

The `FastJWT.access_token_required` dependency can be used as a route dependency when the user context is not needed. 
Used as a parameter dependency, the `FastJWT.access_token_required` will return the `TokenPayload` instance from the valid JWT.
You can use this payload to retrieve data from users for example.

While this method allows for providing user context to a route, it can lead to code repetition and force you to add fetching code that might be outside your route logic.

```py linenums="1" hl_lines="18-24"
from fastapi import FastAPI
from fastapi import Depends

from fastjwt import FastJWT
from fastjwt import TokenPayload
from fastjwt import FJWTConfig

app = FastAPI()
config = FastJWT()
config.JWT_SECRET_KEY = "SECRET_KEY"
security = FastJWT(config=config)

@app.get('/token')
def get_token():
    token = security.create_access_token(uid="USER_ID", foo="bar", age=22)
    return {"access_token": token}

@app.get('/profile')
def get_profile(payload: TokenPayload = Depends(security.access_token_required)):
    return {
        "id": payload.sub,
        "age": getattr(payload, "age"),
        "foo": getattr(payload, "foo"),
    }
```

As usual we create the `FastAPI` application and the `FastJWT` JWT manager. We also provide a `GET /token` route to generate token.

As in the previous section, we use the `FastJWT.access_token_required` dependency, but this time we use it a function dependency instead of a route dependency. Used in the route, `FastJWT.access_token_required` enforce the presence and validity of an `access` token in request. In addition, when used as function dependency, it returns a `TokenPayload` instance related to the token used in request.

Whether the `FastJWT.access_token_required` dependency is used as a function argument or a route/decorator argument, it will enforce validity of the token, resulting in an exception if the token is not genuine.

From there, you can use your `payload` object in the route logic. All the additional fields included with `FastJWT.create_[access|refresh]_token` are alos available.
