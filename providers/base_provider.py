
"""
TRUJARVIS - Base AI Provider

Defines the common interface that all AI providers
must implement.
"""

from abc import ABC, abstractmethod
from collections.abc import Iterator


class BaseProvider(ABC):
    """Abstract interface for AI model providers."""

    @abstractmethod
    def check_connection(self):
        """Check whether the provider is available."""
        pass

    @abstractmethod
    def list_models(self):
        """Return the models available from this provider."""
        pass

    @abstractmethod
    def stream_chat(
        self,
        model: str,
        messages: list,
        options: dict,
    ) -> Iterator[str]:
        """Generate a streaming chat response."""
        pass
