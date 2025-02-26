from pydantic import BaseModel

class GenerateQuestionPromptRequest(BaseModel):
    context: str
    temperature: float
    max_tokens: int


class GenerateQuestionPromptResponse:
    prompt: str

    def __init__(self, prompt: str):
        self.prompt = prompt