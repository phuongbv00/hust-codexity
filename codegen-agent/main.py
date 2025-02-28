from fastapi import FastAPI
from services.chatgpt_service import ChatGPTService
from services.local_service import LocalService
from models.generate_code import GenerateCodeRequest, LLM_TYPE
from models.generate_question_prompt import GenerateQuestionPromptRequest
app = FastAPI()
chat_gpt_service = ChatGPTService()
local_service = LocalService()
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/generate-code")
async def generate_code(request: GenerateCodeRequest):
    if request.model_type == LLM_TYPE.CHATGPT:
        return chat_gpt_service.generate_code(request)
    else:
        return local_service.generate_code(request)

@app.post("/generate-programming-question-prompt")
def generate_programming_question_prompt(request: GenerateQuestionPromptRequest):
    if request.model_type == LLM_TYPE.CHATGPT:
        return chat_gpt_service.generate_programming_question_prompt(request)
    else:
        return local_service.generate_programming_question_prompt(request)