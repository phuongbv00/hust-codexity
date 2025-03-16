from operator import index

import httpx
from service.commonService import CommonService
from models.sastTool import SASTToolRequest
from models.generate_code import GenerateCodeRequest
import json
import os
import requests

URL_GET_POST="http://localhost:8080/fetch-dataset"

class DataConstruction:
    def __init__(self, common_service: CommonService):
        self.client = httpx.AsyncClient()
        self.common_service = common_service

    def genQuestion(self, post, index):
        request_gen_question = {
                "context": post["answer_code_snippets"],
                "temperature": 0,
                "max_tokens": 1024,
                "model_type": "chatgpt"
            }
        question = self.common_service.callgenQuestion(request_gen_question)

        codeVulnerabilities = []
        codeTmp = []
        checkPrompt = False

        # call LLM call 1 temperature 0, 10 lan temperature 0.8
        request_llm = GenerateCodeRequest(
            prompt = question["prompt"],
            temperature = 0,  # Gán giá trị tùy chỉnh
            max_tokens = 1024,
            model_type = "chatgpt",
            vulnerabilities = []
        )
        codeGen = self.common_service.callLLMChatGPT(request_llm)
        codeTmp.append(codeGen["code"])
        for _ in range(10):
            request_llm.temperature = 0.8
            codeGen = self.common_service.callLLMChatGPT(request_llm)
            codeTmp.append(codeGen["code"])

        # call sast tool
        for code in codeTmp:
            request_sast = SASTToolRequest(
                code = code
            )
            sastResult = self.common_service.callSASTTool(request_sast)
            if sastResult["vulnerabilities"]:
                codeVulnerabilities.append(code)
                checkPrompt = True

        if checkPrompt: 
            self.common_service.write_result("data_v2", str(index), "prompt.c", post["answer_code_snippets"])
            fileName = 1
            for codeVul in codeVulnerabilities:
                self.common_service.write_result("data_v2", str(index), str(fileName) + ".c", codeVul)
                fileName = fileName + 1

    def createData(self):
        # call data collector
        # data_req = {"title": "FastAPI", "completed": False}
        response = requests.get(f"{URL_GET_POST}")
        response.raise_for_status()  # Nếu lỗi, nó sẽ tự động raise exception
        totalPost =  response.json()

        index= 1
        if totalPost and len(totalPost) > 0:
            for post in totalPost:
                response = self.genQuestion(post,index)
                index = index + 1

        #         if response.codeVulnerabilities:
        #             questions.append(response.question)
        #             codeVulnerabilities.extend(response.codeVulnerabilities)
