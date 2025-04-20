from agents.research_agent import create_research_agent
from helpers.loggers import get_logger
import os

logger = get_logger()

def research_service(query: str, data: str, provider: str = None, selected_model: str = None):
    """Research service function that processes queries using an AI research agent.

    Args:
        query (str): The user's research query or question
        data (str): The context or data to analyze
        provider (str, optional): The AI provider to use. Defaults to environment variable or 'openai'
        selected_model (str, optional): The specific model to use. Defaults to environment variable or 'gpt-4o-mini'

    Returns:
        str: The answer/response from the research agent

    Raises:
        Exception: If there is an error during processing
    """
    try:
        selected_model = os.getenv("SELECTED_MODEL", "gpt-4o-mini") if selected_model is None else selected_model
        provider = os.getenv("PROVIDER", "openai")
        research_agent = create_research_agent(provider = provider, selected_model = selected_model)
        response_json, prompt_tokens, completion_tokens, total_tokens, response_time = research_agent.generate_response(query = query, data = data)

        reason = response_json.reasoning
        answer = response_json.answer

        logger.info(f"Reason: {reason}")
        logger.info(f"Prompt Tokens: {prompt_tokens}")
        logger.info(f"Completion Tokens: {completion_tokens}")
        logger.info(f"Total Tokens: {total_tokens}")
        logger.info(f"Response Time: {response_time}")

        return answer
    except Exception as e:
        logger.error(f"Error in research service: {e}")
        raise e