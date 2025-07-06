# 🐍 Python Backend Web Project

**AI Short Video Creator** – Nền tảng tạo video ngắn theo xu hướng bằng trí tuệ nhân tạo.

Dự án này là một backend web sử dụng **Python (FastAPI)**, kết hợp các công nghệ AI (LLM, TTS), xử lý video tự động, lưu trữ đám mây và cơ sở dữ liệu NoSQL.

> 🎯 Mục tiêu
- Tạo video ngắn học thuật, truyền thông, giải trí, lan tỏa kiến thức.
- Hỗ trợ sinh viên, người học thực hành với công nghệ AI đa phương tiện hiện đại.

> ⚙️ Chức năng chính
- **F1:** Gợi ý chủ đề theo xu hướng (API trend, từ khóa)
- **F2:** Sinh kịch bản video tự động (AI LLM)
- **F3:** Tạo giọng đọc AI (Text-to-Speech)
- **F4:** Tạo video tự động (ghép ảnh, voice, phụ đề)
- **F5:** Chỉnh sửa cơ bản (hiệu ứng chữ, sticker, nhạc nền)
- **F6:** Xuất video (.mp4)
- **F7:** Quản lý video đã tạo

> 🚀 Công nghệ sử dụng
- **Backend:** Python (FastAPI)
- **Frontend:** ReactJS/Next.js
- **AI NLP:** Gemini
- **TTS:** Google TTS
- **Xử lý video:** MoviePy
- **Database:** MongoDB
- **Lưu trữ media:** Cloudinary

---

## 🗂️ Cấu trúc thư mục backend

```plaintext
project/
│
├── app/                        # Thư mục chính chứa mã nguồn ứng dụng
│   ├── __init__.py             # Khởi tạo app Python package
│   ├── models/                 # Định nghĩa MongoDB document (model dữ liệu)
│   ├── repositories/           # Truy xuất dữ liệu từ MongoDB (CRUD)
│   ├── services/               # Xử lý logic nghiệp vụ
│   │   ├── internal/           # Tích hợp dịch vụ nội bộ (Repo, database, ...)
│   │   └── external/           # Tích hợp dịch vụ bên ngoài (YouTube, Google, AI, ...)
│   ├── api/                    # Định nghĩa các API endpoint
│   ├── dto/                    # Data Transfer Objects (DTO)
│   ├── migrations/             # Script cập nhật dữ liệu/migration
│   ├── schemas/                # Pydantic schema validate input/output
│   ├── integrations/           # Tích hợp dịch vụ bên ngoài (AI, media, ...)
│   │   ├── ai/                 # Tích hợp AI (Gemini, TTS, Stable Diffusion)
│   │   ├── cloud/              # Tích hợp cloud (Cloudinary, ...)
│   │   └── platform/           # Tích hợp nền tảng khác (YouTube, Google, ...)
│   ├── database/               # Kết nối & cấu hình cơ sở dữ liệu
│   └── utils/                  # Tiện ích dùng chung (JWT, File IO, ...)
│
├── config/                     # Cấu hình app & kết nối MongoDB
│   ├── settings.py             # Thiết lập cấu hình chính
│   └── constants.py            # Các hằng số dùng chung
│
├── run.py                      # Điểm khởi chạy chính của ứng dụng
├── requirements.txt            # Danh sách thư viện cần cài đặt
├── secrets/                    # Lưu trữ thông tin bí mật (không commit)
└── .env                        # Biến môi trường (Mongo URI, SECRET_KEY, ...)
```

---

## ▶️ Hướng dẫn chạy dự án

1. **Cài đặt thư viện:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Tạo file `.env`** (hoặc copy từ `.env.example`) và điền các biến môi trường cần thiết (MongoDB URI, Cloudinary, API keys...).

3. **Chạy server FastAPI:**
   ```bash
   python run.py
   ```

4. **Truy cập docs API:**  
   Mở trình duyệt tại [http://localhost:5000/docs](http://localhost:5000/docs)

---

## 📢 Liên hệ & đóng góp

---