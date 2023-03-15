# User Serialization

JSON Web Tokens main purpose is authentication. While it can carry data as described in [**Access Payload Data**](./../get-started/payload_data.md), you should avoid adding to much additional data and **ABSOLUTELY** avoid storing sensitive information in the JWT Payload.

Usually, JWT should carry a user/recipient/subject identifier used to retrieve required data about the user/recipient/subject.

Given the `FastJWT.access_token_required` dependency described in [**Access Payload Data**](./../get-started/payload_data.md), you could retrieve the `TokenPayload` instance and read its `sub` claim to retrieve data from the current user. While this solution works, it increases code repetition, its error prone and it adds additional code not serving the route logic.

To avoid code repetition, FastJWT provides a **custom callback system** to retrieve automatically the user data.

## Get authenticated user context

```py linenums="1"
from fastapi import FastAPI
from fastapi import Depends
from fastapi import FastJWT
from pydantic import BaseModel

# === USER STORE
# The FAKE_DB dictionary is a mockup for
# a user table
FAKE_DB = {
    "john.doe@ocarinow.com": {
        "email": "john.doe@ocarinow.com",
        "password": "test",
        "firstname": "John",
        "lastname": "Doe"
    }
}
# === END USER STORE

# === MODELS
class User(BaseModel):
    email: str
    password: str
    firstname: str
    lastname: str

class LoginForm(BaseModel):
    email: str
    password: str
# === END MODELS


app = FastAPI()
security = FastJWT(model=User)

@security.set_callback_get_model_instance
def get_user_from_uid(uid: str) -> User:
    return User.parse_obj(FAKE_DB[uid])

@app.post('/login')
async def login(data: LoginForm):
    if FAKE_DB.get(data.email) is None:
        raise HTTPException(401, "Bad email/password")
    
    if FAKE_DB.get(data.email)["password"] == data.password:
        access_token = security.create_access_token(data.email)
        return {"access_token": access_token}
    
    raise HTTPException(401, "Bad email/password")

@app.get('/whoami')
async def whoami(user: User = Depends(security.get_current_subject)):
    return f"""You are:
    Firstname: {user.firstname}
    Lastname: {username.lastname}"""
```

### Serialization

Let's consider you have a user store in a form of a database. When a user authenticates itself with a JWT,
you want to be able to retrieve data related to this user stored in your table.

!!! example
    The snippet below simulates a database. It contains information about users

    ```py linenums="6"
    # === USER STORE
    # The FAKE_DB dictionary is a mockup for
    # a user table
    FAKE_DB = {
        "john.doe@ocarinow.com": {
            "email": "john.doe@ocarinow.com",
            "password": "test",
            "firstname": "John",
            "lastname": "Doe"
        }
    }
    # === END USER STORE
    ```

#### Create the User object mapper

First, we create a `pydantic.BaseModel` as an object mapper to describe a `User`. Note that any default python `typing` is also accepted.

```py linenums="19" hl_lines="2-6"
# === MODELS
class User(BaseModel):
    email: str
    password: str
    firstname: str
    lastname: str

class LoginForm(BaseModel):
    email: str
    password: str
# === END MODELS
```

#### Adding Type hints to FastJWT

`FastJWT` is a Generic class, providing explicit type hint for the `model` argument is a good practice for development purposes.

```py linenums="32" hl_lines="2"
app = FastAPI()
security = FastJWT(model=User) # (1)!

@security.set_callback_get_model_instance
def get_user_from_uid(uid: str) -> User:
    return User.parse_obj(FAKE_DB[uid])
```

1.  You can provide type hints with multiple syntax

    === "Hint by argument"
        ```py
        security = FastJWT(model=User)
        ```
    === "Hint by Generic"
        ```py
        security = FastJWT[User]()
        ```
    === "Hint by Typing"
        ```py
        security: FastJWT[User] = FastJWT()
        ```

!!! tip "Tip: Type Hint"
    The `FastJWT` is a Python Generic object, you can use the `model` init parameter to enforce the type hinting.
    Even if you use user serialization, the `model` parameter is not mandatory, and is not used during execution except for your custom defined accessor

    === "Hint by argument"
        ```py
        security = FastJWT(model=User)
        ```
    === "Hint by Generic"
        ```py
        security = FastJWT[User]()
        ```
    === "Hint by Typing"
        ```py
        security: FastJWT[User] = FastJWT()
        ```

#### Declare the custom callback for user retrieval

Since fetching user/recipient/subject data depends on your application logic, FastJWT provides a `FastJWT.set_callback_get_model_instance` decorator to assign a custom callback.

We define the `get_user_from_uid` callback as a function taking `uid` as a main *str* positional arguemnt and returning the appropriate object for the given `uid`

**TYPE** `Callable[[str, ParamSpecKwargs], User]` or `(str) -> User`

```py linenums="32" hl_lines="4-6"
app = FastAPI()
security = FastJWT(model=User)

@security.set_callback_get_model_instance
def get_user_from_uid(uid: str) -> User:
    return User.parse_obj(FAKE_DB[uid])
```

!!! tip "Setting Callback syntax"
    You can set callbacks with the `FastJWT` decorator syntax, but the following method call would also work
    ```py
    def get_user_from_uid(uid: str) -> User:
        return User.parse_obj(FAKE_DB[uid])

    security = FastJWT(model=User)
    security.set_callback_get_model_instance(get_user_from_uid)
    ```

??? abstract "Feature Proposal - Decorator Naming"
    The verbosity of `FastJWT.set_callback_get_model_instance` might encourage us to add shorter aliases in next releases

### Get User Context

Once the user getter callback is set, you can use the `FastJWT.get_current_subject` to obtain the parsed ORM instance. `FastJWT.get_current_subject` is also dependent on `FastJWT.access_token_required` and therefore it enforces token validation without additional dependency declaration.

```py linenums="50" hl_lines="2"
@app.get('/whoami')
async def whoami(user: User = Depends(security.get_current_subject)):
    return f"""You are:
    Firstname: {user.firstname}
    Lastname: {username.lastname}"""
```

From the `whoami` function dependency you can access the `User` instance directly and use it without having to fetch the object inside the route logic.

??? abstract "Feature Proposal - Dependency Naming"
    `FastJWT.get_current_subject` might not be explicit enough and aliases might be added in next releases

=== "Login to get a token"

    ```shell
    $ curl -X POST -s \
        --json '{"email":"john.doe@ocarinow.com", "password":"test"}'\
        http://0.0.0.0:8000/login
    {"access_token": $TOKEN}
    ```
=== "Request the user profile"

    ```shell
    $ curl -s --oauth2-bearer $TOKEN http://0.0.0.0:8000/whoami
    You are:
        Firstname: John
        Lastname: Doe
    ```

## Use a SQL ORM <small>(sqlalchemy)</small>

!!! warning "WIP"
    This section is work in progress