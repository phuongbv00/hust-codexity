from pydantic import BaseModel

class SASTToolRequest(BaseModel):
    code: str