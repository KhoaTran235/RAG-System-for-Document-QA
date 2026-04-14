from pydantic import BaseModel
from typing import Dict, Any

class Chunk(BaseModel):
    source: str
    id: int
    content: str
    metadata: Dict[str, Any]