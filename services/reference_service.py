from agents.reference_agent import create_research_agent #noqa
from helpers.loggers import get_logger
from helpers.helpers import PDFProcessor
from typing import Dict, Any
import traceback

logger = get_logger()

def source_reference_content(path: str):
    """
    Extract reference hyperlinks from a given PDF file using the PDFProcessor.

    Args:
        path (str): The file path to the PDF document.

    Returns:
        list: A list of extracted references (typically hyperlinks) from the PDF, or None if an error occurs.
    """
    try:
        
        pdf_processor = PDFProcessor()
        extracted_references = pdf_processor.extract_references(path)

        return extracted_references 

    except Exception as e:
        logger.error(f"An error {e} occurred during reference scouting.\More Details: {traceback.format_exc()}")
    return 

def encapsulate_references(provider: str, selected_model: Any, pdf_content ,hyperlink_content: Dict[str, str]):
    """
    Generate summarized or encapsulated references from extracted hyperlinks and PDF content using a research agent.

    Args:
        provider (str): The provider used for the model (e.g., OpenAI, Anthropic).
        selected_model (Any): The specific model to be used for generating responses.
        pdf_content (Any): The main textual content extracted from the PDF.
        hyperlink_content (Dict[str, str]): A dictionary of hyperlinks and their associated reference text.

    Returns:
        Any: The encapsulated reference summaries produced by the agent, or raises an exception if an error occurs.
    """
    try:

        reference_agent = create_research_agent(provider = provider, selected_model = selected_model)
        response_json, prompt_tokens, completion_tokens, total_tokens, response_time = reference_agent.generate_response(reference_data = hyperlink_content, main_content = pdf_content)
        encapsulated_references = response_json.encapsulated_references
        
        logger.info(f"Prompt Tokens: {prompt_tokens}")
        logger.info(f"Completion Tokens: {completion_tokens}")
        logger.info(f"Total Tokens: {total_tokens}")
        logger.info(f"Response Time: {response_time}")

        return encapsulated_references
    
    except Exception as e:
        logger.error(f"An error {e} occurred during generation of reference summaries.\n{traceback.format_exc()}")
        raise e