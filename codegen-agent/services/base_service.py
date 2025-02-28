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
                "content": "Bạn là lập trình viên xuất sắc có thể giúp người dùng tạo ra các đoạn mã"
            },
            {
                "role": "user", 
                "content": "Tôi sẽ đưa ra ý tưởng, bài toán hoặc một chương trình chưa hoàn thiện.Tôi muốn bạn hoàn thành chương trình đó cho tôi.Chỉ đưa ra mã nguồn của chương trình hoàn chỉnh(không phải chỉ đoạn code bạn viết thêm) ở dạng text, không cần giải thích gì thêm, không cần đưa vào block code markdown"
            },
            {
                "role": "assistant",
                "content": "Chắc chắn rồi.Bạn hãy đưa ra ý tưởng hoặc đoạn code cần tôi hoàn thiện.Tôi sẽ giúp bạn hoàn thiện chương trình một cách hoàn chỉnh"
            },
            {
                "role": "user",
                "content": input
            }
        ]
    
    def get_repair_vulnerability_prompt(self, input, vulnerabilities: list[Vulnerability]) -> list[map]:
        vuln_info = "Danh sách lỗ hổng: \n"
        for vuln in vulnerabilities:
            vuln_info += f"- {vuln.cwe}: {vuln.message}\n"
            if vuln.location:
                line_info = f" (Dòng {vuln.location.line})" if hasattr(vuln.location, "line") else ""
                vuln_info += line_info

        return [
            {
                "role": "system", 
                "content": "Bạn là lập trình viên xuất sắc có thể giúp người dùng tạo ra các đoạn mã"
            },
            {
                "role": "user", 
                "content": "Tôi sẽ đưa cho bạn một đoạn mã chứa lỗ hổng bảo mật.Sau đó tôi sẽ đưa cho bạn danh sách các lỗ hổng được các công cụ Static Application Security Testing phát hiện ra.Bạn hãy dựa vào danh sách đó để sửa lỗi cho tôi.Bạn chỉ cần đưa ra mã nguồn của chương trình ở dạng text, không cần viết gì thêm, không cần đưa vào block code markdown"
            },
            {
                "role": "assistant", 
                "content": "Chắc chắn rồi, tôi có thể giúp bạn phân tích mã nguồn và kết quả từ công cụ SAST để xác định và khắc phục các vấn đề. Vui lòng cung cấp mã nguồn và kết quả từ công cụ SAST, và tôi sẽ cố gắng hết sức để hỗ trợ bạn. Tôi sẽ chỉ đưa ra mã nguồn được sửa chữa và không giải thích gì thêm."
            },
            {
                "role": "user", 
                "content": input
            },
            {
                "role": "assistant", 
                "content": "Tôi đã thấy mã nguồn bạn cung cấp. Để hỗ trợ bạn tốt hơn, vui lòng cung cấp kết quả từ các công cụ SAST và chỉ rõ các vấn đề hoặc lỗi mà bạn đang gặp phải. Điều này sẽ giúp tôi hiểu rõ vấn đề và đưa ra cách sửa mã chính xác hơn."
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
                "content": "Bạn là một kỹ sư phần mềm xuất sắc có thể giúp người dùng tạo ra các câu hỏi lập trình từ đoạn mã có sẵn hoặc câu trả lời."
            },
            {
                "role": "user",
                "content": "Tôi sẽ cung cấp cho bạn một đoạn mã hoặc câu trả lời. Bạn hãy sử dụng ngữ cảnh này để tạo ra câu hỏi lập trình liên quan đến đoạn mã hoặc câu trả lời đó."
            },
            {
                "role": "user",
                "content": "Lưu ý, bạn chỉ cần đưa ra 5 câu hỏi, mỗi câu ở 1 dòng riêng biệt.Ví dụ về phản hồi của bạn: \n- Câu hỏi 1: Nội dung \n- Câu hỏi 2: Nội dung \n"
            },
            {
                "role": "assistant",
                "content": "Chắc chắn rồi. Vui lòng cung cấp ngữ cảnh chứa mã hoặc câu trả lời để tôi có thể tạo ra câu hỏi lập trình liên quan đến ngữ cảnh đó cho bạn cho bạn."
            },
            {
                "role": "user",
                "content": input
            }
        ]
    
