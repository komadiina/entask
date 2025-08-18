from starlette.responses import Response


class InvalidClientResponse(Response):
    media_type = "application/json"

    def __init__(self):
        super().__init__(content={"error": "Invalid client"}, status_code=400)


class InvalidCSRFTokenResponse(Response):
    media_type = "application/json"

    def __init__(self):
        super().__init__(
            content={"error": "Possible CSRF attack, request revoked."}, status_code=400
        )


class UnauthorizedResponse(Response):
    media_type = "application/json"

    def __init__(self):
        super().__init__(content={"error": "Unauthorized"}, status_code=401)


class InvalidJWTResponse(Response):
    media_type = "application/json"

    def __init__(self):
        super().__init__(
            content={"error": "Invalid authorization token."}, status_code=401
        )


class InvalidRegistrationResponse(Response):
    status_code = 422
    media_type = "application/json"

    def __init__(self, message: str):
        super().__init__(
            {"error": "Invalid registration request." if message is None else message}
        )
