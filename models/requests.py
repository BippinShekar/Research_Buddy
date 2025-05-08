from pydantic import BaseModel
from typing import Optional, List

class ResearchRequest(BaseModel):
    user_query: str
    data: str
    instructions = Optional[str] | None
    provider: Optional[str] | None
    selected_model: Optional[str] | None

class ResourceRequest(BaseModel):
    pdf_path: str
    summarization_instructions: Optional[str] | None
    provider: Optional[str] | None
    selected_model: Optional[str] | None

class ReferenceScouterRequest(BaseModel):
    references: List[str, str]
    provider = Optional[str] | None
    selected_model: Optional[str] | None

class QandARequest(BaseModel):
    context: str
    qa_instructions: Optional[str] | None
    selected_model: Optional[str] | None
    provider: Optional[str] | None

class AudioGenerationRequest(BaseModel):
    context: str
    audio_instructions: Optional[str] | None
    provider: Optional[str] | None
    selected_model: Optional[str] | None
    conversation_style: Optional[str] | None