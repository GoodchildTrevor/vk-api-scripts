"""Custom exceptions for VK API errors."""


class VKAPIError(Exception):
    """Raised when VK API returns an error response."""

    def __init__(self, code: int, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"VK API error {code}: {message}")
