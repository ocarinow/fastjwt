# Overview

<a href="https://github.com/ocarinow/fastjwt" alt="Python"><img src="https://img.shields.io/pypi/pyversions/fastjwt" alt="Python Version" /></a>
<a href="https://github.com/ocarinow/fastjwt/releases" alt="Releases"><img src="https://img.shields.io/github/v/release/ocarinow/fastjwt" alt="Latest Version" /></a>
<a href="https://github.com/ocarinow/fastjwt/blob/main/LICENSE" alt="Licence"><img src="https://img.shields.io/github/license/ocarinow/fastjwt" alt="Licence" /></a>

<a href="https://github.com/ocarinow/fastjwt/actions" alt="Build Status"><img src="https://github.com/ocarinow/fastjwt/actions/workflows/python-release.yaml/badge.svg" alt="Build Status" /></a>
<a href="https://github.com/ocarinow/fastjwt/actions" alt="Test Status"><img src="https://github.com/ocarinow/fastjwt/actions/workflows/python-test.yaml/badge.svg" alt="Test Status" /></a>
<a href="https://github.com/ocarinow/fastjwt/actions" alt="Publish Status"><img src="https://github.com/ocarinow/fastjwt/actions/workflows/python-publish.yaml/badge.svg" alt="Publish Status" /></a>

<a href="https://github.com/ocarinow/fastjwt/actions" alt="Publish Status"><img src="https://raw.githubusercontent.com/ocarinow/fastjwt/main/reports/coverage-badge.svg" alt="Coverage" /></a>
<a href="https://github.com/ocarinow/fastjwt/actions" alt="Publish Status"><img src="https://raw.githubusercontent.com/ocarinow/fastjwt/main/reports/docstr-badge.svg" alt="Docstring" /></a>
<a href="https://github.com/ocarinow/fastjwt/actions" alt="Publish Status"><img src="https://raw.githubusercontent.com/ocarinow/fastjwt/main/reports/flake8-badge.svg" alt="Flake8" /></a>
<a href="https://github.com/ocarinow/fastjwt/actions" alt="Publish Status"><img src="https://raw.githubusercontent.com/ocarinow/fastjwt/main/reports/tests-badge.svg" alt="Tests" /></a>

**fastjwt** enables easy JSON Web Tokens management within your FastAPI application.

_fastjwt_ is heavily inspired from its Flask equivalent [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/stable/)

## Features

- [x] Handles request for JWT in Cookies, Headers, Query Parameters and request Body
- [ ] Handles Token Blocklist via custom callbacks
- [ ] Handles User ORM via custom callbacks
- [X] Protected routes
- [X] Protected routes with fresh token/login
- [X] Implicit/Explicit Token Refresh mechanisms
- [ ] Partially protected routes

## Commands

- `mkdocs new [dir-name]` - Create a new project.
- `mkdocs serve` - Start the live-reloading docs server.
- `mkdocs build` - Build the documentation site.
- `mkdocs -h` - Print help message and exit.

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.
