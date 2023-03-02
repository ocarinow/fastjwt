from typing import Dict
from typing import TypedDict

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel

import fastjwt
from fastjwt import FastJWT
from fastjwt import FastJWTConfig

# ================================================================
# MOCKUP DATABASE
# ================================================================
# Here we simulate a Database containing 2 registerd users


# We define a User model as a `TypedDict`
#   Note that the user model can be any type of object you want
#   and does not need to be a BaseModel or TypedDict
class User(TypedDict):
    name: str
    email: str
    password: str


# We populate a fake user database as a python dictionary
#   Keys represent User ID (here user's email)
#   Value represent the User Object model to be returned
DB: Dict[str, User] = {
    "john.doe@test.com": {
        "name": "John Doe",
        "password": "abcd",
        "email": "john.doe@test.com",
    },
    "tony.stark@test.com": {
        "name": "Tony Stark",
        "password": "hello",
        "email": "tony.stark@test.com",
    },
}

# ================================================================
# APPLICATION
# ================================================================
# We define the FastAPI as usual
app = FastAPI(title="Base FastJWT Example", version=fastjwt.__version__, debug=True)

# We then generate the configuration regarding the desired behavior or the JWT Plugin
config = FastJWTConfig()
config.JWT_COOKIE_SECURE = False  # Secure must always be set to True in Production
config.JWT_ALGORITHM = "HS256"  # We use a symmetric algorithm for the example, please consider using asymmetric algorithm for better protection
config.JWT_SECRET_KEY = "Secret Key"  # We set the string to be used as a secret key
config.JWT_LOCATIONS = [
    "headers",
    "query",
    "json",
]  # We configure the plugin to only look for JWT in Headers, Query Parameters or JSON Body. We removed token in cookies


# We define an accessor `(str) -> User` that given a unique user identifier
# returns an instance of the User Model Object
def get_user_from_db(uid: str) -> User:
    """Simulate fetching a User from a database

    Args:
        uid (str): User unique identifier

    Returns:
        User: User object
    """
    return DB.get(uid)


# Once your configuration is done you can instantiate the FastJWT object
security: FastJWT = FastJWT(user_model=User, config=config)
# We set our custom callback to the FastJWT object
security.set_user_getter(get_user_from_db)


class LoginForm(BaseModel):
    email: str
    password: str


@app.get("/")
def home():
    return "OK"


@app.post("/login")
def login(data: LoginForm):
    # FastJWT is not a validation tool or database management library
    # Therefore you'll need to implement the login/logout logic on
    # your own. The code below is a dummy example for the login logic

    # Check if the data is available in the request
    if (not data.email) or (not data.password):
        raise HTTPException(400, detail={"message": "BAD REQUEST"})

    email = data.email
    password = data.password

    # Check if the user exists in the database
    if email not in DB:
        raise HTTPException(401, detail={"message": f"User {email} does not exists"})

    # Check if the email/password tuple is valid
    if email == DB[email]["email"] and password == DB[email]["password"]:
        # Once all check are done.
        # Generate an access token with the `FastJWT.create_access_token` method
        token = security.create_access_token(uid=email)
        return {"access_token": token}
    raise HTTPException(401, detail={"message": "Bad credentials"})


# Use the FastJWT.auth_required Dependency as a route argument to protected a route
@app.get("/protected", dependencies=[Depends(security.auth_required)])
def protected():
    return "You have access to this protected route"


# Use the FastJWT.get_current_user_callback Dependency as a function argument to retrieve the User object
@app.get("/me")
def profile(user: User = Depends(security.get_current_user_callback)):
    return f"First Name: {user['name'].split(' ')[0]} | Last Name: {user['name'].split(' ')[1]}"
