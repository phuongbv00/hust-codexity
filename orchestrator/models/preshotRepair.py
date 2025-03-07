from pydantic import BaseModel
from models.vulnerability import Vulnerability

class PreshotRepairInput(BaseModel):
    prompt: str