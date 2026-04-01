🚀 Finance Dashboard Backend (Internship Assignment)

A simple and well-structured backend built using FastAPI for managing financial records with role-based access control.

💡 What this project does
User authentication using JWT
Role-based access (Viewer, Analyst, Admin)
Manage financial records (income/expense)
Filter, search, and paginate records
Dashboard APIs for totals and insights
Clean error handling and validation
Bonus: external joke API (for demo purpose)


⚙️ Tech Stack
Python + FastAPI
MongoDB(MONGO_URI)
JWT Authentication
Pydantic
bcrypt (password hashing)

📁 Project Structure
FinSight_Backend/
├── main.py
├── database.py
├── models/
├── schemas/
├── routes/
├── services/
└── utils/


▶️ How to Run
git clone <repo-url>
cd project
pip install -r requirements.txt
uvicorn app.main:app --reload

Swagger:
👉 http://127.0.0.1:8000/docs


🔐 Roles
Viewer → can view dashboard
Analyst → can view records + dashboard
Admin → full control (users + records)


📌 Main APIs
Auth
Register & Login
Records
Create, read, update, delete
Filter by type, category, date
Pagination supported
Dashboard
Total income
Total expense
Net balance
Category-wise summary
Monthly trends
Recent transactions
Bonus
Random joke API (external integration demo)


⚠️ Error Handling
Proper status codes (400, 401, 403, 404, etc.)
Input validation using Pydantic
Handles invalid data and access restrictions


🧠 Notes
Clean and modular structure
Business logic separated in services
Role-based access handled using dependencies
Soft delete used for records

💬 Final Thought

This project focuses on clean backend design, correct logic, and maintainable structure rather than unnecessary complexity.
