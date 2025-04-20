from providers.base_provider import BaseProvider
from pydantic import ValidationError
import traceback
from openai import BadRequestError

class OpenAIProvider(BaseProvider):    
    def generate_response(self, attempt: int = 1, max_retries: int = 3, **kwargs):
        """Generate a response from the OpenAI API.

        Args:
            attempt (int, optional): Current attempt number for retries. Defaults to 1.
            max_retries (int, optional): Maximum number of retry attempts. Defaults to 3.
            **kwargs: Additional keyword arguments passed to generate_user_input.

        Returns:
            If structured_outputs is True:
                response_structure: A validated Pydantic model matching the defined schema
            If structured_outputs is False:
                tuple: (
                    str: Raw response content,
                    int: Number of prompt tokens used,
                    int: Number of completion tokens used, 
                    int: Total tokens used,
                    float: Response time in seconds
                )

        Raises:
            Exception: If validation fails, max retries exceeded, or other API errors occur
        """

        try:

            system_prompt = self.generate_system_prompt()
            user_input = self.generate_user_input(**kwargs)

            response = self.model.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt}, 
                    {"role": "user", "content": user_input}
                    ],
                response_format = self.response_structure,
                temperature = self.temperature,
            )

            response_content = response.choices[0].message.content
            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens
            total_tokens = response.usage.total_tokens  
            response_time = response.choices[0].message.response_time

            if self.structured_outputs:
                try:
                    structured_response = self.response_structure.model_validate_json(response_content)
                    return structured_response, prompt_tokens, completion_tokens, total_tokens, response_time
                except ValidationError as e:
                    raise Exception(f"JSON response: {e} Dosen't match the expected schema")
                
            return response_content, prompt_tokens, completion_tokens, total_tokens, response_time
        
        except BadRequestError as e:

            error_message = e.__str__()
            if "context_length" in error_message or "string too long" in error_message:
                if attempt < max_retries:
                    return self.retry_request(self.generate_response, attempt + 1, max_retries, **kwargs)
                else:
                    print(traceback.format_exc())
                    raise Exception("Max attempts reached")
            else:
                print(traceback.format_exc())
                raise Exception(error_message)
            
        except Exception as e:
            if attempt < max_retries:
                return self.retry_request(self.generate_response, attempt + 1, max_retries, **kwargs)
            else:
                print(traceback.format_exc())
                raise Exception(e)
            