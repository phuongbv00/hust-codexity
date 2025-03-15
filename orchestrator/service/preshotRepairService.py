import httpx
from models.itelrationRepair import ItelrationRepairInput
from models.generate_code import GenerateCodeRequest
from models.sastTool import SASTToolRequest
from service.commonService import CommonService

class PreshotRepairService:
    def __init__(self, common_service: CommonService):
        self.common_service = common_service

    # Preshot Repair Flow
    def preshotRepair(self, input: ItelrationRepairInput):
        try:
            vulnerabilities = []
            # call LLM local
            request_llm = GenerateCodeRequest(
                prompt = input.prompt,
                temperature = 0.5,  # Gán giá trị tùy chỉnh
                max_tokens = 1024,
                model_type = "local",
                vulnerabilities = []
            )
            codeGen = self.common_service.callLLMChatGPT(request_llm)
            # call SAST tool
            request_sast = SASTToolRequest(
                code = codeGen["code"]
                )
            sastResult = self.common_service.callSASTTool(request_sast)

            if sastResult["vulnerabilities"]:
                request_llm.vulnerabilities = sastResult["vulnerabilities"]
            # call LLM chatGPT
            request_llm.model_type = "chatgpt"
            codeGen = self.common_service.callLLMChatGPT(request_llm)
            
            # call SAST tool check final vul
            request_sast.code = codeGen["code"]
            sastResult = self.common_service.callSASTTool(request_sast)
            vulnerabilities = sastResult["vulnerabilities"]
        except Exception as e:
            print("Error: ", e)

        res = {
            "code": codeGen["code"],
            "vulnerabilities": vulnerabilities
        }    
        return res