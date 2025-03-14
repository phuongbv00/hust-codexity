import requests
import json
import logging
import time
import re
import os
import html
from flask import Flask, jsonify

app = Flask(__name__)

def setup_logging():
    logging.basicConfig(
        filename="stackoverflow_c.log", 
        level=logging.INFO, 
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def extract_code_snippet(body):
    """Trích xuất đoạn mã từ nội dung."""
    code_blocks = re.findall(r'<code>(.*?)</code>', body, re.DOTALL)
    return "\n".join(code_blocks) if code_blocks else ""

def fetch_stackoverflow_data(tag="c", pages=5, timeout=60):
    """Lấy danh sách câu hỏi và câu trả lời từ StackOverflow, chỉ lưu đoạn mã."""
    base_url = "https://api.stackexchange.com/2.3/questions"
    questions = []
    start_time = time.time()

    for page in range(1, pages + 1):
        if time.time() - start_time > timeout:  # Hủy nếu quá thời gian
            print("⏳ Hủy quá trình crawl do quá 1 phút mà chưa lấy được dữ liệu.")
            return []

        params = {
            "order": "desc",
            "sort": "votes",
            "tagged": tag,
            "site": "stackoverflow",
            "pagesize": 100,
            "page": page,
            "filter": "withbody"
        }
        
        response = requests.get(base_url, params=params)

        if response.status_code == 429:
            print("⚠ Lỗi 429: Quá nhiều request, đang chờ 10 giây...")
            time.sleep(10)
            continue
        
        data = response.json()
        if not data.get("items"):
            continue  # Bỏ qua nếu không có dữ liệu

        for question in data["items"]:
            question_id = question["question_id"]
            question_code = extract_code_snippet(question.get("body", ""))

            answer_url = f"https://api.stackexchange.com/2.3/questions/{question_id}/answers"
            answer_params = {
                "order": "desc",
                "sort": "votes",
                "site": "stackoverflow",
                "filter": "withbody"
            }

            answer_response = requests.get(answer_url, params=answer_params)
            if answer_response.status_code != 200:
                continue

            answers = answer_response.json().get("items", [])
            code_snippets = [extract_code_snippet(ans.get("body", "")) for ans in answers]

            questions.append({
                "question_id": question_id,
                "question_code": question_code,
                "answer_code_snippets": [code for code in code_snippets if code]
            })
        
        print(f"Đã crawl xong page {page}. Còn lại {pages - page} page nữa.")

    if not questions:
        print("⚠ Không lấy được dữ liệu, hủy quá trình crawl.")
        return []

    filename = "stackoverflow_c_code.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=4, ensure_ascii=False)
    
    return questions

def clean_text(text):
    decoded_text = html.unescape(text)  # Decode HTML entities
    return " ".join(decoded_text.split())  # Xóa các xuống dòng và dư thừa khoảng trắng

@app.route("/fetch_code", methods=["GET"])
def fetch_code():
    data = fetch_stackoverflow_data(pages=5, timeout=60)

    if not data:
        return jsonify([])  # Trả về mảng rỗng nếu crawl thất bại trong 1 phút

    return jsonify({"message": "Dữ liệu đã được lưu vào stackoverflow_c_code.json"})

@app.route("/get_saved_code", methods=["GET"])
def get_saved_code():
    try:
        with open("stackoverflow_c_code.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for item in data:
            item["question_code"] = clean_text(item.get("question_code", ""))
            # Lấy phần tử đầu tiên của answer_code_snippets, nếu có
            if item["answer_code_snippets"]:
                item["answer_code_snippets"] = clean_text(" ".join(item["answer_code_snippets"][:1]))  # Lấy phần tử đầu tiên
            else:
                item["answer_code_snippets"] = ""  # Nếu không có phần tử nào thì để rỗng
            
    except (FileNotFoundError, json.JSONDecodeError):
        return {"error": "Không có dữ liệu hợp lệ"}, 404

    return jsonify(data)

if __name__ == "__main__":
    setup_logging()
    print("Bắt đầu crawl dữ liệu từ StackOverflow...")
    fetch_stackoverflow_data(pages=5)
    app.run(host="0.0.0.0", port=8080, debug=True, use_reloader=True)
