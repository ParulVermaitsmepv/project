# 🏫 School Management System

> A comprehensive, web-based school management application built with **Flask**, **SQLAlchemy**, **SQLite**, and **Bootstrap 5**, providing role-based portals for **Students**, **Teaching Staff**, and **Administrative / Non-Teaching Staff**.

---

## 📊 1. Current Progress & Status Overview

### Overall Project Completion: **100% Core MVP Completed**

| Feature / Module | Status | Progress | Description |
| :--- | :---: | :---: | :--- |
| **Authentication & RBAC** | ✅ Completed | 100% | Multi-role login (Student, Staff, Admin), password hashing, session management, route protection. |
| **Student Dashboard** | ✅ Completed | 100% | Fee status tracking, attendance metrics, academic grades history, interactive notice board. |
| **Fees & Payment System** | ✅ Completed | 100% | Online fee payment gateway, transaction logs, payment method selector, real-time status update. |
| **Teaching Staff Portal** | ✅ Completed | 100% | Class schedules, grade entry with letter grading auto-calc, attendance marking, notice broadcasting. |
| **Admin & User Management** | ✅ Completed | 100% | CRUD operation for all users, JSON data export, automatic fee initialization for students. |
| **Financial & System Analytics**| ✅ Completed | 100% | Collection metrics, pending fee summary, transaction logs, system settings configuration. |
| **Notice Board & Announcements**| ✅ Completed | 100% | Role-targeted announcements (All, Student, Staff) with real-time dynamic display. |
| **RESTful API Backend** | ✅ Completed | 100% | Full JSON APIs for users, fees, grades, attendance, notices, and configuration settings. |
| **Notifications (Email/SMS)** | ⏳ Roadmap (Phase 2) | 0% | Planned automated email/SMS reminders for fee payment & attendance alerts. |
| **Parent Portal & QR Attendance**| ⏳ Roadmap (Phase 2) | 0% | Planned parent dashboard view & automated QR code attendance scanning. |

---

## 🔄 2. System Flow Sequences & Diagrams

### 2.1 System High-Level Architecture Flow
```mermaid
graph TD
    Client["🌐 Client Browser (Bootstrap 5 UI & JS Fetch)"]
    Router["🔀 Flask Application (app.py)"]
    AuthManager["🔒 Login Manager & RBAC Middleware"]
    
    subgraph Services ["Backend Controllers & Logic"]
        UserSvc["User Management Service"]
        FeeSvc["Fee Payment & Transaction Service"]
        AcadSvc["Grades & Attendance Service"]
        NoticeSvc["Notice & Settings Service"]
    end

    ORM["⚙️ SQLAlchemy ORM Models"]
    DB[("💾 SQLite Database (school.db)")]

    Client -->|HTTP Requests| Router
    Router --> AuthManager
    AuthManager -->|Validated Access| Services
    Services --> ORM
    ORM -->|SQL Queries| DB
```

---

### 2.2 User Authentication & Role Routing Flow Sequence
```mermaid
sequenceDiagram
    autonumber
    actor User as 👤 User / Student / Staff / Admin
    participant Browser as 🌐 Client Browser
    participant App as 🐍 Flask app.py
    participant Auth as 🔒 Flask-Login
    participant DB as 💾 SQLite DB

    User->>Browser: Enter Username, Password & Select Role
    Browser->>App: POST /login (username, password, user_type)
    App->>DB: Query User record by username
    DB-->>App: Return User object (with hashed password & role)
    
    alt Invalid Credentials or Role Mismatch
        App-->>Browser: Render login.html with error message
        Browser-->>User: Display "Invalid credentials or user role selection"
    else Valid Credentials
        App->>Auth: login_user(user) & create session cookie
        App-->>Browser: Redirect to / (Home route)
        
        alt Role == 'student'
            Browser->>App: GET /student/dashboard
            App-->>Browser: Render student.html
        else Role == 'teaching_staff'
            Browser->>App: GET /teaching-staff/dashboard
            App-->>Browser: Render staff_teaching.html
        else Role == 'non_teaching_staff'
            Browser->>App: GET /non-teaching-staff/dashboard
            App-->>Browser: Render non_teaching_staff.html
        end
        Browser-->>User: Display Dashboard Home
    end
```

---

### 2.3 Student Fee Payment Flow Sequence
```mermaid
sequenceDiagram
    autonumber
    actor Student as 🎓 Student
    participant Browser as 🌐 Client Browser
    participant App as 🐍 Flask app.py
    participant DB as 💾 SQLite DB

    Student->>Browser: Navigate to Fees Payment Page (/fees)
    Browser->>App: GET /fees (Authenticated as Student)
    App->>DB: Fetch FeesRecord for current_user.id
    DB-->>App: Return FeesRecord (amount, status, due_date)
    App-->>Browser: Render fees_payment.html
    
    Student->>Browser: Enter Payment Amount & Select Payment Method (UPI, Online, Cash, etc.)
    Student->>Browser: Click "Proceed to Pay"
    Browser->>App: POST /api/pay-fees {fees_id, amount, payment_method}
    
    App->>DB: Fetch FeesRecord & Create new FeeTransaction record
    alt Amount Paid >= Fees Amount
        App->>DB: Update FeesRecord status = 'paid', paid_date = NOW()
    end
    App->>DB: Commit DB Session
    DB-->>App: Transaction Saved
    
    App-->>Browser: Return JSON {success: true, message: 'Payment processed successfully'}
    Browser-->>Student: Show Success Alert & Refresh Dashboard Metrics
```

---

### 2.4 Teaching Staff Grade & Attendance Marking Flow Sequence
```mermaid
sequenceDiagram
    autonumber
    actor Teacher as 👨‍🏫 Teaching Staff
    participant Browser as 🌐 Client Browser
    participant App as 🐍 Flask app.py
    participant DB as 💾 SQLite DB

    Teacher->>Browser: Select Class & View Enrolled Students
    Browser->>App: GET /teaching-staff/dashboard
    App->>DB: Query ClassRoom, Enrollments & Students
    DB-->>App: Return Class & Student lists
    App-->>Browser: Render staff_teaching.html

    rect rgb(240, 248, 255)
        note over Teacher, DB: Grade Submission Workflow
        Teacher->>Browser: Enter Marks (Score, Max Score, Exam Title, Subject)
        Teacher->>Browser: Click "Submit Grade"
        Browser->>App: POST /api/grades/submit {student_id, subject, exam_title, score, max_score}
        App->>App: Calculate Percentage & Auto-assign Grade Letter (A+, A, B, C, D, F)
        App->>DB: Insert new Grade record
        App->>DB: Commit DB Session
        App-->>Browser: Return JSON {success: true, grade_letter: 'A+'}
        Browser-->>Teacher: Display Updated Grade List
    end

    rect rgb(255, 245, 238)
        note over Teacher, DB: Attendance Marking Workflow
        Teacher->>Browser: Select Attendance Status (Present / Absent / Late) for Student
        Teacher->>Browser: Click "Mark Attendance"
        Browser->>App: POST /api/attendance/mark {student_id, class_id, status, remarks}
        App->>DB: Insert new Attendance record
        App->>DB: Commit DB Session
        App-->>Browser: Return JSON {success: true, message: 'Attendance marked successfully'}
        Browser-->>Teacher: Update Attendance Status Indicator
    end
```

---

### 2.5 Admin User Management & System Configuration Flow Sequence
```mermaid
sequenceDiagram
    autonumber
    actor Admin as 👨‍💼 Administrator
    participant Browser as 🌐 Client Browser
    participant App as 🐍 Flask app.py
    participant DB as 💾 SQLite DB

    Admin->>Browser: Open User Management (/admin/users)
    Browser->>App: GET /admin/users
    App->>DB: Query all Users (Students, Teaching Staff, Admin)
    DB-->>App: Return User lists
    App-->>Browser: Render admin_users.html

    alt Add New User
        Admin->>Browser: Submit "Add User" Form
        Browser->>App: POST /api/users/add {username, email, role, full_name, ...}
        App->>DB: Create User record with hashed password
        opt User Role == 'student'
            App->>DB: Automatically create default FeesRecord ($5000 pending)
        end
        App->>DB: Commit DB Session
        App-->>Browser: Return JSON {success: true, user: {...}}
    else Export User Data
        Admin->>Browser: Click "Export Users JSON"
        Browser->>App: GET /admin/users/export
        App->>DB: Query all users & convert to JSON payload
        DB-->>App: Return JSON list
        App-->>Browser: Download `users_export.json` attachment
    else Delete User
        Admin->>Browser: Click "Delete User"
        Browser->>App: POST /api/users/delete/<id>
        App->>DB: Cascading delete associated Fees, Grades, Attendance & Enrollments
        App->>DB: Delete User record
        App->>DB: Commit DB Session
        App-->>Browser: Return JSON {success: true}
    end
```

---

### 2.6 Data Flow Diagram (DFD Level-1)
```mermaid
flowchart LR
    subgraph External Entities
        Student["🎓 Student"]
        Teacher["👨‍🏫 Teaching Staff"]
        Admin["👨‍💼 Admin Staff"]
    end

    subgraph System Processes
        P1["1.0 Auth & Access Control"]
        P2["2.0 Fee Tracking & Payment Engine"]
        P3["3.0 Academic & Attendance Management"]
        P4["4.0 User Administration & Config"]
        P5["5.0 Notice & Broadcast System"]
    end

    subgraph Data Stores
        D1[("D1: Users Store")]
        D2[("D2: Fees & Transactions Store")]
        D3[("D3: Academic Records Store")]
        D4[("D4: System Settings Store")]
        D5[("D5: Notices Store")]
    end

    Student -->|Login Credentials| P1
    Teacher -->|Login Credentials| P1
    Admin -->|Login Credentials| P1
    P1 <-->|Read / Verify| D1

    Student -->|Pay Fee Request| P2
    P2 <-->|Read / Write Status| D2
    
    Teacher -->|Grades & Attendance Input| P3
    P3 <-->|Store Grades / Attendance| D3

    Admin -->|Add/Edit/Delete User & Export| P4
    P4 <-->|Manage Users| D1
    P4 <-->|Manage Settings| D4

    Admin & Teacher -->|Post Announcement| P5
    P5 <-->|Store & Query Notices| D5
```

---

## 🗄️ 3. Database Schema Entity-Relationship Model

```mermaid
erDiagram
    User ||--o{ FeesRecord : "has fee records"
    User ||--o{ FeeTransaction : "initiates transactions"
    User ||--o{ ClassRoom : "teaches classes"
    User ||--o{ Enrollment : "enrolled in"
    User ||--o{ Attendance : "has attendance"
    User ||--o{ Grade : "receives grades"
    User ||--o{ Notice : "authors notices"

    FeesRecord ||--o{ FeeTransaction : "has transactions"
    ClassRoom ||--o{ Enrollment : "contains enrolled students"
    ClassRoom ||--o{ Attendance : "holds attendance"
    ClassRoom ||--o{ Grade : "holds exam grades"

    User {
        int id PK
        string username UK
        string email UK
        string password_hash
        string full_name
        string role "student | teaching_staff | non_teaching_staff"
        string enrollment_id UK
        string department
        datetime created_at
    }

    FeesRecord {
        int id PK
        int user_id FK
        string student_name
        float amount
        datetime due_date
        datetime paid_date
        string status "pending | paid | overdue"
        datetime created_at
    }

    FeeTransaction {
        int id PK
        int fees_record_id FK
        float amount_paid
        datetime payment_date
        string transaction_id UK
        string payment_method "online | cash | cheque | upi"
        text notes
    }

    ClassRoom {
        int id PK
        string name
        string subject
        int teacher_id FK
        string schedule_time
    }

    Grade {
        int id PK
        int student_id FK
        int class_id FK
        string subject
        string exam_title
        float score
        float max_score
        string grade_letter "A+ | A | B | C | D | F"
    }
```

---

## 💻 4. Technology Stack & Project Structure

### Technology Stack
- **Backend Framework**: Python Flask (v2.3.2)
- **Database & ORM**: SQLite + Flask-SQLAlchemy
- **Authentication**: Flask-Login + Werkzeug Security (SHA-256 Password Hashing)
- **Frontend Layer**: HTML5, Custom CSS3, Bootstrap 5, JavaScript (Fetch API)
- **Data Export**: Built-in JSON streaming service

### Directory Structure
```
project/
├── app.py                          # Main Flask application, ORM models & API routes
├── config.py                       # Application configuration settings
├── init_db.py                      # Database initialization & sample data generator
├── wsgi.py                         # WSGI production server entry point
├── requirements.txt                # Python package dependencies
├── readme.md                       # Complete documentation & flow sequence diagrams
├── PROJECT_SUMMARY.md              # Project status and completion log
├── QUICK_START.md                  # Detailed setup and launch instructions
│
├── templates/                      # Jinja2 HTML Templates
│   ├── base.html                  # Master layout with responsive navbar & footer
│   ├── index.html                 # Public landing home page
│   ├── login.html                 # Multi-role authentication page
│   ├── student.html               # Student dashboard
│   ├── staff_teaching.html        # Teaching staff dashboard
│   ├── non_teaching_staff.html    # Administrative staff dashboard
│   ├── fees_payment.html          # Student fee payment portal
│   ├── admin_users.html           # User management portal
│   └── profile.html               # User profile & password update page
│
├── styles/
│   └── style.css                  # Custom CSS styles, themes & responsive layouts
│
└── school.db                       # SQLite database instance (generated on setup)
```

---

## ⚡ 5. REST API Endpoints Reference

| Category | Endpoint | Method | Required Access | Description |
| :--- | :--- | :---: | :---: | :--- |
| **Authentication** | `/login` | `GET / POST` | Public | Authenticate user credentials and assign session |
| | `/logout` | `GET` | Authenticated | Destroy current active session |
| | `/profile` | `GET / POST` | Authenticated | View profile & change password |
| **Student** | `/student/dashboard` | `GET` | Student | View student metrics, grades, attendance & fees |
| | `/fees` | `GET` | Student | Access student fee details & payment modal |
| | `/api/pay-fees` | `POST` | Student | Process fee payment transaction |
| **Teaching Staff** | `/teaching-staff/dashboard` | `GET` | Teaching Staff | Access assigned classes & student rosters |
| | `/api/grades/submit` | `POST` | Staff / Admin | Record grades & auto-calculate grade letters |
| | `/api/attendance/mark` | `POST` | Staff / Admin | Record student attendance status |
| **Admin** | `/non-teaching-staff/dashboard`| `GET` | Admin Staff | View financial overview & transaction metrics |
| | `/admin/users` | `GET` | Admin Staff | View & manage user accounts |
| | `/api/users/add` | `POST` | Admin Staff | Add new user (auto-creates fee record if student) |
| | `/api/users/edit/<id>` | `POST` | Admin Staff | Update user account details |
| | `/api/users/delete/<id>` | `POST` | Admin Staff | Delete user account & clear dependent data |
| | `/admin/users/export` | `GET` | Admin Staff | Download user records as JSON format |
| | `/api/fees/create` | `POST` | Admin Staff | Issue new fee record for a student |
| | `/api/notices/create` | `POST` | Staff / Admin | Post announcement to notice board |
| | `/api/settings/update` | `POST` | Admin Staff | Update system settings |

---

## 🚀 6. Installation & Quick Start Guide

### Step 1: Environment Setup
```bash
# Navigate to the project directory
cd project

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
# On macOS/Linux:
source .venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Initialize Database with Seed Data
```bash
python init_db.py
```
> This creates `school.db`, builds database tables, and populates initial sample users, classes, grades, attendance, fees, and notices.

### Step 4: Run Application
```bash
python app.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

---

## 🗝️ 7. Default Demo Credentials

| Role | Username | Password | Access Rights |
| :--- | :--- | :--- | :--- |
| **Student** | `student1` | `password123` | Student Dashboard, Fees Payment, Grades View |
| **Student** | `student2` | `password123` | Student Dashboard (Overdue status sample) |
| **Student** | `student3` | `password123` | Student Dashboard (Paid status sample) |
| **Teaching Staff** | `staff1` | `password123` | Math Classes, Mark Attendance, Grade Entry |
| **Teaching Staff** | `staff2` | `password123` | Physics Classes, Attendance, Grade Entry |
| **Administrator** | `admin1` | `password123` | Full System Access, User CRUD, Financial Reports |

---

## 🔮 8. Roadmap & Future Enhancements

- [ ] **Automated Email & SMS Alerts**: Send instant notifications upon fee receipt generation or overdue dates.
- [ ] **QR Code Attendance System**: Allow teachers to take attendance via mobile camera QR scanning.
- [ ] **Parent Portal Module**: Dedicated portal for parents to track attendance, report cards, and pay fees.
- [ ] **Online Examination System**: Multiple choice & quiz engine integrated with auto-grading.
- [ ] **PDF Receipt Generator**: Export formal fee payment receipts and student ID cards in PDF format.
