# JWT Locations

JWT can be provided with request in different locations. FastJWT allows to control and configure the JWT locations via the `JWT_LOCATIONS` setting.

```py linenums="1"
from fastapi import FastAPI, Depends
from fastjwt import FastJWT, FastJWTConfig

app = FastAPI()

config = FastJWTConfig()
config.JWT_LOCATIONS = ["headers", "query", "cookies", "json"]

security = FastJWT(config=config)

@app.get('/protected', dependencies=[Depends(security.auth_required)])
def protected():
    return "OK"

```

## Headers

JWT via headers is controlled by two settings:

- `JWT_HEADER_NAME`: The header name. By default `'Authorization'`
- `JWT_HEADER_TYPE`: The header value type/prefix. By default `'Bearer'`

The FastJWT instance will check this specific header whenever it needs to retrieve a token if the `"headers"` location is in `JWT_LOCATIONS`

Authentication is only based on the presence of the `JWT_HEADER_NAME` header in the headers. To log out your user, remove the authorization header.

=== "curl"
    ```shell
    $ curl --oauth2-bearer $TOKEN http://0.0.0.0:8000/protected
     "OK"
    # OR
    $ curl -H 'Authorization: "Bearer $TOKEN"' http://0.0.0.0:8000/protected
    ```
=== "JavaScript"

    ```js
    async function requestProtectedRoute(TOKEN){
        const response = await fetch("http://0.0.0.0:8000/protected", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${TOKEN}`
            }
        })
        return response
    }
    ```
=== "Python"

    ```py
    import requests
    
    r = request.get(
        "http://0.0.0.0:8000/protected", 
        headers={
            "Authorization": f"Bearer {TOKEN}"
        }
    )
    ```

## Query Parameters

JWT via query parameters is controlled by a single setting:

- `JWT_QUERY_STRING_NAME`: The key used in the query string to identify the token. By default `'token'`

!!! warning
    It is important to remember that using JWT in query strings is **NOT** advised. Even with HTTPS protocol, the request URL is not protected, hence the token is visible.
    Such request will be saved in plain text in browsers and could be easily compromised.

    Specific cases may be of use, for example in case of one time tokens for email validation...

To use JWT in query strings you just need to suffix your URL with `?token=$TOKEN`

=== "curl"
    ```shell
    $ curl http://0.0.0.0:8000/protected?token=$TOKEN
     "OK"
    ```
=== "JavaScript"

    ```js
    async function requestProtectedRoute(TOKEN){
        const response = await fetch(`http://0.0.0.0:8000/protected?token=${TOKEN}`)
        return response
    }
    ```
=== "Python"

    ```py
    import requests
    
    r = request.get(f"http://0.0.0.0:8000/protected?token={TOKEN}")
    ```

## JSON Body

## Cookies