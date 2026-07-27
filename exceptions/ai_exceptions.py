class AIServiceError(Exception):
    """Base exception for all AI service errors."""
    pass


class AIAuthenticationError(AIServiceError):
    """Raised when authentication with the AI provider fails."""
    pass


class AIRateLimitError(AIServiceError):
    """Raised when the AI provider rate limit is exceeded."""
    pass


class AIConnectionError(AIServiceError):
    """Raised when the AI provider cannot be reached."""
    pass


class AITimeoutError(AIServiceError):
    """Raised when the AI request times out."""
    pass    