"""Base Example for FastJWT

In this script we create a dummy FastAPI application.

The main features showcased by this app are:
    - FastJWT Setup
    - FastJWT Base Configuration
    - FastJWT Callbacks
        - User Callback
        - Token Blacklist Callback
    - API Logic
        - Login
            - Generate an access token
        - Logout
            - Add a token to the blacklist
        - Protected Routes
        - Acessing User Object in a protected route


"""

import base64
from typing import Dict
from typing import TypedDict

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel

import fastjwt
from fastjwt import FastJWT
from fastjwt import FJWTConfig
from fastjwt import RequestToken

# ================================================================
# MOCKUP DATABASE
# ================================================================
# Here we simulate a Database containing 2 registerd users


# We define a User model as a `TypedDict`
#   Note that the user model can be any type of object you want
#   and does not need to be a BaseModel or TypedDict
class User(TypedDict):
    """Base User model for Type Annotationn"""

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

TOKEN_BLACKLIST = []

# ================================================================
# APPLICATION
# ================================================================
# We define the FastAPI as usual
app = FastAPI(title="Base FastJWT Example", version=fastjwt.__version__, debug=True)

# We then generate the configuration regarding the desired behavior or the JWT Plugin
config = FJWTConfig()
# Secure must always be set to True in Production
config.JWT_COOKIE_SECURE = False
# We use a symmetric algorithm for the example,
# please consider using asymmetric algorithm for better protection
config.JWT_ALGORITHM = "HS256"
SECRET_KEY = "Secret Key"
# We set the secret key as a base64 encoded string
config.JWT_SECRET_KEY = base64.b64encode(SECRET_KEY.encode()).decode()

# We configure the plugin to only look for JWT in Headers, Query Parameters or
# JSON Body. We removed token in cookies
config.JWT_TOKEN_LOCATION = [
    "headers",
    "query",
    "json",
]


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


# We define an accessor `(str) -> bool` that given an encoded token
# checks if the token is blacklisted
def find_token_in_blacklist(token: str) -> bool:
    """Simulate the check in a blacklisted token database

    Args:
        token (str): Encoded token

    Returns:
        bool: Whether or not the token is blacklisted
    """
    return token in TOKEN_BLACKLIST


# Once your configuration is done you can instantiate the FastJWT object
security: FastJWT[User] = FastJWT(model=User, config=config)
# We set our custom callbacks to the FastJWT object
security.set_callback_get_model_instance(get_user_from_db)
security.set_callback_token_blocklist(find_token_in_blacklist)
security.handle_errors(app)


class LoginForm(BaseModel):
    """Simulate the login form data model for the example."""

    email: str
    password: str


@app.get("/")
def home():
    """Ping route"""
    return "OK"


@app.get("/blacklist")
def blacklist():
    """Return the current token blacklist."""
    return TOKEN_BLACKLIST


@app.post("/login")
def login(data: LoginForm):
    """Login Route"""
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


@app.post("/logout", dependencies=[Depends(security.access_token_required)])
def logout(token: RequestToken = Depends(security.get_token_from_request())):
    """Logout Route"""
    # You can access the RequestToken object via the
    # `FastJWT.get_token_from_request` method
    # Note that this method returns None if no token is provided in the request
    # This dependency does not enforce the authentication requirement

    # The logic here is to blacklist the token
    TOKEN_BLACKLIST.append(token.token)
    return "OK"


# Use the FastJWT.auth_required Dependency as a route argument to protected a route
@app.get("/protected", dependencies=[Depends(security.access_token_required)])
def protected():
    """Protected Route"""
    return "You have access to this protected route"


# Use the FastJWT.get_current_user_callback Dependency as a function argument to
# retrieve the User object
@app.get("/me")
def profile(user: User = Depends(security.get_current_subject)):
    """Protected Route to get the subject information"""
    return (
        f"First Name: {user['name'].split(' ')[0]} "
        f"| Last Name: {user['name'].split(' ')[1]}"
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
