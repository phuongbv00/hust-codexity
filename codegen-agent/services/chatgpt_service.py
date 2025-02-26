from services.base_service import BaseLLMService
from openai import OpenAI
from openai.types import Completion
from config.config import Settings
class ChatGPTService(BaseLLMService):
    client: OpenAI
    settings = Settings()
 
    def __init__(self):
        self.client = OpenAI(api_key=self.settings.openai_api_key)
        return 

    def generate_code(self, request):
        response = self.client.completions.create(
            model=self.settings.open_ai_model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            messages=[
               
            ]
        )
        return ""

    def generate_programming_question_prompt(self, request): 
        return ""