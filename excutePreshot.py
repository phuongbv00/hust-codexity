import os
import requests
import time

BASE_DIR = "Data"
URL_PRESHOT = "http://127.0.0.1:8083/preshot-repair"

def codexity():
    start_time = time.time()
    # Lặp qua từng thư mục con trong Code/
    codeProcess = 0
    codeNonVul = 0
    codeVul = 0

    for folder in range(1, 91):  # Duyệt từ 1 -> 90
        folder_path = os.path.join(BASE_DIR, str(folder) + ".c")  # Đường dẫn đến thư mục con

        if not os.path.exists(folder_path):
            print(f"Warning: {folder_path} not found!")
            continue  # Nếu thư mục không tồn tại, bỏ qua

        # Lặp qua tất cả file .c trong thư mục con
        i = 1
        for file_name in os.listdir(folder_path):
            try:
                if file_name.endswith(".c"):  # Chỉ xử lý file .c
                    file_path = os.path.join(folder_path, file_name)
                    with open(file_path, "r", encoding="utf-8") as f:
                        code_content = f.read()
                    payload = {
                        "prompt" : code_content
                    }
                    codeProcess += 1
                    response = requests.post(f"{URL_PRESHOT}", json=payload)
                    # response.raise_for_status()
                    dataRes = response.json()
                    if dataRes["vulnerabilities"]:
                        codeVul += 1
                    else:
                        codeNonVul += 1
            except Exception as e:
                print("Error: ", e)
                continue
    end_time = time.time()
    result = {
        "codeProcess" : codeProcess,
        "codeNonVul": codeNonVul,
        "codeVul": codeVul,
        "time": end_time - start_time
    }
    return result



if __name__ == "__main__":
    response =  codexity()
    print("Số lượng code ban đầu: ", 990)
    print("Số lượng code được xử lý chạy qua bộ lọc lỗ hổng bảo mật: ", response["codeProcess"])
    print("Số lượng code sau khi xử lý không còn lỗ hổng bảo mật: ", response["codeNonVul"])
    print("Số lượng code sau khi xử lý còn lỗ hổng bảo mật: ", response["codeVul"])
    print("Thời gian xử lý: ", response["time"])
    input("Nhấn Enter để thoát...") 