from models.vulnerability import Vulnerability
from pydantic import BaseModel
from enum import Enum
class LLM_TYPE(Enum):
    LOCAL = "local"
    CHATGPT = "chatgpt"
class GenerateCodeRequest(BaseModel):
    prompt: str
    temperature: float
    max_tokens: int
    model_type: LLM_TYPE
    vulnerabilities: list[Vulnerability]

class GenerateCodeResponse:
    code: str
    def __init__(self, code: str):
        self.code = code