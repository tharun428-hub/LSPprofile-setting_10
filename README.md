🏦 LSP Profile Setting & RBAC Service

A FastAPI-based Role Based Access Control (RBAC) microservice for managing users, admins, profile settings, and secure permission-based operations.

📑 Table of Contents

Project Overview

Modules

Roles & Permissions

API Endpoints

Router Architecture

System Architecture

RBAC Permission Matrix

Database Connection Flow

Request Lifecycle

Project Structure

Installation & Setup

Tech Stack

Authentication Flow

Module Completion Summary

Future Enhancements

Author

📌 Project Overview

The LSP Profile Setting System provides:

1️⃣ Secure authentication using JWT tokens
2️⃣ Role-Based Access Control (RBAC) for Super Admin, Admin, and Users
3️⃣ User profile management and address settings
4️⃣ Request-based account operations (lock/unlock/delete)
5️⃣ Modular FastAPI architecture for scalability and maintainability

🧩 Modules
1️⃣ Authentication Module

Handles user login and JWT token generation.

2️⃣ Role-Based Access Control (RBAC)

Controls API access based on user roles and permissions.

3️⃣ Admin Management Module

Allows admins to manage users and process system requests.

4️⃣ Profile Settings Module

Handles personal details, employment data, bank information, and address settings.

5️⃣ Change Request Module

Used for sensitive actions that require approval such as account deletion or lock requests.

👥 Roles & Permissions
Role	Permissions
Super Admin	Full system access, create admin, lock/unlock users
Admin	Manage users, process requests, update profiles
User	Manage own profile & address
🔐 Super Admin Access

Login

View all users

Create Admin

Delete Users (via request)

Lock / Unlock accounts

Update any user profile

Access Admin Dashboard

👨‍💼 Admin Access

Login

View users

View dashboard

Update user data

Process requests

View profile settings

👤 User Access

Login

View own profile

Update personal details

Manage address settings

🔗 API Endpoints
Authentication
Method	Endpoint	Description
POST	/auth/login	User login & JWT token generation
Admin APIs
Method	Endpoint	Description
GET	/admin/users	View all users
POST	/admin/create	Create admin
PUT	/admin/lock/{id}	Lock user account
PUT	/admin/unlock/{id}	Unlock user account
User APIs
Method	Endpoint	Description
GET	/user/profile	View own profile
PUT	/user/update	Update user details
Profile Settings APIs
Method	Endpoint	Description
GET	/profile/read	Read profile settings
POST	/profile/address	Add address
PUT	/profile/address	Update address
🧭 Router Architecture
Router	File	Purpose
Auth Router	routes/auth.py	Authentication
Admin Router	routes/admin.py	Admin operations
User Router	routes/user.py	User operations
Profile Read Router	routes/profile_read.py	Profile viewing
Profile Address Router	routes/profile_address.py	Address management
Router Flow
Client Request
      ↓
FastAPI App
      ↓
Router (Module Based)
      ↓
RBAC Permission Check
      ↓
Database (SQLAlchemy)
      ↓
Response
🏗️ System Architecture
Client / Frontend
        ↓
    FastAPI Application
        ↓
   Router Layer (Module Based)
        ↓
   RBAC Permission Layer
        ↓
   Service Layer (Business Logic)
        ↓
 Repository Layer (DB Operations)
        ↓
     Database (SQLAlchemy)
Architecture Explanation

Routers → Handle API requests

Permissions Layer → Validates role access

Services → Business logic implementation

Repositories → Database operations

Models → Database table structure

🔐 RBAC Permission Matrix
Feature	User	Admin	Super Admin
Login	✔	✔	✔
View Own Profile	✔	✔	✔
Update Own Profile	✔	✔	✔
View All Users	❌	✔	✔
Create Admin	❌	❌	✔
Delete User	Request Only	Request Only	✔
Lock / Unlock Account	Request Only	Request Only	✔
View Dashboard	❌	✔	✔
Update Any Profile	❌	✔	✔
🗄️ Database Connection Flow
FastAPI Request
        ↓
Depends(get_db)
        ↓
SQLAlchemy Session
        ↓
Model Operations
        ↓
Database Engine
🔄 Request Lifecycle
User Request
     ↓
Router
     ↓
JWT Authentication
     ↓
RBAC Permission Check
     ↓
Service Layer
     ↓
Repository Layer
     ↓
Database
     ↓
Response Returned
🗂 Project Structure
LSP_PROFILE_SETTING/
├── app/
│   ├── core/
│   │   ├── database.py
│   │   ├── permissions.py
│   │   └── default_data.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   └── change_request.py
│   │
│   ├── routes/
│   │   ├── auth.py
│   │   ├── admin.py
│   │   ├── user.py
│   │   ├── profile_read.py
│   │   └── profile_address.py
│   │
│   └── main.py
│
├── requirements.txt
├── .env
└── README.md
⚙️ Installation & Setup
# Create virtual environment
python -m venv venv

# Activate environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
uvicorn app.main:app --reload

Access API Documentation:

http://127.0.0.1:8000/docs
🧰 Tech Stack
Layer	Technology
Framework	FastAPI
Language	Python 3.10+
Database	SQLite / PostgreSQL
ORM	SQLAlchemy
Authentication	JWT
Validation	Pydantic
Server	Uvicorn
🔐 Authentication Flow
User Login
     ↓
Credential Validation
     ↓
JWT Token Generation
     ↓
Token Sent to Client
     ↓
Protected API Access
📊 Module Completion Summary
✔ Completed Features

JWT Authentication

Role Based Access Control (RBAC)

Super Admin functionality

Admin dashboard access

User profile management

Address settings module

Permission middleware

Modular router architecture

🚀 Future Enhancements

Email verification

OTP login

Notification system

Activity logs

Docker deployment

API rate limiting

Module 10 — Profile Settings & RBAC System
