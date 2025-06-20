# import requests
# from typing import List

# class ContentGenerator:
#     @staticmethod
#     def _call_api(system_prompt: str, user_prompt: str, max_token: int = 300, temperature: float = 0.7, stream: bool = False) -> str:
#         headers = {
#             "Authorization": f"Bearer {current_app.config["LLM_API_KEY"]}",
#             "Content-Type": "application/json"
#         }
#         data = {
#             "model": current_app.config["LLM_API_MODEL"],
#             "max_tokens": max_token,
#             "temperature": 0.7,
#             "messages": [
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": user_prompt}
#             ]
#         }

#         response = requests.post(current_app.config["LLM_API_URL"], headers=headers, json=data)
#         if response.status_code == 200:
#             return response.json()["choices"][0]["message"]["content"]
#         else:
#             raise Exception(f"API error {response.status_code}: {response.text}")

#     @staticmethod
#     def generate_topic_suggestions(query: str) -> List[str]:
#         query_str = query.get("query", "")
#         limit = query.get("limit", 5)

#         # system_prompt = (
#         #     "Bạn là trợ lý sáng tạo nội dung video. "
#         #     "Trả về CHỈ JSON: {\"topics\": [\"topic1\", \"topic2\", ...]}. "
#         #     "Không thêm markdown, code fence, hoặc định dạng khác."
#         # )
#         # user_prompt = (
#         #     f"Gợi ý {limit} chủ đề video ngắn (dưới 1 phút) thịnh hành, hấp dẫn cho từ khóa: \"{query_str}\"."
#         #     if query_str
#         #     else f"Gợi ý {limit} chủ đề video ngắn (dưới 1 phút) thịnh hành, hấp dẫn."
#         # )

#         system_prompt = "Bạn là trợ lý chuyên hỗ trợ sáng tạo nội dung video."
#         user_prompt = f"Gợi ý 5 chủ đề video ngắn thịnh hành và hấp dẫn cho từ khóa: \"{query}\"."

#         try:
#             result = ContentGenerator._call_api(system_prompt, user_prompt)
#             return [line.strip("-•* ").strip() for line in result.strip().split("\n") if line.strip()]
#         except Exception as e:
#             print(f"[Topic error] {e}")
#             return []

#     @staticmethod
#     def generate_script(topic: str) -> str:
#         # system_prompt = (
#         #     "Bạn là chuyên gia viết kịch bản video ngắn. "
#         #     "Trả về CHỈ văn bản thuần, không markdown, code fence, hoặc JSON. "
#         #     "Script phải hấp dẫn, rõ ràng, phù hợp cho lồng tiếng và video với ảnh nền AI."
#         # )
#         # user_prompt = f"Viết kịch bản video ngắn (~100 từ) về chủ đề: \"{topic}\", dùng cho lồng tiếng."

#         system_prompt = "Bạn là chuyên gia viết kịch bản video ngắn hấp dẫn."
#         user_prompt = f"Viết một đoạn script video ngắn (~100 từ) về chủ đề: \"{topic}\"."

#         try:
#             return ContentGenerator._call_api(system_prompt, user_prompt).strip()
#         except Exception as e:
#             print(f"[Script error] {e}")
#             return "Xin lỗi, tôi không thể tạo kịch bản cho chủ đề này."
