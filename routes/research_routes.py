from fastapi import APIRouter
from controllers.agent_controller import research_agent

router = APIRouter()

router.post("/research")(research_agent)