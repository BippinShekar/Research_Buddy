from pathlib import Path
from openai import OpenAI

class AudioProvider():

    def __init__(self) -> None:
        pass

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
    
client = OpenAI()
speech_file_path = Path(__file__).parent / "speech.mp3"

with client.audio.speech.with_streaming_response.create(
    model="gpt-4o-mini-tts",
    voice="coral",
    input="Today is a wonderful day to build something people love!",
    instructions="Speak in a cheerful and positive tone.",
) as response:
    response.stream_to_file(speech_file_path)