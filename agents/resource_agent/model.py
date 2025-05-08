from pydantic import BaseModel

class ResourceAgentResponse(BaseModel):
    atomic_summaries: dict
    title: str
    summary: str
