from agents.reference_agent import ReferenceScoutingAgent #noqa
from helpers.loggers import get_logger
from helpers.helpers import PDFProcessor
import traceback

logger = get_logger()

def reference_couting_service(path: str):
    try:
        
        pdf_processor = PDFProcessor()
        extracted_references = pdf_processor.extract_references(path)

        return extracted_references 

    except Exception as e:
        logger.error(f"An error {e} occurred during reference scouting.\More Details: {traceback.format_exc()}")
    return 