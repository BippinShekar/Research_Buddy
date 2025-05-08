from pydantic import BaseModel
from typing import Dict

class ReferenceScoutingAgent(BaseModel):
    encapsulated_references: Dict[str, str] | None