"""
Exception classes for the Omics AI Explorer library.
"""


class OmicsAIError(Exception):
    """Base exception class for Omics AI Explorer library."""
    pass


class AuthenticationError(OmicsAIError):
    """Raised when authentication fails."""
    pass


class NetworkError(OmicsAIError):
    """Raised when network requests fail."""
    pass


class ValidationError(OmicsAIError):
    """Raised when input validation fails."""
    pass