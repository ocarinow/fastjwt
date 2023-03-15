# fastjwt

<p style="text-align:center;">
<a href="https://github.com/ocarinow/fastjwt" alt="Python"><img src="https://img.shields.io/pypi/pyversions/fastjwt" alt="Python Version" /></a>
<a href="https://github.com/ocarinow/fastjwt/releases" alt="Releases"><img src="https://img.shields.io/github/v/release/ocarinow/fastjwt" alt="Latest Version" /></a>
<a href="https://github.com/ocarinow/fastjwt/blob/main/LICENSE" alt="Licence"><img src="https://img.shields.io/github/license/ocarinow/fastjwt" alt="Licence" /></a>
<a href="https://ocarinow.github.io/fastjwt/" alt="Documentation"><img src="https://img.shields.io/badge/docs-passing-brightgreen" alt="Documentation"></img></a></p>

<p style="text-align:center;">
<a href="https://github.com/ocarinow/fastjwt/actions" alt="Build Status"><img src="https://github.com/ocarinow/fastjwt/actions/workflows/python-release.yaml/badge.svg" alt="Build Status" /></a>
<a href="https://github.com/ocarinow/fastjwt/actions" alt="Test Status"><img src="https://github.com/ocarinow/fastjwt/actions/workflows/python-test.yaml/badge.svg" alt="Test Status" /></a>
<a href="https://github.com/ocarinow/fastjwt/actions" alt="Publish Status"><img src="https://github.com/ocarinow/fastjwt/actions/workflows/python-publish.yaml/badge.svg" alt="Publish Status" /></a>
<a href="https://github.com/ocarinow/fastjwt/actions" alt="Publish Status"><img src="https://github.com/ocarinow/fastjwt/actions/workflows/python-documentation.yaml/badge.svg" alt="Documentation Status" /></a></p>

<p style="text-align:center;">
<a href="https://github.com/ocarinow/fastjwt/actions" alt="Publish Status"><img src="https://raw.githubusercontent.com/ocarinow/fastjwt/main/reports/coverage-badge.svg" alt="Coverage" /></a>
<a href="https://github.com/ocarinow/fastjwt/actions" alt="Publish Status"><img src="https://raw.githubusercontent.com/ocarinow/fastjwt/main/reports/docstr-badge.svg" alt="Docstring" /></a>
<a href="https://github.com/ocarinow/fastjwt/actions" alt="Publish Status"><img src="https://raw.githubusercontent.com/ocarinow/fastjwt/main/reports/flake8-badge.svg" alt="Flake8" /></a>
<a href="https://github.com/ocarinow/fastjwt/actions" alt="Publish Status"><img src="https://raw.githubusercontent.com/ocarinow/fastjwt/main/reports/tests-badge.svg" alt="Tests" /></a></p>

<p style="text-align:center;">
<a href="https://github.com/ocarinow/fastjwt/commits" alt="Stars"><img src="https://img.shields.io/github/commit-activity/m/ocarinow/fastjwt" alt="Commit Activity" /></a>
<a href="https://github.com/ocarinow/fastjwt" alt="Repo Size"><img src="https://img.shields.io/github/repo-size/ocarinow/fastjwt" alt="Repo Size" /></a>
<a href="https://github.com/ocarinow/fastjwt" alt="Issues"><img src="https://img.shields.io/github/issues/ocarinow/fastjwt" alt="Issues" /></a>
<a href="https://github.com/ocarinow/fastjwt" alt="Pull Requests"><img src="https://img.shields.io/github/issues-pr/ocarinow/fastjwt" alt="Pull Requests" /></a>
<a href="https://github.com/ocarinow/fastjwt" alt="Downloads"><img src="https://img.shields.io/github/downloads/ocarinow/fastjwt/total" alt="Downloads" /></a>
</p>
<p style="text-align:center;">
<a href="https://github.com/ocarinow/fastjwt/stargazers" alt="Stars"><img src="https://img.shields.io/github/stars/ocarinow/fastjwt?style=social" alt="Stars" /></a>
<a href="https://github.com/ocarinow/fastjwt" alt="Forks"><img src="https://img.shields.io/github/forks/ocarinow/fastjwt?style=social" alt="Forks" /></a>
<a href="https://github.com/ocarinow/fastjwt/watchers" alt="Watchers"><img src="https://img.shields.io/github/watchers/ocarinow/fastjwt?style=social" alt="Watchers" /></a>
</p>

FastAPI Plugin for reusable JWT Authentication Management

**fastjwt** enables easy JSON Web Tokens management within your FastAPI application.

_fastjwt_ is heavily inspired from its Flask equivalent [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/stable/)

**Documentation**: [https://ocarinow.github.io/fastjwt/](https://ocarinow.github.io/fastjwt/)

## Features

- [X] Encode/Decode JWT for application Authentication
- [X] Automatic JWT detection in request
    - [X] JWT in Headers
    - [X] JWT in Cookies
    - [X] JWT in Query strings
    - [X] JWT in JSON Body
- [X] Implicit/Explicit token refresh mechanism
- [X] Freshness state of token
- [X] Route protection
    - [X] Token type based protection _(access/refresh)_
    - [X] Token freshness protection
    - [X] Partial route protection
- [X] Handle custom user logic for revoked token validation
- [X] Handle custom logic for token recipient retrieval _(ORM, pydantic serialization...)_
- [X] Provide FastAPI compliant dependency injection API
- [X] Automatic error handling

## Setup

### Requirements

FastJWT is built on top of the following dependencies:

- [FastAPI](https://github.com/tiangolo/fastapi) as web framework
- [Pydantic](https://github.com/pydantic/pydantic) as data validation
- [PyJWT](https://github.com/jpadilla/pyjwt) as python implementation of the JSON Web Token standard

FastJWT also relies on [`typing-extensions`](https://pypi.org/project/typing-extensions/) for backward compatibility _(python3.9)_

### Install

```shell
# With pip
pip install fastjwt
# With poetry
poetry add fastjwt
# With pipenv
pipenv install fastjwt
```

## Example

```py
from fastapi import FastAPI, Depends
from fastjwt import FastJWT

app = FastAPI()
security = FastJWT()

@app.get('/login')
def login():
    return security.create_access_token(uid='foo')

@app.get('/protected', dependencies=[Depends(security.access_token_required())])
def protected():
    return "This is a protected endpoint"
```

## Development

> <span style="color:orange;">**WORK IN PROGRESS**</span>
>
> The development guide is not available yet

## Contributing

> <span style="color:orange;">**WORK IN PROGRESS**</span>
>
> The contribution guide is not available yet

## License

This project is open source and under [MIT License](https://github.com/ocarinow/fastjwt/blob/main/LICENSE)
