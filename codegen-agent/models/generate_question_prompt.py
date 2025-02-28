from pydantic import BaseModel
from models.generate_code import LLM_TYPE

class GenerateQuestionPromptRequest(BaseModel):
    context: str
    temperature: float
    max_tokens: int
    model_type: LLM_TYPE
class GenerateQuestionPromptResponse:
    prompt: str

    def __init__(self, prompt: str):
        self.prompt = prompt