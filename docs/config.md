# Configuration

FastJWT options are inspired by [vimalloc/flask-jwt-extended](https://flask-jwt-extended.readthedocs.io/en/stable/options/).

- [Configuration](#configuration)
  - [Main options](#main-options)
    - [JWT\_ACCESS\_TOKEN\_EXPIRES](#jwt_access_token_expires)
    - [JWT\_ALGORITHM](#jwt_algorithm)
    - [JWT\_DECODE\_AUDIENCE](#jwt_decode_audience)
    - [JWT\_DECODE\_ISSUER](#jwt_decode_issuer)
    - [JWT\_ENCODE\_AUDIENCE](#jwt_encode_audience)
    - [JWT\_ENCODE\_ISSUER](#jwt_encode_issuer)
    - [JWT\_PRIVATE\_KEY](#jwt_private_key)
    - [JWT\_PUBLIC\_KEY](#jwt_public_key)
    - [JWT\_REFRESH\_TOKEN\_EXPIRES](#jwt_refresh_token_expires)
    - [JWT\_SECRET\_KEY](#jwt_secret_key)
    - [JWT\_TOKEN\_LOCATION](#jwt_token_location)
  - [Header options](#header-options)
    - [JWT\_HEADER\_NAME](#jwt_header_name)
    - [JWT\_HEADER\_TYPE](#jwt_header_type)
  - [Cookie options](#cookie-options)
    - [JWT\_ACCESS\_COOKIE\_NAME](#jwt_access_cookie_name)
    - [JWT\_ACCESS\_COOKIE\_PATH](#jwt_access_cookie_path)
    - [JWT\_COOKIE\_CSRF\_PROTECT](#jwt_cookie_csrf_protect)
    - [JWT\_COOKIE\_DOMAIN](#jwt_cookie_domain)
    - [JWT\_COOKIE\_MAX\_AGE](#jwt_cookie_max_age)
    - [JWT\_COOKIE\_SAMESITE](#jwt_cookie_samesite)
    - [JWT\_COOKIE\_SECURE](#jwt_cookie_secure)
    - [JWT\_REFRESH\_COOKIE\_NAME](#jwt_refresh_cookie_name)
    - [JWT\_REFRESH\_COOKIE\_PATH](#jwt_refresh_cookie_path)
  - [CSRF options](#csrf-options)
    - [JWT\_ACCESS\_CSRF\_COOKIE\_NAME](#jwt_access_csrf_cookie_name)
    - [JWT\_ACCESS\_CSRF\_COOKIE\_PATH](#jwt_access_csrf_cookie_path)
    - [JWT\_ACCESS\_CSRF\_FIELD\_NAME](#jwt_access_csrf_field_name)
    - [JWT\_ACCESS\_CSRF\_HEADER\_NAME](#jwt_access_csrf_header_name)
    - [JWT\_CSRF\_CHECK\_FORM](#jwt_csrf_check_form)
    - [JWT\_CSRF\_IN\_COOKIES](#jwt_csrf_in_cookies)
    - [JWT\_CSRF\_METHODS](#jwt_csrf_methods)
    - [JWT\_REFRESH\_CSRF\_COOKIE\_NAME](#jwt_refresh_csrf_cookie_name)
    - [JWT\_REFRESH\_CSRF\_COOKIE\_PATH](#jwt_refresh_csrf_cookie_path)
    - [JWT\_REFRESH\_CSRF\_FIELD\_NAME](#jwt_refresh_csrf_field_name)
    - [JWT\_REFRESH\_CSRF\_HEADER\_NAME](#jwt_refresh_csrf_header_name)
  - [JSON options](#json-options)
    - [JWT\_JSON\_KEY](#jwt_json_key)
    - [JWT\_REFRESH\_JSON\_KEY](#jwt_refresh_json_key)
  - [Query options](#query-options)
    - [JWT\_QUERY\_STRING\_NAME](#jwt_query_string_name)


## Main options

### JWT_ACCESS_TOKEN_EXPIRES

`datetime.timedelta(minutes=15)`

Validity period for access tokens expressed as `datetime.timedelta`. If configured with an environment variable, describe the expiration time in seconds.

### JWT_ALGORITHM

`"HS256"`

Signing algorithm for JWTs

### JWT_DECODE_AUDIENCE

`None`

Audience claim or list of audience claims (aud) expected when decoding JWT

### JWT_DECODE_ISSUER

`None`

Issuer claim (iss) expected when decoding JWT

### JWT_ENCODE_AUDIENCE

`None`

Audience claim or list of audience claims (aud) used to create JWT

### JWT_ENCODE_ISSUER

`None`

Issuer claim (iss) used to create JWT

### JWT_PRIVATE_KEY

`None`

The secret key to encode JWT. This configuration must be set if `JWT_ALGORITHM` refers to an asymmetric algorithm.

### JWT_PUBLIC_KEY

`None`

The secret key to decode JWT. This configuration must be set if `JWT_ALGORITHM` refers to an asymmetric algorithm.

### JWT_REFRESH_TOKEN_EXPIRES

`datetime.timedelta(days=20)`

Validity period for refresh tokens expressed as `datetime.timedelta`. If configured with an environment variable, describe the expiration time in seconds.

### JWT_SECRET_KEY

`None`

The secret key to encode/decode JWT. This configuration must be set if `JWT_ALGORITHM` refers to a symmetric algorithm.

### JWT_TOKEN_LOCATION

`["headers"]`

List of `TokenLocation` to configure FastJWT where to look JWT in requests.
Avaialble options are: `headers`, `cookies`, `query`, `json`

## Header options

These parameters are only relevant if `headers` is in `JWT_TOKEN_LOCATIONS`

### JWT_HEADER_NAME

`"Authorization"`

The header name containing the JWT in request.

### JWT_HEADER_TYPE

`"Bearer"`

The header type containing the JWT in request. This parameters acts as a prefix before the token. If null, the header should only be composed of the JWT.

## Cookie options

These parameters are only relevant if `cookies` is in `JWT_TOKEN_LOCATIONS`

### JWT_ACCESS_COOKIE_NAME

`"access_token_cookie"`

Name of the cookie containing the access token

### JWT_ACCESS_COOKIE_PATH

`"/"`

Path for the access cookie

### JWT_COOKIE_CSRF_PROTECT

`True`

Enables CSRF protection when using cookies.

**THIS SHOULD ALWAYS BE SET TO `True` IN PRODUCTION**

### JWT_COOKIE_DOMAIN

`None`

Domain for cross domain cookies

### JWT_COOKIE_MAX_AGE

`None`

WIP

### JWT_COOKIE_SAMESITE

`"Lax"`

Cookie property for managing cross-site browsing.
Available options are: `None`, `Lax`, `Strict`

### JWT_COOKIE_SECURE

`True`

Enable the `Secure` property while setting cookies. Secured cookies can only be exchanged via HTTPS connection.

**THIS SHOULD ALWAYS BE SET TO `True` IN PRODUCTION**

While developing, you might set this option to `False` to test your application on localhost


### JWT_REFRESH_COOKIE_NAME

`"refresh_token_cookie"`

Name of the cookie containing the refresh token

### JWT_REFRESH_COOKIE_PATH

`"/"`

Path for the refresh cookie

## CSRF options

These parameters are only relevant if `cookies` is in `JWT_TOKEN_LOCATIONS` and `JWT_COOKIE_CSRF_PROTECT` is `True`

### JWT_ACCESS_CSRF_COOKIE_NAME

`"csrf_access_token"`

Name of the cookie containing the CSRF token.

### JWT_ACCESS_CSRF_COOKIE_PATH

`"/"`

Path for the CSRF cookie

### JWT_ACCESS_CSRF_FIELD_NAME

`"csrf_token"`

Form field name containing the CSRF token

### JWT_ACCESS_CSRF_HEADER_NAME

`"X-CSRF-TOKEN"`

Name of the header containing the CSRF token

### JWT_CSRF_CHECK_FORM

`False`

WIP

### JWT_CSRF_IN_COOKIES

`True`

When enabled, store CSRF token in additional cookie

### JWT_CSRF_METHODS

`["POST", "PUT", "PATCH", "DELETE"]`

Request methods for which CSRF checks should be performed

### JWT_REFRESH_CSRF_COOKIE_NAME

`"csrf_refresh_token"`

Name of the cookie containing the CSRF token.

### JWT_REFRESH_CSRF_COOKIE_PATH

`"/"`

Path for the CSRF cookie

### JWT_REFRESH_CSRF_FIELD_NAME

`"csrf_token"`

Form field name containing the CSRF token

### JWT_REFRESH_CSRF_HEADER_NAME

`"X-CSRF-TOKEN"`

Name of the header containing the CSRF token

## JSON options

### JWT_JSON_KEY

`"access_token"`

Key containing the access token in the JSON body

### JWT_REFRESH_JSON_KEY

`"refresh_token"`

Key containing the refresh token in the JSON body

## Query options

### JWT_QUERY_STRING_NAME

`"token"`

Query parameter name containing the JWT
