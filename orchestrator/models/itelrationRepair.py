from pydantic import BaseModel

class ItelrationRepairInput(BaseModel):
    prompt: str
    max_iterations: int
