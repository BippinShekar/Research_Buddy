from agents.ex_agent1.prompts import ROLE, TASK, INSTRUCTIONS, OUTPUT_FORMAT, EXAMPLES
from agents.ex_agent1.model import Agent1Response
from providers.manager import get_provider

def create_agent1(selected_model: str = "gpt-4o-mini"):
    """
    Create an instance of the Agent1 class.
    """
    model, Agent = get_provider(selected_model)

    return Agent(
        model=model,
        model_name=selected_model,
        agent_name="Agent1",
        role=ROLE,
        task=TASK,
        instructions=INSTRUCTIONS,
        output_format=OUTPUT_FORMAT,
        response_structure=Agent1Response,
        structured_outputs=True,
        examples=EXAMPLES)

all = ["create_agent1"]