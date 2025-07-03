# 🐍 Python Backend Web Project 

Dự án này là một backend web sử dụng **Python (FastAPI)**

---

## 🗂️ Cấu trúc thư mục backend

project/
│
├── app/                         # Main application package
│   ├── __init__.py              # Khởi tạo app
│   ├── models/                  # Định nghĩa các MongoDB document
│   ├── repositories/            # Truy xuất dữ liệu từ MongoDB (CRUD)
│   ├── services/                # Logic nghiệp vụ, thao tác với repo
│   ├── api/                     # Định nghĩa các API endpoint
│   │   ├── middleware/          # Chứa middleware, error handler
│   │   ├── routers/             # Các routers
│   ├── dto/                     # Data Transfer Objects (DTO)
│   ├── migrations/              # Script cập nhật dữ liệu
│   ├── schemas/                 # Định nghĩa các Pydantic schema cho validate input/output (request & response models)
│   ├── integrations/            # Tích hợp bên ngoài (AI, media, etc.)
│   │   ├── ai/
│   │   ├── cloud/
│   │   ├── platform/            # Youtube, Facebook...
│   └── database/                # Kết nối cơ sở dữ liệu
│   ├── utils/                   # 
│
├── config/                      # Cấu hình app & kết nối MongoDB
│   └── settings.py
├── run.py                       # Điểm khởi chạy chính
├── requirements.txt             # Danh sách thư viện cần cài
├── secrets/                     # 
└── .env                         # Biến môi trường (Mongo URI, SECRET_KEY, ...)

---

