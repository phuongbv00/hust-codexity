import httpx
from service.commonService import CommonService
from models.sastTool import SASTToolRequest
from models.generate_code import GenerateCodeRequest
import json

URL_GET_POST="http://localhost:8080/get_saved_code"

class DataConstruction:
    def __init__(self, common_service: CommonService):
        self.client = httpx.AsyncClient()
        self.common_service = common_service

    async def genQuestion(self, post):
        request_gen_question = {
                "context": post.answer_code_snippets,
                "temperature": 0,
                "max_tokens": 500,
                "model_type": "chatgpt"
            }
        question = await self.common_service.callgenQuestion(request_gen_question)

        questionVulnerabilities = []
        codeVulnerabilities = []
        codeTmp = []

        # call LLM call 1 temperature 0, 10 lan temperature 0.8
        request_llm = GenerateCodeRequest(
            prompt = question,
            temperature = 0,  # Gán giá trị tùy chỉnh
            max_tokens = 500,
            model_type = "chatgpt",
            vulnerabilities = []
        )
        codeGen = await self.common_service.callLLMChatGPT(request_llm)
        codeTmp.append(codeGen.code)
        for _ in range(10):
            request_llm.temperature = 0.8
            codeGen = await self.common_service.callLLMChatGPT(request_llm)
            codeTmp.append(codeGen.code)

        # call sast tool
        for code in codeTmp:
            request_sast = SASTToolRequest(
                code = code
            )
            sastResult = await self.common_service.callSASTTool(request_sast)
            if sastResult.vulnerabilities:
                codeVulnerabilities.append(code)
        res = {
            "question": question,
            "codeVulnerabilities": codeVulnerabilities
        }       
        return res

    async def createData(self):
        # call data collector
        # data_req = {"title": "FastAPI", "completed": False}
        response = await self.client.get(f"{URL_GET_POST}")
        response.raise_for_status()  # Nếu lỗi, nó sẽ tự động raise exception
        totalPost =  response.json()
        codeVulnerabilities = []
        questions = []

        if totalPost and len(totalPost) > 0:
            for post in totalPost:
                response = self.genQuestion(post)
                if response.codeVulnerabilities:
                    questions.append(response.question)
                    codeVulnerabilities.extend(response.codeVulnerabilities)

        # save file questin and code
        filename = "question.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(questions, f, indent=4, ensure_ascii=False)
        
        filename = "code.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(codeVulnerabilities, f, indent=4, ensure_ascii=False)
            
