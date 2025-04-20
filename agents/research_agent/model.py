from pydantic import BaseModel

class ResearchAgentResponse(BaseModel):
    reasoning: str
    answer: str
