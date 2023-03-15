# Dependency Injection

Following the FastAPI dependency injection syntax, we can use the FastJWT dependencies in multiple places

## Route

The straightforward usage is to protect a given route. Let's consider `GET /protected` as the endpoint to protect.
Depending on your need for context you might want to use FastJWT dependencies as function or route dependencies.

If you don't need to know the user/recipient/subject context _-e.g you need to display the same data to all your authenticated user regardless of who they are-_

```py
from fastapi import FastAPI
from fastapi import Depends
from fastjwt import FastJWT

app = FastAPI()
security = FastJWT()

@app.get('/protected', dependencies=[Depends(security.access_token_required)])
def protected(): # (1)!
    ...
```

1. Used as a route dependency, it does not provide any context but only enforce authentication

If the recipient context is needed in the route logic, you can pass the dependency to the function to retrieve a `TokenPayload` or a custom ORM object _(see [Custom Callbacks>User Serialization](../callbacks/user.md))_

```py
from fastapi import FastAPI
from fastapi import Depends
from fastjwt import FastJWT
from fastjwt import TokenPayload

app = FastAPI()
security = FastJWT()

@app.get('/protected')
def protected(payload: TokenPayload = Depends(security.access_token_required)): # (1)!
    ...
```

1. Used as a function dependency, the return value is available as a function argument

## Application

You can also apply dependencies at an application level. It might be useful if your application is not in charge of providing authentication token but only to protect routes.

```py
from fastapi import FastAPI
from fastapi import Depends
from fastjwt import FastJWT
from fastjwt import TokenPayload

app = FastAPI(dependencies=[Depends(security.access_token_required)]) # (1)!
security = FastJWT()

@app.get('/protected')
def protected(payload: TokenPayload = Depends(security.access_token_required)): # (2)!
    ...

@app.get('/protected/nocontext')
def protected_no_context(): # (3)!
    ...
```

1. Dependencies defined here will be applied to all the routes
2. You still need to apply the dependency if you need to access the token context in your route
3. The route is also protected but does not need context data

In the example above, all the application's routes require a valid access token.
Note that in order to get the context in the route logic you'll have to specify the required dependency.

!!! note "Note on performance"
    For routes where context is needed, it seems like the dependency is called 2 times.
    FastAPI creates a dependency graph and execute all the parent nodes from our selected dependency.
    FastAPI handles the runtime and **does not** execute the dependency multiple times.

## APIRouter

Since adding global dependencies might be too narrow. We can use `fastapi.APIRouter` to scope a selection of route to protect under a FastJWT dependency

=== "app.py"
    
    ```py title="app.py"
    from fastapi import FastAPI
    from fastjwt import FastJWT

    app = FastAPI()
    security = FastJWT()

    @app.get('/')
    def home():
        return "Hello, World!"
    ```
=== "router.py"
    
    ```py title="router.py"
    from fastapi import APIRouter
    from fastapi import Depends
    
    from app import security

    router = APIRouter(dependencies=[Depends(security.access_token_required)]) # (1)!
    
    @router.get('/protected'):
    def protected():
        return "This is a protected endpoint"
    ```

    1. You can include the dependency in the APIRouter definition

=== "main.py"
    
    ```py title="main.py"
    from app import app
    from app import security
    from router import router
    
    app.include_router(
        router, 
        dependencies=[Depends(security.access_token_required)] # (1)!
    )
    ```

    1. You can include the dependency in the APIRouter when including the router within the application instead of during router definition. This syntax is en EXCLUSIVE OR with regard to the one in `router.py`