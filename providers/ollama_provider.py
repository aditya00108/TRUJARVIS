
"""
TRUJARVIS - Ollama Provider

Connects local Ollama models with the
unified TRUJARVIS provider architecture.
"""

from collections.abc import Iterator

import ollama

from core.config import OLLAMA_HOST
from providers.base_provider import BaseProvider


class OllamaProvider(BaseProvider):
    """Provider implementation for locally hosted Ollama models."""

    def __init__(self, host: str = OLLAMA_HOST):
        self.client = ollama.Client(host=host)

    # Check Ollama connection
    def check_connection(self):
        try:
            self.client.list()
            return True, "Ollama connected successfully."

        except Exception as error:
            return False, str(error)

    # Get locally available models
    def list_models(self):
        try:
            response = self.client.list()

            return [
                model.model
                for model in response.models
            ]

        except Exception as error:
            raise RuntimeError(
                f"Unable to retrieve Ollama models: {error}"
            ) from error

    # Generate streaming chat response
    def stream_chat(
        self,
        model: str,
        messages: list,
        options: dict,
    ) -> Iterator[str]:

        if not messages:
            raise ValueError(
                "Conversation messages cannot be empty."
            )

        try:
            stream = self.client.chat(
                model=model,
                messages=messages,
                stream=True,
                options=options,
            )

            for chunk in stream:
                content = chunk.message.content

                if content:
                    yield content

        except Exception as error:
            raise RuntimeError(
                f"Ollama Provider Error: {error}"
            ) from error
