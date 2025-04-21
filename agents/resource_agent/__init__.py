from agents.resource_agent.prompts import (
    RESOURCE_ROLE, 
    RESOURCE_TASK, 
    RESOURCE_INSTRUCTIONS, 
    RESOURCE_OUTPUT_FORMAT, 
    RESOURCE_USER_INPUT
)
from agents.resource_agent.model import ResourceAgentResponse
from providers.manager import get_provider

def understand_resource_agent(provider: str = "openai", selected_model: str = "gpt-4o-mini"):
    """
    Create an instance of the Resource Agent class.
    """
    model, Agent = get_provider(provider=provider, selected_model=selected_model)

    return Agent(
        model=model,
        model_name=selected_model,
        agent_name="Resource Agent",
        role=RESOURCE_ROLE,
        task=RESOURCE_TASK,
        instructions=RESOURCE_INSTRUCTIONS + RESOURCE_OUTPUT_FORMAT,
        response_structure=ResourceAgentResponse,
        structured_outputs=True,
        examples=None,
        user_input=RESOURCE_USER_INPUT
    )

all = ["understand_resource_agent"]