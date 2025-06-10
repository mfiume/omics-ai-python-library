"""
Omics AI Explorer Python Library

A simple Python library for interacting with Omics AI Explorer instances.
Supports multiple networks like hifisolves.org, neuroscience.ai, and cloud.parkinsonsroadmap.org.
"""

from .client import OmicsAIClient
from .exceptions import OmicsAIError, AuthenticationError, NetworkError, ValidationError

__version__ = "0.1.0"
__all__ = ["OmicsAIClient", "OmicsAIError", "AuthenticationError", "NetworkError", "ValidationError"]