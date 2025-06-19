# 🐍 Python Backend Web Project 

Dự án này là một backend web sử dụng **Python (Flask)**

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
│   │   ├── *_bp                 # Các blueprint
│   ├── dto/                     # Data Transfer Objects (DTO)
│   ├── migrations/              # Script cập nhật dữ liệu
│   ├── integrations/            # Tích hợp bên ngoài (AI, media, etc.)
│   │   ├── ai/
│   │   ├── cloud/
│   └── database/                # Kết nối cơ sở dữ liệu
│
├── config/                      # Cấu hình app & kết nối MongoDB
│   └── config.py
├── run.py                       # Điểm khởi chạy chính
├── requirements.txt             # Danh sách thư viện cần cài
└── .env                         # Biến môi trường (Mongo URI, SECRET_KEY, ...)

---

