
"""
TRUJARVIS - Model Router

Central manager for selecting and executing AI providers.
"""

from collections.abc import Iterator

from providers.base_provider import BaseProvider


class ModelRouter:

    def __init__(self):
        self.providers = {}
        self.default_provider = None

    def register_provider(
        self,
        name: str,
        provider: BaseProvider,
        make_default: bool = False,
    ):
        if not isinstance(provider, BaseProvider):
            raise TypeError(
                "Provider must implement BaseProvider."
            )

        self.providers[name] = provider

        if make_default or self.default_provider is None:
            self.default_provider = name

    def get_provider(self, name=None):
        active_name = name or self.default_provider

        if active_name not in self.providers:
            raise ValueError(
                f"Provider '{active_name}' is not registered."
            )

        return self.providers[active_name]

    def check_connection(self, provider_name=None):
        provider = self.get_provider(provider_name)
        return provider.check_connection()

    def list_models(self, provider_name=None):
        provider = self.get_provider(provider_name)
        return provider.list_models()

    def generate_response(
        self,
        messages: list,
        model: str,
        options: dict,
        provider_name=None,
    ) -> Iterator[str]:

        if not messages:
            raise ValueError(
                "Conversation messages cannot be empty."
            )

        provider = self.get_provider(provider_name)

        yield from provider.stream_chat(
            model=model,
            messages=messages,
            options=options,
        )
