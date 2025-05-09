from agents.reference_agent import ReferenceScoutingAgent #noqa
from helpers.loggers import get_logger
from helpers.helpers import PDFProcessor
from typing import Dict
import traceback

logger = get_logger()

def source_reference_content(path: str):
    try:
        
        pdf_processor = PDFProcessor()
        extracted_references = pdf_processor.extract_references(path)

        return extracted_references 

    except Exception as e:
        logger.error(f"An error {e} occurred during reference scouting.\More Details: {traceback.format_exc()}")
    return 

def encapsulate_references(hyperlink_content: Dict[str, str]):
    return 