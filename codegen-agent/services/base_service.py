from models.generate_code import GenerateCodeRequest
from models.generate_question_prompt import GenerateQuestionPromptRequest
from abc import abstractmethod
from models.vulnerability import Vulnerability
class BaseLLMService:
    @abstractmethod
    def generate_code(self, request: GenerateCodeRequest) -> str:
        return
    
    @abstractmethod
    def generate_programming_question_prompt(self, request: GenerateQuestionPromptRequest) -> str:
        return
    
    def get_normal_prompt(self, input: str) -> list:
        return [
            {
                "role": "system", 
                "content": "You are a C language programming expert."
            },
            {
                "role": "user", 
                "content": "I will provide an idea, a problem, or an incomplete program. I want you to complete the program for me. And return full source code of the program(not just the part you write) in plain text without any additional explanation, comment and markdown code blocks."
            },
            {
                "role": "assistant",
                "content": "Certainly. Please provide the idea or the code that needs completion. I will help you produce a fully functional program."
            },
            {
                "role": "user",
                "content": input
            }
        ]
    
    def get_repair_vulnerability_prompt(self, input, vulnerabilities: list[Vulnerability]) -> list[map]:
        vuln_info = "Vulnerabilities: \n"
        for vuln in vulnerabilities:
            vuln_info += f"- {vuln.cwe}: {vuln.message}\n"
            if vuln.location:
                line_info = f" (Dòng {vuln.location.line})" if hasattr(vuln.location, "line") else ""
                vuln_info += line_info

        return [
            {
                "role": "system", 
                "content": "You are a security expert and a c language programming expert."
            },
            {
                "role": "user", 
                "content": "I will give you a piece of code containing security vulnerabilities. Then I will provide you with a list of vulnerabilities detected by Static Application Security Testing tools. Please use that list to fix the issues for me. You only need to provide the source code of the program in text without any additional explanation, comment and Markdown code blocks."
            },
            {
                "role": "assistant", 
                "content": "Certainly. I can help you analyze the source code and the results from the SAST tools to identify and fix any issues. Please provide the source code and SAST results, and I will do my best to help you. I will only provide the repaired source code without any further explanation."
            },
            {
                "role": "user", 
                "content": input
            },
            {
                "role": "assistant", 
                "content": "I have seen the source code you provided. To better assist you, please provide the SAST tool results and clearly specify the issues or errors you are encountering. This will help me understand the problem and provide a more accurate fix."
            },
            {
                "role": "user", 
                "content": vuln_info
            }
        ]
    
    def get_programming_question_prompt(self, input: str) -> list:
        return [
            {
                "role": "system",
                "content": "You are an excellent software engineer who can help users generate programming questions from existing code snippets or answers."
            },
            {
                "role": "user",
                "content": "I will provide you with a code snippet or an answer. Please use this context to create programming questions related to the code snippet or answer."
            },
            {
                "role": "user",
                "content": "Note that you only need to provide 5 questions, each question on a separate line. Example of your response:\n- Question 1: Content\n- Question 2: Content\n"
            },
            {
                "role": "assistant",
                "content": "Certainly. Please provide the code snippet or answer so that I can create programming questions related to it for you."
            },
            {
                "role": "user",
                "content": input
            }
        ]
    
