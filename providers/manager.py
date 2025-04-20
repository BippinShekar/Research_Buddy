from providers.openai_provider import OpenAIProvider
from typing import Any
from openai import OpenAI
import os
from providers.base_provider import BaseProvider

def get_provider(provider: str, selected_model: str = None) -> tuple[Any, BaseProvider]:
    """
    Get the provider for the selected model.

    Args:
        provider (str): The name of the provider to use (e.g. "openai")
        selected_model (str, optional): The specific model to use. Defaults to None.

    Returns:
        tuple[Any, BaseProvider]: A tuple containing:
            - The provider client instance
            - The provider class that inherits from BaseProvider

    Raises:
        KeyError: If the specified provider is not found in the provider mapping
    """
    provider_map = {
        "openai": lambda: (OpenAI(os.getenv("OPENAI_API_KEY")), OpenAIProvider)
    }
    if provider not in provider_map:
        raise ValueError(f"Provider '{provider}' not supported. Available providers: {list(provider_map.keys())}")
    return provider_map[provider]()
