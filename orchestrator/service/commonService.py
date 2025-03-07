import httpx
from models.itelrationRepair import ItelrationRepairInput
from models.generate_code import GenerateCodeRequest
from models.sastTool import SASTToolRequest

URL_LLM_CHATGPT = ""
URL_SAST_TOOL = ""

class CommonService:
    def __init__(self):
        self.client = httpx.AsyncClient()
    
    # call LLM chatGPT
    async def callLLMChatGPT(self, request: dict) -> dict:
        response = await self.client.post(f"{URL_LLM_CHATGPT}", json=request.dict())
        response.raise_for_status()  # Nếu lỗi, nó sẽ tự động raise exception
        return response.json() 
     
    
    # call SAST tool
    async def callSASTTool(self, request: dict) -> dict:
        response = await self.client.get(f"{URL_SAST_TOOL}",  json=request.dict())
        response.raise_for_status()  # Nếu lỗi, nó sẽ tự động raise exception
        return response.json() 
    