# Comprehensive Bootstrap CSS Integration & General Backend Implementation Plan

Enhance the School Management System by converting all hardcoded/mock UI interactions into fully functional, general backend operations. Standardize styling with Bootstrap 5 and custom CSS, and add complete CRUD capabilities across Student, Teaching Staff, and Administrative user roles.

## User Review Required

> [!IMPORTANT]
> - Database schema will be updated to include new tables (`ClassRoom`, `Enrollment`, `Attendance`, `Grade`, `Notice`, `SystemSetting`). Running `init_db.py` will initialize default data and sample classes, grades, and attendance records.
> - All UI modals (Add User, Edit User, Delete User, Enter Grades, Mark Attendance, System Settings, Fees Creation) will now be connected to dynamic Flask backend REST APIs.

## Open Questions

None. The features align directly with the user prompt to make the backend complete, generalized, and fully interactive using Bootstrap CSS.

## Proposed Changes

---

### Backend & Database Models

#### [MODIFY] [app.py](file:///c:/New%20folder/project/app.py)
- **New DB Models**:
  - `ClassRoom`: Class name, section, subject, teacher_id (ForeignKey to User).
  - `Enrollment`: Student enrollment in a ClassRoom.
  - `Attendance`: Date, student_id, class_id, status (`present`/`absent`/`late`), remarks.
  - `Grade`: Student_id, class_id, subject, exam_title, score, max_score, grade_letter.
  - `Notice`: Title, content, category, author_id, target_role, created_at.
  - `SystemSetting`: Key-value pairs for configurable school settings (e.g. school name, session year, contact email).
- **Generalized REST APIs & Routes**:
  - **User Management**: `POST /api/users/add`, `POST /api/users/edit/<id>`, `POST /api/users/delete/<id>`, `GET /admin/users/export`.
  - **Fees Management**: `POST /api/fees/create`, `GET /api/fees/list`, existing `POST /api/pay-fees`.
  - **Class & Student Management**: `GET /api/classes`, `POST /api/classes/create`.
  - **Attendance Management**: `POST /api/attendance/mark`, `GET /api/attendance/class/<id>`.
  - **Grade Management**: `POST /api/grades/submit`, `GET /api/grades/student/<id>`.
  - **Notices Management**: `POST /api/notices/create`, `POST /api/notices/delete/<id>`.
  - **Settings & Profile**: `GET/POST /profile`, `POST /api/settings/update`.

#### [MODIFY] [init_db.py](file:///c:/New%20folder/project/init_db.py)
- Seed database with full sample data: users across all 3 roles, classes, fee records, fee transactions, grades, attendance records, notices, and default system settings.

---

### Styling & Design System

#### [MODIFY] [style.css](file:///c:/New%20folder/project/styles/style.css)
- Refine Bootstrap 5 extensions: color variables, modern card elevations, glassmorphism highlights, custom table hover effects, responsive modal styling, and badge styling.

#### [MODIFY] [base.html](file:///c:/New%20folder/project/templates/base.html)
- Standardize Bootstrap 5 layout container structure, dynamic flash messages, active link indicators, profile menu dropdown, and modern footer styling.

---

### Dashboards & Views

#### [MODIFY] [student.html](file:///c:/New%20folder/project/templates/student.html)
- Wire real data for attendance, grades, notices, and fee payments.

#### [MODIFY] [staff_teaching.html](file:///c:/New%20folder/project/templates/staff_teaching.html)
- Add interactive Bootstrap modals for **Enter Grades**, **Mark Attendance**, and **View Class Reports**. Connect them to Flask backend endpoints with JavaScript `fetch()`.

#### [MODIFY] [non_teaching_staff.html](file:///c:/New%20folder/project/templates/non_teaching_staff.html)
- Add interactive Bootstrap modals for **Fees Management**, **System Settings**, **Notices Creation**, and real dynamic financial summaries.

#### [MODIFY] [admin_users.html](file:///c:/New%20folder/project/templates/admin_users.html)
- Wire **Add User**, **Edit User**, **Delete User**, and **Export CSV/JSON** modals to backend API endpoints.

#### [NEW] [profile.html](file:///c:/New%20folder/project/templates/profile.html)
- User profile & password update page.

---

## Verification Plan

### Automated Tests
- Run `python init_db.py` to ensure schema creation and seed data execution work without error.
- Run `python app.py` and verify all endpoints response codes.

### Manual Verification
- Test user logins:
  - Student (`student1` / `password123`)
  - Teaching Staff (`staff1` / `password123`)
  - Admin (`admin1` / `password123`)
- Test CRUD actions: Add/Edit/Delete user, Pay fee, Submit grade, Mark attendance, Create notice, Update settings.
