from pydantic import BaseModel

class Agent1Response(BaseModel):
    reasoning: str
    answer: str
