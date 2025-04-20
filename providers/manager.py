from typing import Any
from openai import OpenAI
import os
from providers.base_provider import BaseProvider
from providers.providers.openai_provider import OpenAIProvider

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
        ValueError: If the specified provider is not found in the provider mapping
    """
    provider_map = {
        "openai": (OpenAI(api_key=os.getenv("OPENAI_API_KEY")), OpenAIProvider)
    }
    if provider not in provider_map:
        raise ValueError(f"Provider '{provider}' not supported. Available providers: {list(provider_map.keys())}")
    model_client, provider_class = provider_map[provider]
    return model_client, provider_class
