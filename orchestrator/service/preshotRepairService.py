import httpx
from models.itelrationRepair import ItelrationRepairInput
from models.generate_code import GenerateCodeRequest
from models.sastTool import SASTToolRequest
from service.commonService import CommonService

class PreshotRepairService:
    def __init__(self, common_service: CommonService):
        self.common_service = common_service

    # Preshot Repair Flow
    async def preshotRepair(self, input: ItelrationRepairInput):
        # call LLM local
        request_llm = GenerateCodeRequest(
            prompt = input.prompt,
            temperature = 0.5,  # Gán giá trị tùy chỉnh
            max_tokens = 500,
            model_type = "local",
            vulnerabilities = []
        )
        codeGen = await self.common_service.callLLMChatGPT(request_llm)
        request_sast = SASTToolRequest(
            code = codeGen.code
            )
        sastResult = await self.common_service.callSASTTool(request_sast)

        if sastResult.vulnerabilities:
            request_llm.vulnerabilities = sastResult.vulnerabilities
        codeGen = await self.common_service.callLLMChatGPT(request_llm)
            
        return codeGen