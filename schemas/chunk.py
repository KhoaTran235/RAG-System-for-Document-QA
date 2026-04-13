from pydantic import BaseModel

class Chunk(BaseModel):
    id: str
    content: str
    metadata: dict