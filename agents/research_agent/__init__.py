from agents.research_agent.prompts import RESEARCH_ROLE, RESEARCH_TASK, RESEARCH_INSTRUCTIONS, RESEARCH_OUTPUT_FORMAT, RESEARCH_EXAMPLES, RESEARCH_USER_INPUT
from agents.research_agent.model import ResearchAgentResponse
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
        role=RESEARCH_ROLE,
        task=RESEARCH_TASK,
        instructions=RESEARCH_INSTRUCTIONS + RESEARCH_OUTPUT_FORMAT,
        response_structure=ResearchAgentResponse,
        structured_outputs=True,
        examples=RESEARCH_EXAMPLES,
        user_input=RESEARCH_USER_INPUT
    )

all = ["create_research_agent"]