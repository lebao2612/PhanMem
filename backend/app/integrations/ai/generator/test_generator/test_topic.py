import requests
import json

API_KEY = "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"

prompt = "Gợi ý 50 trending topic, trả về dạng danh sách, mỗi dòng là 1 topic. Trả lời dạng text, không có ký tự đặc biệt."

url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
data = {
    "model": "gpt-3.5-turbo",
    # "max_tokens": 150,
    # "temperature": 0.7,
    "stream": True,
    "messages": [
        {"role": "system", "content": "Bạn là trợ lý chuyên hỗ trợ sáng tạo nội dung video. Chỉ trả lời đúng kết quả mà không cần giải thích."},
        {"role": "user", "content": prompt}
    ]
}

response = requests.post(url, headers=headers, json=data, stream=True)

if response.status_code == 200:
    print("📌 Kết quả trả về:\n")
    for line in response.iter_lines():
        line = line.decode("utf-8").strip()
        if not line.startswith("data: "):
            continue

        json_data = line.replace("data: ", "")
        if json_data == "[DONE]":
            break

        try:
            chunk = json.loads(json_data)
            delta = chunk["choices"][0]["delta"]
            if "content" in delta:
                print(delta["content"], end="", flush=True)
        except json.JSONDecodeError as e:
            print(f"\n❌ JSONDecodeError: {e}")
            print(f"Dữ liệu lỗi: {json_data}")
else:
    print("❌ Lỗi:", response.status_code)
    print(response.text)
