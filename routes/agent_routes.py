from fastapi import APIRouter
from controllers.agent_controller import agent_controller

router = APIRouter()

router.get("/agent1")(agent_controller)