from pydantic import BaseModel

class ResourceAgentResponse(BaseModel):
    objective: str
    title: str
    summary: str
