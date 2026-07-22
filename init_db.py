"""
Database initialization script for School Management System
Creates sample users and fees records for testing
"""

import sys
sys.path.insert(0, '.')
from app import app, db, User, FeesRecord
from datetime import datetime, timedelta

def init_database():
    with app.app_context():
        # Drop all tables and recreate
        print("Creating database tables...")
        db.create_all()
        
        # Check if users already exist
        if User.query.first() is not None:
            print("Database already initialized. Skipping sample data creation.")
            return
        
        print("Creating sample users...")
        
        # Create sample students
        students = [
            {
                'username': 'student1',
                'email': 'student1@school.edu',
                'full_name': 'Raj Kumar',
                'role': 'student',
                'enrollment_id': 'STU001',
                'password': 'password123'
            },
            {
                'username': 'student2',
                'email': 'student2@school.edu',
                'full_name': 'Priya Singh',
                'role': 'student',
                'enrollment_id': 'STU002',
                'password': 'password123'
            },
            {
                'username': 'student3',
                'email': 'student3@school.edu',
                'full_name': 'Arjun Patel',
                'role': 'student',
                'enrollment_id': 'STU003',
                'password': 'password123'
            }
        ]
        
        for student_data in students:
            student = User(
                username=student_data['username'],
                email=student_data['email'],
                full_name=student_data['full_name'],
                role=student_data['role'],
                enrollment_id=student_data['enrollment_id']
            )
            student.set_password(student_data['password'])
            db.session.add(student)
        
        db.session.flush()
        student1 = User.query.filter_by(username='student1').first()
        student2 = User.query.filter_by(username='student2').first()
        student3 = User.query.filter_by(username='student3').first()
        
        # Create sample teaching staff
        teaching_staff = [
            {
                'username': 'staff1',
                'email': 'staff1@school.edu',
                'full_name': 'Mr. Sharma',
                'role': 'teaching_staff',
                'department': 'Mathematics',
                'password': 'password123'
            },
            {
                'username': 'staff2',
                'email': 'staff2@school.edu',
                'full_name': 'Ms. Verma',
                'role': 'teaching_staff',
                'department': 'Science',
                'password': 'password123'
            }
        ]
        
        for staff_data in teaching_staff:
            staff = User(
                username=staff_data['username'],
                email=staff_data['email'],
                full_name=staff_data['full_name'],
                role=staff_data['role'],
                department=staff_data['department']
            )
            staff.set_password(staff_data['password'])
            db.session.add(staff)
        
        # Create sample non-teaching staff (admin)
        admin = User(
            username='admin1',
            email='admin@school.edu',
            full_name='Admin User',
            role='non_teaching_staff',
            department='Administration'
        )
        admin.set_password('password123')
        db.session.add(admin)
        
        db.session.flush()
        
        print("Creating sample fees records...")
        
        # Create fees records for students
        today = datetime.utcnow()
        fees_records = [
            {
                'student_id': student1.id,
                'student_name': student1.full_name,
                'amount': 5000.00,
                'due_date': today + timedelta(days=10),
                'status': 'pending'
            },
            {
                'student_id': student2.id,
                'student_name': student2.full_name,
                'amount': 5000.00,
                'due_date': today - timedelta(days=5),
                'status': 'overdue'
            },
            {
                'student_id': student3.id,
                'student_name': student3.full_name,
                'amount': 5000.00,
                'due_date': today - timedelta(days=30),
                'status': 'paid',
                'paid_date': today - timedelta(days=10)
            }
        ]
        
        for fee_data in fees_records:
            fee = FeesRecord(
                user_id=fee_data['student_id'],
                student_name=fee_data['student_name'],
                amount=fee_data['amount'],
                due_date=fee_data['due_date'],
                status=fee_data['status']
            )
            if fee_data['status'] == 'paid':
                fee.paid_date = fee_data.get('paid_date')
            db.session.add(fee)
        
        db.session.commit()
        print("✓ Database initialization completed successfully!")
        print("\nSample Login Credentials:")
        print("-" * 50)
        print("Student: student1 / password123")
        print("Student: student2 / password123")
        print("Teaching Staff: staff1 / password123")
        print("Admin: admin1 / password123")
        print("-" * 50)

if __name__ == '__main__':
    init_database()
