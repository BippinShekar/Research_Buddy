from abc import ABC, abstractmethod
import time
import os
from unicodedata import normalize

class BaseProvider(ABC):
    """
    Base class for all LLM providers.
    """
    def __init__(
            self, 
            model, model_name: str, agent_name: str, 
            role: str, task: str, instructions: str, 
            structured_outputs: bool, response_structure: str, 
            user_input: str, temperature: float, examples: list = None ):
        
        self.model = model,
        self.model_name = model_name
        self.agent_name = agent_name
        self.role = role
        self.task = task
        self.instructions = instructions
        self.structured_outputs = structured_outputs
        self.response_structure = response_structure
        self.user_input = user_input
        self.temperature = temperature
        self.examples = examples

    def generate_system_prompt(self):
        """
        Generate the system prompt for the language model.

        The system prompt combines several components:
        - Role: Defines the model's role/persona
        - Task: Specifies what the model needs to accomplish
        - Instructions: Detailed steps/guidelines for the task
        - Output Format: JSON schema for structured responses (if enabled)
        - Examples: Sample interactions (if provided)

        Returns:
            str: The formatted system prompt containing all relevant components
        """
        system_prompt = (f"ROLE:\n{self.role}\n"
                         f"TASK:\n{self.task}\n"
                         f"INSTRUCTIONS:\n{self.instructions}\n"
                         )
        
        if self.response_structure:
            system_prompt += f"OUTPUT FORMAT:\nRespond with the following JSON structure:\n{self.response_structure.schema_json()}\n"

        if self.examples:
            system_prompt += f"EXAMPLES:\n{self.examples}\n"
        
        return system_prompt
    
    def generate_user_input(self, **kwargs):
        """
        Generate the user input for the language model by formatting the template with provided kwargs.
        
        This method formats the stored user input template with the provided keyword arguments.
        It also performs encoding validation to prevent any Unicode/encoding related errors.

        Args:
            **kwargs: Keyword arguments used to format the user input template.
                     These should match the placeholders in the template.

        Returns:
            str: The formatted user input string ready to be sent to the LLM.

        Raises:
            UnicodeEncodeError: If the formatted string contains invalid Unicode characters.
            KeyError: If required template placeholders are missing from kwargs.
        """
        
        normalized_template = normalize('NFKC', self.user_input).encode('ascii', 'ignore').decode('ascii')
        normalized_kwargs = {
            k: normalize('NFKC', str(v)).encode('ascii', 'ignore').decode('ascii') for k, v in kwargs.items()
        }
        
        return normalized_template.format(**normalized_kwargs)
    
    def retry_request(self, func, max_retries: int = 3, **kwargs):
        """
        Retry a failed request with exponential backoff.

        Args:
            func: The function to retry
            max_retries (int, optional): Maximum number of retry attempts. Defaults to 3.
            **kwargs: Additional keyword arguments passed to the function.

        Returns:
            The result of the successful function call.

        Raises:
            Exception: If max retries are exceeded without a successful call.
        """
        for _ in range(max_retries):
            try:
                return func(**kwargs)
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(os.getenv("LLM_RETRY_DELAY", 3))
        raise Exception("Max retries exceeded")
    
    @abstractmethod
    def generate_response(self, attempt: int = 1, max_retries: int = 3, **kwargs):
        """
        Generate the response from the LLM.
        """
        pass
    
    