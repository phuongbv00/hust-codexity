from services.base_service import BaseLLMService
from openai import OpenAI
from models.generate_code import GenerateCodeResponse
from models.generate_question_prompt import GenerateQuestionPromptResponse
from config.config import Settings
class ChatGPTService(BaseLLMService):
    client: OpenAI
    settings = Settings()
 
    def __init__(self):
        self.client = OpenAI(api_key=self.settings.openai_api_key)
        return 

    def generate_code(self, request):
        # Thêm thông tin về các lỗ hổng bảo mật nếu có
        if request.vulnerabilities and len(request.vulnerabilities) > 0:
            messages = self.get_repair_vulnerability_prompt(request.prompt, request.vulnerabilities)
        else:
            # Tạo messages cho API request
            messages = self.get_normal_prompt(request.prompt)
        
        # Gọi đến OpenAI 
        print(messages)
        response = self.client.chat.completions.create(
            model=self.settings.openai_model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            messages=messages
        )
        
        # Trích xuất code từ response
        generated_code = response.choices[0].message.content
        
        # Trả về code trong response format
        return GenerateCodeResponse(code=generated_code)

    def generate_programming_question_prompt(self, request): 
         
        response = self.client.chat.completions.create(
            model=self.settings.openai_model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            messages=self.get_programming_question_prompt(request.context)
        )
        
        # Trích xuất code từ response
        prompt = response.choices[0].message.content
        
        # Trả về code trong response format
        return GenerateQuestionPromptResponse(prompt=prompt)