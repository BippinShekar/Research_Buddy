from pydantic import BaseModel
from typing import Optional

class AgentRequest(BaseModel):
    user_query: str
    data: str
    provider: Optional[str] = None
    selected_model: Optional[str] = None