from models.vulnerability import Vulnerability
from pydantic import BaseModel

class GenerateCodeRequest(BaseModel):
    prompt: str
    temperature: float
    max_tokens: int
    vulnerabilities: list[Vulnerability]

class GenerateCodeResponse:
    code: str
    def __init__(self, code: str):
        self.code = code