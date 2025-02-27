from fastapi import FastAPI
from config.config import Settings
from services.chatgpt_service import ChatGPTService
from models.generate_code import GenerateCodeRequest
from models.generate_question_prompt import GenerateQuestionPromptRequest
app = FastAPI()
chat_gpt_service = ChatGPTService()
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/generate-code")
async def generate_code(request: GenerateCodeRequest):
    return chat_gpt_service.generate_code(request)

@app.post("/generate-programming-question-prompt")
def generate_programming_question_prompt(request: GenerateQuestionPromptRequest):
    return chat_gpt_service.generate_programming_question_prompt(request)