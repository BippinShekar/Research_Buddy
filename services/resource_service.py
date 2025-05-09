from helpers.helpers import PDFProcessor
from helpers.loggers import get_logger
from agents.resource_agent import understand_resource_agent
import os
import traceback

logger = get_logger()

def process_pdf_document(pdf_file, provider: str = None, selected_model: str = None):
    """Process a PDF document and extract key information using an AI research agent.
    
    Args:
        pdf_file: The PDF file to process
        provider (str, optional): The AI provider to use. Defaults to environment variable or 'openai'
        selected_model (str, optional): The specific model to use. Defaults to environment variable or 'gpt-4o-mini'
        
    Returns:
        dict: Dictionary containing summary, detailed title, objective and any extracted images
        
    Raises:
        Exception: If there is an error during processing
    """
    try:
        # Set default values if not provided
        selected_model = os.getenv("SELECTED_MODEL", "gpt-4o-mini") if selected_model is None else selected_model
        provider = os.getenv("PROVIDER", "openai")
        
        # Extract content from PDF
        pdf_processor = PDFProcessor(pdf_path = pdf_file)

        text_content = pdf_processor.extract_text()
        image_content = pdf_processor.extract_images() #noqa

        resource_agent = understand_resource_agent(provider=provider, selected_model=selected_model)
        
        response_json, prompt_tokens, completion_tokens, total_tokens, response_time = resource_agent.generate_response(
            data=text_content
        )
        
        logger.info(f"Prompt Tokens: {prompt_tokens}")
        logger.info(f"Completion Tokens: {completion_tokens}") 
        logger.info(f"Total Tokens: {total_tokens}")
        logger.info(f"Response Time: {response_time}")
        
        document_info = {
            "summary": response_json.summary,
            "title": response_json.title,
            "atomic_summaries": response_json.atomic_summaries
        }
        
        return document_info
        
    except Exception as e:
        logger.error(f"Error processing PDF document: {e}.\n{traceback.format_exc()}")
        raise e