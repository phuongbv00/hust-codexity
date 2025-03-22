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
                line_info = f" (Line {vuln.location.line})" if hasattr(vuln.location, "line") else ""
                vuln_info += line_info

        return [
            {
                "role": "system", 
                "content": "You are a security expert and a c language programming expert."
            },
            {
                "role": "user", 
                "content": "I will give you a piece of code containing security vulnerabilities."
            },
            {
                "role": "user",
                "content": "Then I will provide you with a list of vulnerabilities detected by Static Application Security Testing tools."
            },
            {
                "role": "user",
                "content": "Please use that list to fix the issues for me. You MUST return only the source code without any additional explanation, comment"
            },
            {
                "role": "assistant", 
                "content": "Please provide the source code"
            },
            {
                "role": "user", 
                "content": input
            },
            {
                "role": "assistant", 
                "content": "I have seen the source code you provided.Please provide the SAST tool results. This will help me understand the problem and provide a more accurate fix."
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
                "content": "You are a software developer, you can give detailed instructions for building a program."
            },
            {
                "role": "user",
                "content": "I will give you a program, summarize the meaning of each function in the program and the meaning of the program."
            },
            {
                "role": "user",
                "content": "Example:\r\nInput:\r\n#include <stdio.h>\r\n#include <stdlib.h>\r\n\r\ntypedef struct {\r\n    int *arr;\r\n    int capacity;\r\n    int size;\r\n} List;\r\n\r\nList *list_new() {\r\n    List *list = (List *) malloc(sizeof(List));\r\n    list->arr = NULL;\r\n    list->capacity = 0;\r\n    list->size = 0;\r\n    return list;\r\n}\r\n\r\nvoid list_add(List *list, int value) {\r\n    if (list->size == list->capacity) {\r\n        int newCapacity = (list->capacity == 0) ? 1 : list->capacity * 2;\r\n        int *newArr = (int *) realloc(list->arr, newCapacity * sizeof(int));\r\n        if (newArr == NULL) {\r\n            printf(\"Memory allocation failed.\\n\");\r\n            return;\r\n        }\r\n        list->arr = newArr;\r\n        list->capacity = newCapacity;\r\n    }\r\n    list->arr[list->size] = value;\r\n    list->size++;\r\n}\r\n\r\nvoid list_print(List *list) {\r\n    printf(\"List: \");\r\n    for (int i = 0; i < list->size; i++) {\r\n        printf(\"%d \", list->arr[i]);\r\n    }\r\n    printf(\"\\n\");\r\n}\r\n\r\nvoid list_free(List *list) {\r\n    free(list->arr);\r\n    free(list);\r\n}\r\n\r\nint main() {\r\n    List *list = list_new();\r\n    list_add(list, 10);\r\n    list_add(list, 20);\r\n    list_add(list, 30);\r\n    list_print(list);\r\n    list_free(list);\r\n    return 0;\r\n}"
            },
            {
                "role": "user",
                "content": "output:\r\nSummary of the Program: This program implements a dynamic list (similar to a dynamically resizing array) in C. It allows adding integers to the list, dynamically resizes the list as needed, prints the contents, and properly frees memory when done.\r\n\r\nFunction Breakdown:\r\n- List *list_new() : Creates a new empty list.\r\n- void list_add(List *list, int value): Adds a new integer to the list, resizing it dynamically if needed.\r\n- void list_print(List *list): Prints all the elements in the list.\r\n- void list_free(List *list): Frees the dynamically allocated memory used by the list.\r\n- int main(): Demonstrates the usage of the dynamic list."
            },
            {
                "role": "user",
                "content": input
            }
        ]
    
