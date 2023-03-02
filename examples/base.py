from typing import Dict
from typing import TypedDict

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse

import fastjwt
from fastjwt import FastJWT
from fastjwt import FastJWTConfig
from fastjwt.payload import JWTPayload


class User(TypedDict):
    name: str
    email: str
    password: str


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


def get_user_from_db(uid: str) -> User:
    """Simulate fetching a User from a database

    Args:
        uid (str): User unique identifier

    Returns:
        User: User object
    """
    return DB.get(uid)


app = FastAPI(title="Base FastJWT Example", version=fastjwt.__version__, debug=True)

config = FastJWTConfig()
config.JWT_COOKIE_SECURE = False
config.JWT_ALGORITHM = "HS256"
config.JWT_SECRET_KEY = "SFVDSDVD"

security: FastJWT = FastJWT(user_model=User, payload_model=JWTPayload, config=config)
security.set_user_getter(get_user_from_db)


class LoginForm(BaseModel):
    email: str
    password: str


@app.get("/")
def home():
    return "OK"


@app.post("/login")
def login(data: LoginForm):
    if (not data.email) or (not data.password):
        raise HTTPException(400, detail={"message": "BAD REQUEST"})
    email = data.email
    password = data.password
    if email not in DB:
        raise HTTPException(401, detail={"message": f"User {email} does not exists"})
    indexed_user = DB[email]
    if email == indexed_user["email"] and password == indexed_user["password"]:
        token = security.create_access_token(uid=email)
        response = JSONResponse(content={"access_token": token})
        security.set_access_cookie(response=response, token=token)
        return response
    raise HTTPException(401, detail={"message": "Bad credentials"})


@app.get("/me")
def profile(user: User = Depends(security.get_current_user_callback)):
    return f"First Name: {user['name'].split(' ')[0]} | Last Name: {user['name'].split(' ')[1]}"


@app.get("/protected", dependencies=[Depends(security.auth_required)])
def protected():
    return "You have access to this protected route"
