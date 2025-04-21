from fastapi import APIRouter
from controllers.agent_controller import resource_agent

router = APIRouter()

router.post("/resource")(resource_agent)