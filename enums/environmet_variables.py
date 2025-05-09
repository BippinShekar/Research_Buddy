import os
from enum import Enum

class EnvironmentVariables(Enum):
    OPENAI_API_KEY = "OPENAI_API_KEY"
    WORKERS = "WORKERS"
    LLM_RETRY_DELAY = "LLM_RETRY_DELAY"
    SELECTED_MODEL = "SELECTED_MODEL"
    PROVIDER = "PROVIDER"
    REFERENCE_PATTERN = "REFERENCE_PATTERN"

    def value_from_env(self) -> str | None:
        return os.getenv(self.value)
