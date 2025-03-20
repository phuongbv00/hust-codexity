from models.itelrationRepair import ItelrationRepairInput
from models.generate_code import GenerateCodeRequest
from models.sastTool import SASTToolRequest
from service.commonService import CommonService
import os

class HybridService:
    def __init__(self, common_service: CommonService):
        self.common_service = common_service

    # Hybrid Repair Flow
    def hybridRepair(self, input: ItelrationRepairInput):
        
        vulnerabilities = []
        request_llm = GenerateCodeRequest(
                prompt = input.prompt,
                temperature = 0.5,  # Gán giá trị tùy chỉnh
                max_tokens = 1024,
                model_type = "local",
                vulnerabilities = []
            )
        # call LLM local
        codeGen = self.common_service.callLLMChatGPT(request_llm)
        request_sast = SASTToolRequest(
            code = codeGen["code"]
            )
        # call SAST tool
        sastResult = self.common_service.callSASTTool(request_sast)
        if sastResult.get("vulnerabilities"):
            request_llm.vulnerabilities = sastResult["vulnerabilities"]
            request_llm.model_type = "chatgpt"
            for _ in range(input.max_iterations):  
                try:
                    # call LLM
                    codeGen = self.common_service.callLLMChatGPT(request_llm)
                    # call SAST tool
                    request_sast.code = codeGen["code"]
                    sastResult = self.common_service.callSASTTool(request_sast)
                    print("log SastResult: ", sastResult)
                    if not sastResult.get("vulnerabilities"):
                        break
                    request_llm.vulnerabilities = sastResult["vulnerabilities"]
                    vulnerabilities = sastResult["vulnerabilities"]
                except Exception as e:
                    print("Error: ", e)
                    continue
        res = {
            "code": codeGen["code"],
            "vulnerabilities": vulnerabilities
        }
        return res
    
