class NoAuthorizationError(Exception):
    """Exception subclass raised when no authentication token is available"""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class BadConfigurationError(Exception):
    """Exception subclass raised when unallowed FastJWTConfig arguments are provided"""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
