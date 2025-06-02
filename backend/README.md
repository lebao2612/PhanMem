# 🐍 Python Backend Web Project 

Dự án này là một backend web sử dụng **Python (Flask)**

---

## 🗂️ Cấu trúc thư mục backend

project/
│── app/ # Main application package
│ ├── init.py 
│ ├── models/ # Định nghĩa các MongoDB document
│ ├── repositories/ # Truy xuất dữ liệu từ MongoDB (CRUD)
│ ├── services/ # Logic nghiệp vụ
│ ├── routes/ # Định nghĩa các API endpoint
│ ├── dto/ # Data Transfer Objects (DTO)
│ ├── migrations/ # script cập nhật dữ liệu
│ ├── ai/
│ └── database/ 
│── main.py # Khởi tạo Flask app
│── config.py # Cấu hình app & kết nối MongoDB
│── run.py # Điểm khởi chạy chính
│── requirements.txt # Danh sách thư viện cần cài
└── .env # Biến môi trường (Mongo URI, SECRET_KEY, ...)

---

