from helpers.loggers import get_logger
from models.requests import ResearchRequest, ResourceRequest
from fastapi.responses import JSONResponse
from services.research_service import research_service
from services.resource_service import process_pdf_document
import traceback

logger = get_logger()

async def research_agent(request: ResearchRequest):
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
    pdf_path = request.pdf_path
    provider = request.provider
    selected_model = request.selected_model

    logger.info(f"Resource Controller processing resource data from {pdf_path}")
    try:
        result = process_pdf_document(pdf_path, provider, selected_model)
        return JSONResponse(content={"result": result}, status_code=200)
    except Exception as e:
        logger.error(f"Error in resource agent: {e} at: {traceback.format_exc()}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
