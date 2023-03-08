# Installation

## from package manager <small>(prefered)</small>

=== "pip"

    ```shell
    pip install fastjwt
    ```
=== "poetry"

    ```shell
    poetry add fastjwt
    ```
=== "pipenv"

    ```shell
    pipenv install fastjwt
    ```

_fastjwt_ is compatible with Python 3.9+. The current dependencies are `pydantic` and `pyjwt[crypto]`.

!!! note

    The `pyjwt[crypto]` will be switched to `pyjwt` to avoid adding the `cryptography` library if not needed. Next release should allow for `pip install fastjwt[crypto]`

## from repository

=== "pip"

    ```
    pip install git+git://github.com/ocarinow/fastjwt.git@[branch]#egg=fastjwt
    ```
=== "poetry"

    ```
    poetry add https://github.com/ocarinow/fastjwt.git
    ```
=== "pipenv"

    ```
    pipenv install git+https://github.com/ocarinow/fastjwt.git@[branch]#egg=fastjwt
    ```

## from GitHub

=== "https"

    ```shell
    git clone https://github.com/ocarinow/fastjwt.git
    ```
=== "ssh"

    ```shell
    git clone git@github.com:ocarinow/fastjwt.git
    ```
=== "GitHub CLI"

    ```shell
    gh repo clone ocarinow/fastjwt
    ```
