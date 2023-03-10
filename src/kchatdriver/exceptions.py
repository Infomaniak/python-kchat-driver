from requests import HTTPError


class InvalidOrMissingParameters(HTTPError):
    """
    Raised when kChat returns a
    400 Invalid or missing parameters in URL or request body
    """


class NoAccessTokenProvided(HTTPError):
    """
    Raised when kChat returns a
    401 No access token provided
    """


class NotEnoughPermissions(HTTPError):
    """
    Raised when kChat returns a
    403 Do not have appropriate permissions
    """


class ResourceNotFound(HTTPError):
    """
    Raised when kChat returns a
    404 Resource not found
    """


class MethodNotAllowed(HTTPError):
    """
    Raised when kChat returns a
    405 Method Not Allowed
    """


class ContentTooLarge(HTTPError):
    """
    Raised when kChat returns a
    413 Content too large
    """


class FeatureDisabled(HTTPError):
    """
    Raised when kChat returns a
    501 Feature is disabled
    """
