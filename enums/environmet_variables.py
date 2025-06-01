import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv(override=True)

class EnvironmentVariables(Enum):
    OPENAI_API_KEY = "OPENAI_API_KEY"
    WORKERS = "WORKERS"
    LLM_RETRY_DELAY = "LLM_RETRY_DELAY"
    SELECTED_MODEL = "SELECTED_MODEL"
    PROVIDER = "PROVIDER"
    REFERENCE_PATTERN = "REFERENCE_PATTERN"

    @property
    def value_from_env(self) -> str | None:
        return os.getenv(self.value)

    @staticmethod
    def environment_check() -> None:
        missing_vars = [
            var.name for var in EnvironmentVariables
            if not os.getenv(var.value)
        ]
        if missing_vars:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )