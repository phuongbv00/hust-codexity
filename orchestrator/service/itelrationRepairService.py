import httpx
from models.itelrationRepair import ItelrationRepairInput
from models.generate_code import GenerateCodeRequest
from models.sastTool import SASTToolRequest
from service.commonService import CommonService
import os

BASE_DIR = "Codes"
class ItelrationRepairService:
    def __init__(self, common_service: CommonService):
        self.common_service = common_service

    # Itelration Repair Flow
    def itelrationRepair(self, input: ItelrationRepairInput):
        
        vulnerabilities = []
        request_llm = GenerateCodeRequest(
                prompt = input.prompt,
                temperature = 0.5,  # Gán giá trị tùy chỉnh
                max_tokens = 1024,
                model_type = "chatgpt",
                vulnerabilities = []
            )
        for _ in range(input.max_iterations):  
            try:
                # call LLM
                codeGen = self.common_service.callLLMChatGPT(request_llm)
                request_sast = SASTToolRequest(
                        code = codeGen["code"]
                    )
                sastResult = self.common_service.callSASTTool(request_sast)
                if not sastResult["vulnerabilities"]:
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
    

    def codexity(self):
        # Lặp qua từng thư mục con trong Code/
        result = []
        for folder in range(1, 2):  # Duyệt từ 1 -> 90
            folder_path = os.path.join(BASE_DIR, str(folder) + ".c")  # Đường dẫn đến thư mục con

            if not os.path.exists(folder_path):
                print(f"Warning: {folder_path} not found!")
                continue  # Nếu thư mục không tồn tại, bỏ qua

            # Lặp qua tất cả file .c trong thư mục con
            i = 1
            for file_name in os.listdir(folder_path):
                if file_name.endswith(".c"):  # Chỉ xử lý file .c
                    file_path = os.path.join(folder_path, file_name)
                    with open(file_path, "r", encoding="utf-8") as f:
                        code_content = f.read()
                    payload = ItelrationRepairInput(
                        prompt = code_content,  # Tên file
                        max_iterations = 1  # Nội dung code
                    )
                    response = self.itelrationRepair(payload)
                    self.common_service.write_result("Result", folder_path, "Code" + str(i) + ".c", response["code"])
                    result.append(response)
                    i = i+1
        return result


    # Gửi request đến API (bỏ qua nếu chỉ muốn đọc file)
    # try:
    #     response = requests.post(API_URL, json=payload)
    #     response.raise_for_status()  # Kiểm tra lỗi HTTP
    #     print(f" Processed {file_path} - Status: {response.status_code}")
    # except requests.RequestException as e:
    #     print(f" Error processing {file_path}: {e}")