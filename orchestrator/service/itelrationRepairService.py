import httpx
from models.itelrationRepair import ItelrationRepairInput
from models.generate_code import GenerateCodeRequest
from models.sastTool import SASTToolRequest
from service.commonService import CommonService

class ItelrationRepairService:
    def __init__(self, common_service: CommonService):
        self.common_service = common_service

    # Itelration Repair Flow
    async def itelrationRepair(self, input: ItelrationRepairInput):
        # call LLM
        request_llm = GenerateCodeRequest(
            prompt = input.prompt,
            temperature = 0.5,  # Gán giá trị tùy chỉnh
            max_tokens = 500,
            model_type = "chatgpt"
        )
        codeGen = await self.common_service.callLLMChatGPT(request_llm)

        for _ in range(input.max_iterations):  
            request_sast = SASTToolRequest(
                    code = codeGen
                )
            sastResult = await self.common_service.callSASTTool(request_sast)
            if not sastResult.vulnerabilities:
                break
        
            request_llm.vulnerabilities = sastResult.vulnerabilities
            codeGen = await self.common_service.callLLMChatGPT(request_llm)
            
        return codeGen