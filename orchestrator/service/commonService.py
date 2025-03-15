import httpx
from models.itelrationRepair import ItelrationRepairInput
from models.generate_code import GenerateCodeRequest
from models.sastTool import SASTToolRequest
import requests
import os

URL_LLM_CHATGPT = "http://127.0.0.1:8081/generate-code"
URL_GEN_QUESTION = "http://127.0.0.1:8081/generate-programming-question-prompt"
URL_SAST_TOOL = "http://127.0.0.1:8082/analyze-code"

class CommonService:
    def __init__(self):
        self.client = requests
    
    # call LLM chatGPT
    def callLLMChatGPT(self, request) -> dict:
        response = self.client.post(f"{URL_LLM_CHATGPT}", json=request.model_dump(), timeout=60)
        response.raise_for_status()  # Nếu lỗi, nó sẽ tự động raise exception
        return response.json() 
     
    
    # call SAST tool
    def callSASTTool(self, request) -> dict:
        response = self.client.post(f"{URL_SAST_TOOL}",  json=request.model_dump())
        response.raise_for_status()  # Nếu lỗi, nó sẽ tự động raise exception
        return response.json() 
    
    # call gen question
    def callgenQuestion(self, request) -> dict:
        response = self.client.post(f"{URL_GEN_QUESTION}",  json=request)
        response.raise_for_status()  # Nếu lỗi, nó sẽ tự động raise exception
        return response.json() 
    
    def write_result(self, dir, sub_dir, name_file, generated_codes):
        # Định nghĩa đường dẫn thư mục và file
        directory_path = os.path.join(dir, sub_dir)
        file_path = os.path.join(directory_path, name_file)

        # Kiểm tra và tạo thư mục nếu chưa tồn tại
        os.makedirs(directory_path, exist_ok=True)

        # Ghi đè nội dung vào file
        with open(file_path, "w") as file:
            file.write(generated_codes)
    