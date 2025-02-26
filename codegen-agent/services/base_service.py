from models.generate_code import GenerateCodeRequest
from abc import abstractmethod

class BaseLLMService:
    @abstractmethod
    def generate_code(self, request: GenerateCodeRequest) -> str:
        return
    
    @abstractmethod
    def generate_programming_question_prompt(self, request: GenerateCodeRequest) -> str:
        return
    
