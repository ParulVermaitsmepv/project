# School Management System

A comprehensive web-based school management system built with Flask, SQLAlchemy, and Bootstrap 5. This system provides role-based access for students, teaching staff, and administrative personnel.

## Features

### 🎓 For Students
- View personal dashboard with enrollment details
- Track pending and paid fees
- Online fees payment system
- Payment history tracking
- Real-time fee status updates

### 👨‍🏫 For Teaching Staff
- Manage assigned classes
- Enter and track student grades
- Mark attendance
- View class performance reports
- Send messages to students

### 👨‍💼 For Administrative Staff
- User management (add, edit, delete users)
- Fees management and tracking
- Financial reports and summaries
- System configuration
- Transaction history

### 🔐 Security Features
- Role-based access control (RBAC)
- Secure password hashing (Werkzeug)
- Session management with Flask-Login
- CSRF protection with Flask sessions
- Input validation and sanitization

## Technology Stack

- **Backend**: Flask 2.3.2
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Authentication**: Flask-Login
- **Security**: Werkzeug Password Hashing

## Project Structure

```
.
├── app.py                          # Main Flask application & routes
├── init_db.py                      # Database initialization script
├── requirements.txt                # Python dependencies
├── templates/                      # HTML templates
│   ├── base.html                  # Base template with navbar/footer
│   ├── index.html                 # Home page
│   ├── login.html                 # Login page
│   ├── student.html               # Student dashboard
│   ├── staff_teaching.html        # Teaching staff dashboard
│   ├── non_teaching_staff.html    # Administrative dashboard
│   ├── fees_payment.html          # Fees payment page
│   └── admin_users.html           # User management page
├── styles/
│   └── style.css                  # Custom CSS styles
└── school.db                       # SQLite database (created after init)
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
cd agents-project-base-setup-bootstrap-login
```

### Step 2: Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database
```bash
python init_db.py
```

This will:
- Create the SQLite database (`school.db`)
- Create all tables
- Insert sample users and fees records
- Display login credentials for testing

### Step 5: Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

## Default Login Credentials

After running `init_db.py`, use these credentials to test the system:

| Role | Username | Password |
|------|----------|----------|
| Student | student1 | password123 |
| Student | student2 | password123 |
| Student | student3 | password123 |
| Teaching Staff | staff1 | password123 |
| Teaching Staff | staff2 | password123 |
| Administrative | admin1 | password123 |

## Usage Guide

### For Students
1. Login with your student credentials
2. View your enrollment ID and fees status on the dashboard
3. Click "Pay Fees" to proceed with payment
4. Select payment method and enter amount
5. Complete the transaction

### For Teaching Staff
1. Login with your staff credentials
2. Access your assigned classes from the dashboard
3. Manage student grades and attendance
4. Generate performance reports

### For Administrative Staff
1. Login with admin credentials
2. Access "User Management" to manage system users
3. View financial summaries and transaction history
4. Configure system settings and generate reports

## Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: Email address
- `password_hash`: Hashed password
- `full_name`: User's full name
- `role`: User role (student, teaching_staff, non_teaching_staff)
- `enrollment_id`: For students
- `department`: For staff
- `created_at`: Account creation timestamp

### FeesRecord Table
- `id`: Primary key
- `user_id`: Foreign key to User
- `student_name`: Student name
- `amount`: Fee amount
- `due_date`: Due date for payment
- `paid_date`: Date when paid
- `status`: Payment status (pending, paid, overdue)
- `created_at`: Record creation timestamp

### FeeTransaction Table
- `id`: Primary key
- `fees_record_id`: Foreign key to FeesRecord
- `amount_paid`: Amount paid in transaction
- `payment_date`: Payment date
- `transaction_id`: Unique transaction ID
- `payment_method`: Online, cash, cheque, etc.

## Configuration

Edit `app.py` to modify:

```python
# Secret key for sessions (change in production!)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

# Database location
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
```

## API Endpoints

### Public Routes
- `GET /` - Home page
- `GET /login` - Login page
- `POST /login` - Handle login

### Student Routes (Requires login as student)
- `GET /student/dashboard` - Student dashboard
- `GET /fees` - Fees payment page
- `POST /api/pay-fees` - Process payment

### Teaching Staff Routes (Requires login as staff)
- `GET /teaching-staff/dashboard` - Staff dashboard

### Admin Routes (Requires login as admin)
- `GET /non-teaching-staff/dashboard` - Admin dashboard
- `GET /admin/users` - User management

### Common Routes
- `GET /logout` - Logout user

## Security Considerations

1. **Change Secret Key**: Update `app.config['SECRET_KEY']` before production
2. **Use HTTPS**: Deploy with SSL/TLS certificates
3. **Database Backup**: Regular backups of `school.db`
4. **Update Dependencies**: Keep Flask and libraries updated
5. **Input Validation**: All forms validate input server-side
6. **CSRF Protection**: Built-in Flask session protection

## Future Enhancements

- [ ] Email notifications for fee payments
- [ ] SMS reminders for overdue fees
- [ ] Advanced reporting and analytics
- [ ] Student attendance QR code system
- [ ] Parent portal access
- [ ] Mobile app integration
- [ ] Online exam system
- [ ] Digital assignment submission

## Troubleshooting

### Issue: Port 5000 already in use
```bash
python app.py --port 5001
```

### Issue: Database locked error
Delete `school.db` and run `python init_db.py` again

### Issue: Module not found
Ensure virtual environment is activated and dependencies installed:
```bash
pip install -r requirements.txt
```

## Support & Contact

For issues, questions, or suggestions:
- Create an issue in the repository
- Contact the development team
- Email: support@schoolmanagementsystem.edu

## License

This project is part of a school management system for educational purposes.

## Contributing

Contributions are welcome! Please follow these guidelines:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Last Updated**: July 2024  
**Version**: 1.0.0  
**Status**: Production Ready
