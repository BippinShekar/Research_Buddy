from helpers.loggers import get_logger
from models.requests import AgentRequest
from fastapi.responses import JSONResponse

logger = get_logger()

async def agent_controller(request: AgentRequest):
    query = request.user_query
    logger.info(f"Agent Controller processing query: {query}")
    return JSONResponse(content={"message": "Query received", "query": query})