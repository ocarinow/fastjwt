# Access User

JWT authentication enables scoping an endpoint logic to a given user without an explicit reference of it. Following endpoint's names illustrate this concept:

- [ ] `/profile/{userId}`
- [x] `/profile`
- [x] `/me`

Since our JWT is carrying a `uid` for user identification, we can create scoped endpoints as follow:

```py linenums="1"
from fastapi import FastAPI, Depends
from fastjwt import FastJWT

app = FastAPI()
security = FastJWT()

@app.get("/profile", dependencies=[Depends(security.auth_required)])
def profile():
    # You cannot access the user information when
    # dependency is used in route decorator
    ...

@app.get("/me")
def profile(uid: str = Depends(security.auth_required)):
    # You can now access the user unique identifier
    user = UserObject.find_in_db(uid=uid)
    ...
```

The `FastJWT.auth_required` dependency can be used as a route dependency when the user context is not needed. 
Used as a parameter dependency, the `FastJWT.auth_required` will return the `uid` *str* property from the valid JWT. 
You can use this identifier to retrieve data from users for example.

While this method allows for providing user context to a route, it can lead to code repetition and force you to add fetching code that might be outside your route logic.

## Get authenticated user context

To avoid code repetition, FastJWT provides a **custom callback system** to retrieve automatically the user data.

```py linenums="1"
from pydantic import BaseModel
from fastapi import FastAPI, Depends
from fastjwt import FastJWT

app = FastAPI()

FAKE_DB = { # This object mockups a database
    "john.doe@fastwt.com": {
        "username": "jd",
        "name": "John Doe",
        "password": "abcd"
    }
}

class User(BaseModel):
    username: str
    name: str

def get_user_from_db(uid: str) -> User:
    return FAKE_DB.get(uid)

security = FastJWT(user_model=User)
security.set_user_getter(get_user_from_db)

@app.get("/me")
def profile(user: User = Depends(security.get_authenticated_user)):
    # You can now access the user object
    return user.dict()
```

!!! note 
    The `FastJWT.get_authenticated_user` methods depends on `FastJWT.auth_required`, to avoid multiplying the dependencies per route

    Any route having the `FastJWT.get_authenticated_user` will required a request with a valid JWT

### User serialization

FastJWT allows you to define an object that will be returned when the `FastJWT.get_authenticated_user` dependency is used

```py linenums="1" hl_lines="15-17"
from pydantic import BaseModel
from fastapi import FastAPI, Depends
from fastjwt import FastJWT

app = FastAPI()

FAKE_DB = { # This object mockups a database
    "john.doe@fastwt.com": {
        "username": "jd",
        "name": "John Doe",
        "password": "abcd"
    }
}

class User(BaseModel):
    username: str
    name: str

def get_user_from_db(uid: str) -> User:
    return FAKE_DB.get(uid)

security = FastJWT(user_model=User)
security.set_user_getter(get_user_from_db)

@app.get("/login")
def login():
    token = security.create_access_token(uid="john.doe@fastwt.com")
    return {"access_token": token}

@app.get("/me")
def profile(user: User = Depends(security.get_authenticated_user)):
    # You can now access the user object
    return user.dict()
```

Here we use a `pydantic` model but any valid Python `typing` is supported.


### Set the callback

```py linenums="1" hl_lines="19-23"
from pydantic import BaseModel
from fastapi import FastAPI, Depends
from fastjwt import FastJWT

app = FastAPI()

FAKE_DB = { # This object mockups a database
    "john.doe@fastwt.com": {
        "username": "jd",
        "name": "John Doe",
        "password": "abcd"
    }
}

class User(BaseModel):
    username: str
    name: str

def get_user_from_db(uid: str) -> User:
    return FAKE_DB.get(uid)

security = FastJWT(user_model=User)
security.set_user_getter(get_user_from_db)

@app.get("/login")
def login():
    token = security.create_access_token(uid="john.doe@fastwt.com")
    return {"access_token": token}

@app.get("/me")
def profile(user: User = Depends(security.get_authenticated_user)):
    # You can now access the user object
    return user.dict()
```

You can define any fetching function that takes a `uid` string positional parameter and returns the user context. This function can return any object if the `uid` has been found.

Use the `FastJWT.set_user_getter` method to define which accessor to use. Once defined, you can use the `FastJWT.get_authenticated_user` dependency.

!!! tip "Tip: Type Hint"
    The `FastJWT` is a Python Generic object, you can use the `user_model` init parameter to enforce the type hinting.
    Even if you use user serialization, the `user_model` parameter is not mandatory, and is not used during execution except for your custom defined accessor

    === "Hint by argument"
        ```py
        security = FastJWT(user_model=User)
        ```
    === "Hint by Generic"
        ```py
        security = FastJWT[User, ...]()
        ```
    === "Hint by Typing"
        ```py
        security: FastJWT[User, ...] = FastJWT()
        ```

### Access the user context

Once the user callback set and defined, you can use the `FastJWT.get_authenticated_user` as a function dependency to access the `User` instance

```py linenums="1" hl_lines="25-33"
from pydantic import BaseModel
from fastapi import FastAPI, Depends
from fastjwt import FastJWT

app = FastAPI()

FAKE_DB = { # This object mockups a database
    "john.doe@fastwt.com": {
        "username": "jd",
        "name": "John Doe",
        "password": "abcd"
    }
}

class User(BaseModel):
    username: str
    name: str

def get_user_from_db(uid: str) -> User:
    return FAKE_DB.get(uid)

security = FastJWT(user_model=User)
security.set_user_getter(get_user_from_db)

@app.get("/login")
def login():
    token = security.create_access_token(uid="john.doe@fastwt.com")
    return {"access_token": token}

@app.get("/me")
def profile(user: User = Depends(security.get_authenticated_user)):
    # You can now access the user object
    return user.dict()
```

=== "Login to get a token"

    ```shell
    $ curl -s http://0.0.0.0:8000/login
     {"access_token": $TOKEN}
    ```
=== "Request the user profile"

    ```shell
    $ curl -s --oauth2-bearer $TOKEN http://0.0.0.0:8000/me
     {"username": "jd", "name": "John Doe"}
    ```


## Use a SQL ORM <small>(sqlalchemy)</small>

!!! warning "WIP"
    This section is work in progress