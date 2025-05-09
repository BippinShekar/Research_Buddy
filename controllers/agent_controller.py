from helpers.loggers import get_logger
from models.requests import ResearchRequest, ResourceRequest, ReferenceScouterRequest
from fastapi.responses import JSONResponse
from services.research_service import research_service
from services.resource_service import process_document
from services.reference_service import source_reference_content, encapsulate_references
import traceback

logger = get_logger()

async def research_agent(request: ResearchRequest):
    """
    Handle incoming research queries and return the generated response.

    Args:
        request (ResearchRequest): Request object containing user query, optional data, provider, and model selection.

    Returns:
        JSONResponse: A JSON response containing either the research result or an error message.
    """
    query = request.user_query
    data = request.data
    provider = request.provider
    selected_model = request.selected_model

    logger.info(f"Agent Controller processing query: {query}")
    try:
        result = research_service(query, data, provider, selected_model)
        return JSONResponse(content={"result": result}, status_code=200)
    except Exception as e:
        logger.error(f"Error in research agent: {e} at: {traceback.format_exc()}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
    

async def resource_agent(request: ResourceRequest):
    """
    Handle incoming research queries and return the generated response.

    Args:
        request (ResearchRequest): Request object containing user query, optional data, provider, and model selection.

    Returns:
        JSONResponse: A JSON response containing either the research result or an error message.
    """
    pdf_path = request.pdf_path
    provider = request.provider
    selected_model = request.selected_model

    logger.info(f"Resource Controller processing resource data from {pdf_path}")
    try:
        result = process_document(pdf_path, provider, selected_model)
        return JSONResponse(content={"result": result}, status_code=200)
    except Exception as e:
        logger.error(f"Error in resource agent: {e} at: {traceback.format_exc()}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

async def reference_agent(request: ReferenceScouterRequest):
    """
    Extract and encapsulate reference hyperlinks from a provided PDF document.

    Args:
        request (ReferenceScouterRequest): Request object with PDF path, provider, and model selection.

    Returns:
        JSONResponse: A JSON response with the extracted reference data or an error message.
    """
    pdf_path = request.pdf_path
    provider = request.provider
    selected_model = request.selected_model

    logger.info(f"Reference Controller processing resource references from {pdf_path}")
    try:
        reference_content = source_reference_content(path = pdf_path)
        reference_metadata = encapsulate_references(hyperlink_content = reference_content) #noqa

        return JSONResponse(content={"result": ""}, status_code=200)
    except Exception as e:
        logger.error(f"Error in resource agent: {e} at: {traceback.format_exc()}")
        return JSONResponse(content={"error": str(e)}, status_code=500)