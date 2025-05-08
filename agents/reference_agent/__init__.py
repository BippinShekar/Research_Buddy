from agents.reference_agent.prompts import (
    REFERENCE_ROLE,
    REFERENCE_INSTRUCTIONS,
    REFERENCE_OUTPUT_FORMAT,
    REFERENCE_TASK,
    REFERENCE_USER
    
)
from agents.reference_agent.model import ReferenceScoutingAgent
from providers.manager import get_provider

def create_research_agent(provider: str = "openai", selected_model: str = "gpt-4o-mini"):
    """
    Create an instance of the Research Agent class.
    """
    model, Agent = get_provider(provider=provider, selected_model=selected_model)

    return Agent(
        model=model,
        model_name=selected_model,
        agent_name="Research Agent",
        role=REFERENCE_ROLE,
        task=REFERENCE_TASK,
        instructions=REFERENCE_INSTRUCTIONS + REFERENCE_OUTPUT_FORMAT,
        response_structure=ReferenceScoutingAgent,
        structured_outputs=True,
        examples="",
        user_input=REFERENCE_USER
    )

all = ["create_reference_agent"]