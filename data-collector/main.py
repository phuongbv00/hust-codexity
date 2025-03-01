
import requests
import json
import time
import logging
import re
import subprocess
import os

def setup_logging():
    logging.basicConfig(
        filename="stackoverflow_c.log", 
        level=logging.INFO, 
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def extract_code_snippet(body):
    """Trích xuất đoạn mã từ nội dung câu trả lời trên StackOverflow."""
    code_blocks = re.findall(r'<code>(.*?)</code>', body, re.DOTALL)
    return "\n".join(code_blocks) if code_blocks else ""

def fetch_stackoverflow_data(tag="c", pages=5):
    """Lấy danh sách câu hỏi và đoạn mã từ câu trả lời trên StackOverflow theo tag C."""
    url_questions = "https://api.stackexchange.com/2.3/questions"
    url_answers = "https://api.stackexchange.com/2.3/questions/{}/answers"
    
    params = {
        "order": "desc",
        "sort": "votes",
        "tagged": tag,
        "site": "stackoverflow",
        "pagesize": 50,
        "filter": "withbody"
    }
    
    questions = []
    for page in range(1, pages + 1):
        params["page"] = page
        response = requests.get(url_questions, params=params)
        
        if response.status_code == 429:
            print("⚠ Lỗi 429: Quá nhiều request, đang chờ 10 giây...")
            time.sleep(10)
            continue
        
        if response.status_code == 200:
            data = response.json()
            for item in data.get("items", []):
                question_id = item["question_id"]
                
                # Lấy code từ câu trả lời
                answer_response = requests.get(url_answers.format(question_id), params={"site": "stackoverflow", "filter": "withbody"})
                answers_code = []
                security_issues = []
                if answer_response.status_code == 200:
                    answer_data = answer_response.json()
                    for ans in answer_data.get("items", []):
                        code_snippet = extract_code_snippet(ans.get("body", ""))
                        if code_snippet:
                            answers_code.append(code_snippet)
                            security_issues.extend(check_security_issues(code_snippet))
                
                questions.append({
                    "id": question_id,
                    "title": item["title"],
                    "tags": item["tags"],
                    "link": item["link"],
                    "answers_code": answers_code,
                    "security_issues": security_issues
                })
        else:
            print(f"Lỗi khi lấy dữ liệu: {response.status_code}")
        
        time.sleep(5)
    
    return questions

def check_security_issues(code):
    """Kiểm tra lỗi bảo mật trong mã nguồn C bằng CppCheck."""
    issues = []
    if not code.strip():
        return issues
    
    filename = "temp.c"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)
    
    result = subprocess.run(["cppcheck", "--enable=all", filename], capture_output=True, text=True)
    
    if result.returncode == 0:
        for line in result.stderr.split("\n"):
            if "error" in line.lower() or "warning" in line.lower():
                issues.append(line.strip())
    
    os.remove(filename)
    return issues

# Cấu hình logging
setup_logging()

# Lấy dữ liệu C từ StackOverflow
dataset = fetch_stackoverflow_data(pages=5)

# Hiển thị số lượng lỗi bảo mật tìm thấy
total_issues = sum(len(entry["security_issues"]) for entry in dataset)
print(f"✅ Tổng số lỗi bảo mật tìm thấy: {total_issues}")

# Lưu vào file JSON
with open("stackoverflow_c_code.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=4, ensure_ascii=False)

print("✅ Dữ liệu đã được lưu vào stackoverflow_c_code.json")
