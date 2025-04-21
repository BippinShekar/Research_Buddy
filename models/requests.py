from pydantic import BaseModel
from typing import Optional

class ResearchRequest(BaseModel):
    user_query: str
    data: str
    provider: Optional[str] = None
    selected_model: Optional[str] = None

class ResourceRequest(BaseModel):
    pdf_path: str
    provider: Optional[str] = None
    selected_model: Optional[str] = None