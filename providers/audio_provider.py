from pathlib import Path
from openai import OpenAI
import base64

class AudioProvider():

    def __init__(self, model: str, model_name: str, agent_name: str, role: str, task: str, instructions: str, user_input: str, temperature: float = 0, examples: list = None) -> None:
        self.model = model
        self.model_name = model_name
        self.agent_name = agent_name
        self.role = role
        self.task = task
        self.instructions = instructions
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
        
        system_prompt += "OUTPUT:\nRespond in a humane way, with a clear and concise answer."
        
        return system_prompt
    
    def generate_audio(self, prompt: str):
        """
        Generate audio from the LLM, with the given prompt as input. 

        Args:
            prompt (str): The prompt to generate audio from.

        Returns:
            str: The path to the generated audio file.
        """

        audio_output = self.model.chat.completions.create(
            model="gpt-4o-audio-preview",
            modalities=["text", "audio"],
            audio={"voice": "alloy", "format": "wav"},
            messages=[
                {
                    "role": "system",
                    "content": self.generate_system_prompt()
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        wav_bytes = base64.b64decode(audio_output.choices[0].message.audio.data)

        return wav_bytes