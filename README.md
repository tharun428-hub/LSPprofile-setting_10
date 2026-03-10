Loan Service Platform (LSP) – Backend API

A FastAPI-based Loan Service Platform (LSP) that manages users, profile settings, loan applications, and admin controls.
This project provides authentication, profile management, loan application processing, and admin-level user management.

🚀 Features
User Features

User Registration & Login

JWT Authentication

Profile Management

Upload Profile Image

Profile Completion Percentage

Bank Details Management

Employee Details Management

Consent Management

Loan Application

Admin Features

Admin Login

View All Users

View Admin Users

Create Admin

Delete Users (after request review)

Lock / Unlock User Accounts

View Profile Settings

Update Any User Profile

View Dashboard

System Features

Secure Authentication with JWT

Role-Based Access Control

Profile Completion Tracking

Email Notification Support

Database Integration with SQLAlchemy

Modular FastAPI Architecture

🏗 Project Structure
LSPprofiletemp
│
├── app
│   ├── core
│   │   ├── auth.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── email_service.py
│   │   ├── permissions.py
│   │   └── dependencies.py
│   │
│   ├── models
│   │   ├── user.py
│   │   ├── user_profile.py
│   │   ├── bank_details.py
│   │   ├── employee_details.py
│   │   ├── loan.py
│   │   ├── consent.py
│   │   ├── notification.py
│   │   └── change_request.py
│   │
│   ├── routes
│   │   ├── auth.py
│   │   ├── admin.py
│   │   ├── user.py
│   │   ├── profile.py
│   │   └── loan.py
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
⚙️ Tech Stack
Technology	Usage
FastAPI	Backend Framework
Python	Programming Language
SQLAlchemy	ORM
JWT	Authentication
Pydantic	Data Validation
PostgreSQL / MySQL	Database
Swagger UI	API Testing

▶️ Run the Application
uvicorn app.main:app --reload

Server will start at:

http://127.0.0.1:8000
📘 API Documentation

FastAPI automatically provides interactive documentation.

Swagger UI
http://127.0.0.1:8000/docs
ReDoc
http://127.0.0.1:8000/redoc
🔐 Authentication

The API uses JWT Token Authentication.

Steps:

Login using /login

Get access token

Use token in headers

Authorization: Bearer <token>
📊 Profile Completion Logic

Profile completion is calculated based on filled user profile fields such as:

Name

Email

Phone Number

Address

Bank Details

Employee Details

Profile Image

Each field contributes to a percentage of profile completion.

🧪 Testing APIs

You can test APIs using:

Swagger UI

Postman

Curl


📄 License

This project is licensed under the MIT License.