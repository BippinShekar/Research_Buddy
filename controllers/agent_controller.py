from helpers.loggers import get_logger
from models.requests import AgentRequest
from fastapi.responses import JSONResponse
from services.research_service import research_service
import traceback

logger = get_logger()

async def research_agent(request: AgentRequest):
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