# JWT Locations

JWT can be provided with request in different locations. FastJWT allows to control and configure the JWT locations via the `JWT_TOKEN_LOCATION` setting.

```py linenums="1"
from fastapi import FastAPI
from fastapi import Depends
from fastjwt import FastJWT
from fastjwt import FJWTConfig

app = FastAPI()

config = FJWTConfig()
config.JWT_TOKEN_LOCATION = ["headers", "query", "cookies", "json"]

security = FastJWT(config=config)

@app.get('/protected', dependencies=[Depends(security.access_token_required)])
def protected():
    return "OK"

```

## Headers

JWT via headers is controlled by two settings:

- `JWT_HEADER_NAME`: The header name. By default `'Authorization'`
- `JWT_HEADER_TYPE`: The header value type/prefix. By default `'Bearer'`

The FastJWT instance will check this specific header whenever it needs to retrieve a token if the `"headers"` location is in `JWT_TOKEN_LOCATION`

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

JWT via JSON Body is controlled by the following parameters:

- `JWT_JSON_KEY`: The json key relative to the access token. By default `access_token`
- `JWT_REFRESH_JSON_KEY`: The json key relative to the refresh token. By default `refresh_token`

Please note that sending JWT via JSON Body cannot be accomplished with GET requests, and require the `Content-Type: application/json` header.

=== "curl"

    ```shell
    curl -X POST -s --json '{"access_token":"$TOKEN"}' http://0.0.0.0:8000/protected
     "OK"
    ```
=== "JavaScript"

    ```js
    async function requestProtectedRoute(TOKEN){
        const response = await fetch("http://0.0.0.0:8000/protected", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: {
                "access_token": TOKEN
            }
        })
        return response
    }
    ```
=== "Python"

    ```py
    import requests
    
    r = request.post(
        "http://0.0.0.0:8000/protected", 
        data={
            "access_token": TOKEN
        }
    )
    ```

## Cookies

JWT via Cookies is controlled by the following parameters:

- `JWT_ACCESS_COOKIE_NAME`: Cookie name containing the access token. By default `access_token_cookie`
- `JWT_ACCESS_COOKIE_PATH`: Path of the access token cookie. By default `/`
- `JWT_COOKIE_CSRF_PROTECT`: Enable CSRF protection for cookie authentication. By default `True`
- `JWT_COOKIE_DOMAIN`: The domain for cookies set by FastJWT. By default `None`
- `JWT_COOKIE_MAX_AGE`: Max age for cookies set by FastJWT. By default `None`
- `JWT_COOKIE_SAMESITE`: The SameSite property for cookies set by FastJWT. By default `Lax`
- `JWT_COOKIE_SECURE`: Enable Cookie Secure property. By default `True`
- `JWT_REFRESH_COOKIE_NAME`: Cookie name containing the refresh token. By default `refresh_token_cookie`
- `JWT_REFRESH_COOKIE_PATH`: Path of the refresh token cookie. By default `/`
- `JWT_ACCESS_CSRF_COOKIE_NAME`: Cookie name containing the access CSRF token. By default `csrf_access_token`
- `JWT_ACCESS_CSRF_COOKIE_PATH`: Path of the access CSRF token cookie. By default `/`
- `JWT_CSRF_IN_COOKIES`: Add CSRF tokens when cookies are set by FastJWT. By default `True`
- `JWT_REFRESH_CSRF_COOKIE_NAME`: Cookie name containing the refresh CSRF token. By default `csrf_refresh_cookie`
- `JWT_REFRESH_CSRF_COOKIE_PATH`: Path of the refresf CSRF token cookie. By default `/`

If you develop an API to be consumed by a front end application _(on web browser)_. Cookies are an efficient way to provide authentication.

!!! info "Note on HTTP Only"
    `access` & `refresh` tokens set in cookies are `HTTP Only`. Meaning they cannot be accessed by JavaScript on client side. This property of `[access|refresh]` token cookies is hard coded and is not configurable. This is the expected behavior for authentication through Cookies to avoid XSS <small>(Cross Site Scripting)</small> attacks.

    See [Cross-site scripting (XSS)](https://developer.mozilla.org/en-US/docs/Glossary/Cross-site_scripting)

!!! info "Note on Secure"
    `Secure` cookie property requires an **HTTPS** request to send the secure cookie. The `JWT_COOKIE_SECURE` parameter should **always** be `True` in production. It is set as a configurable parameter for ease of development.

While JWTs in cookies are suitable for web application authentication, they require additional work to prevent attacks. One of the most common attack on cookies is [Cross Site Request Forgery (CSRF)](https://developer.mozilla.org/en-US/docs/Glossary/CSRF).

To prevent such CSRF attacks, FastJWT provides double submit CSRF token when setting cookies. The idea is to add a second layer of validation. The CSRF prevention workflow can be summarized as followed:

1. **Login**
      - When you log in into your account, the server adds a `Set-Cookie` header for your `access` token.
        This cookie is `Secure` and `HTTP Only`, meaning it cannot be read by JavaScript. 
        This token is the base64 encoded JWT signed with your secrets and contains a `csrf` claim with a UUID.
      - Besides the access token, the server adds another `Set-Cookie` header for the CSRF token.
        This CSRF cookie does not have the `HTTP Only` property and can be read by client-side JavaScript.
2. **Client-Side request**
      - When a request is made by the client-side, the request headers should include the CSRF double dubmit token.
        If not, the server will invalidate the request and produce a `CSRFError`.
        If the CSRF token provided does not match the JWT `csrf` claim, the server will invalidate the request.

This workflow prevents CSRF attacks because you need to pass explicitly the CSRF token in your request headers _(which is not a default behavior)_ and JavaScript from another domain will not have read access to this CSRF cookie.

=== "curl"

    ```shell
    curl -X POST -s --cookie "access_token_cookie=$TOKEN" -H 'X-CSRF-TOKEN: "$CSRF_TOKEN"' http://0.0.0.0:8000/protected
    "OK"
    ```
=== "JavaScript"

    ```js
    function getCookie(cname) {
        let name = cname + "=";
        let ca = document.cookie.split(';');
        for(let i = 0; i < ca.length; i++) {
            let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
        }
        return "";
    }

    function getCSRFCookie() {
        return getCookie("csrf_access_token")
    }

    async function requestProtectedRoute(){
        const response = await fetch("http://0.0.0.0:8000/protected", {
            method: "POST",
            credentials: 'include'
            headers: {
                "X-CSRF-TOKEN": getCSRFCookie()
            },
        })
        return response
    }
    ```
=== "Python"

    ```py
    import requests
    
    r = request.post(
        "http://0.0.0.0:8000/protected", 
        headers= {
            "X-CSRF-TOKEN": CSRF_TOKEN
        },
        cookies={
            "access_token_cookie": TOKEN,
        }
    )
    ```