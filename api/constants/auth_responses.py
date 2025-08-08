from starlette.responses import Response


class InvalidClientResponse(Response):
    status_code = 400
    media_type = "application/json"

    def __init__(self):
        super().__init__({"error": "Invalid client"})


class InvalidCSRFTokenResponse(Response):
    status_code = 400
    media_type = "application/json"

    def __init__(self):
        super().__init__({"error": "Possible CSRF attack, request revoked."})


class UnauthorizedResponse(Response):
    status_code = 401
    media_type = "application/json"

    def __init__(self):
        super().__init__({"error": "Unauthorized"})


class InvalidJWTResponse(Response):
    status_code = 401
    media_type = "application/json"

    def __init__(self):
        super().__init__({"error": "Invalid authorization token."})


class InvalidRegistrationResponse(Response):
    status_code = 422
    media_type = "application/json"

    def __init__(self, message: str):
        super().__init__(
            {"error": "Invalid registration request." if message is None else message}
        )
