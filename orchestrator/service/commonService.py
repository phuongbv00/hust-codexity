import httpx
from models.itelrationRepair import ItelrationRepairInput
from models.generate_code import GenerateCodeRequest
from models.sastTool import SASTToolRequest

URL_LLM_CHATGPT = "http://127.0.0.1:8081/generate-code"
URL_GEN_QUESTION = "http://127.0.0.1:8081/generate-programming-question-prompt"
URL_SAST_TOOL = "http://127.0.0.1:8082/analyze-code"

class CommonService:
    def __init__(self):
        self.client = httpx.AsyncClient()
    
    # call LLM chatGPT
    async def callLLMChatGPT(self, request) -> dict:
        response = await self.client.post(f"{URL_LLM_CHATGPT}", json=request.model_dump())
        response.raise_for_status()  # Nếu lỗi, nó sẽ tự động raise exception
        return response.json() 
     
    
    # call SAST tool
    async def callSASTTool(self, request) -> dict:
        response = await self.client.post(f"{URL_SAST_TOOL}",  json=request.model_dump())
        response.raise_for_status()  # Nếu lỗi, nó sẽ tự động raise exception
        return response.json() 
    
    # call gen question
    async def callgenQuestion(self, request) -> dict:
        response = await self.client.post(f"{URL_GEN_QUESTION}",  json=request)
        response.raise_for_status()  # Nếu lỗi, nó sẽ tự động raise exception
        return response.json() 
    