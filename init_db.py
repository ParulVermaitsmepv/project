"""
Database initialization script for School Management System
Creates sample users, classes, attendance, grades, notices, and fees records for testing
"""

import sys
sys.path.insert(0, '.')
from app import app, db, User, FeesRecord, FeeTransaction, ClassRoom, Enrollment, Attendance, Grade, Notice, SystemSetting
from datetime import datetime, timedelta, timezone

def init_database():
    with app.app_context():
        print("Dropping existing database tables and recreating schema...")
        db.drop_all()
        db.create_all()
        
        print("Creating sample users...")
        
        # 1. Create Students
        students_data = [
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
        
        for sdata in students_data:
            s = User(
                username=sdata['username'],
                email=sdata['email'],
                full_name=sdata['full_name'],
                role=sdata['role'],
                enrollment_id=sdata['enrollment_id']
            )
            s.set_password(sdata['password'])
            db.session.add(s)
        
        # 2. Create Teaching Staff
        teaching_staff_data = [
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
        
        for tdata in teaching_staff_data:
            t = User(
                username=tdata['username'],
                email=tdata['email'],
                full_name=tdata['full_name'],
                role=tdata['role'],
                department=tdata['department']
            )
            t.set_password(tdata['password'])
            db.session.add(t)
            
        # 3. Create Admin / Non-teaching staff
        admin = User(
            username='admin1',
            email='admin@school.edu',
            full_name='Admin User',
            role='non_teaching_staff',
            department='Administration'
        )
        admin.set_password('password123')
        db.session.add(admin)
        
        db.session.commit()
        
        student1 = User.query.filter_by(username='student1').first()
        student2 = User.query.filter_by(username='student2').first()
        student3 = User.query.filter_by(username='student3').first()
        staff1 = User.query.filter_by(username='staff1').first()
        staff2 = User.query.filter_by(username='staff2').first()
        
        print("Creating sample classrooms...")
        c1 = ClassRoom(name='Class 10-A', subject='Mathematics', teacher_id=staff1.id, schedule_time='09:00 AM - 10:00 AM')
        c2 = ClassRoom(name='Class 10-B', subject='Mathematics', teacher_id=staff1.id, schedule_time='10:15 AM - 11:15 AM')
        c3 = ClassRoom(name='Class 11-A', subject='Physics', teacher_id=staff2.id, schedule_time='11:30 AM - 12:30 PM')
        c4 = ClassRoom(name='Class 11-B', subject='Physics', teacher_id=staff2.id, schedule_time='02:00 PM - 03:00 PM')
        db.session.add_all([c1, c2, c3, c4])
        db.session.commit()

        # Enrollments
        db.session.add_all([
            Enrollment(student_id=student1.id, class_id=c1.id),
            Enrollment(student_id=student1.id, class_id=c3.id),
            Enrollment(student_id=student2.id, class_id=c1.id),
            Enrollment(student_id=student3.id, class_id=c2.id)
        ])

        print("Creating sample fees records & transactions...")
        today = datetime.now(timezone.utc)
        
        f1 = FeesRecord(user_id=student1.id, student_name=student1.full_name, amount=5000.00, due_date=today + timedelta(days=10), status='pending')
        f2 = FeesRecord(user_id=student2.id, student_name=student2.full_name, amount=5000.00, due_date=today - timedelta(days=5), status='overdue')
        f3 = FeesRecord(user_id=student3.id, student_name=student3.full_name, amount=5000.00, due_date=today - timedelta(days=30), status='paid', paid_date=today - timedelta(days=10))
        
        db.session.add_all([f1, f2, f3])
        db.session.commit()

        t3 = FeeTransaction(fees_record_id=f3.id, amount_paid=5000.00, payment_date=today - timedelta(days=10), transaction_id='TXN987654321', payment_method='online')
        db.session.add(t3)

        print("Creating sample attendance records...")
        for i in range(5):
            past_date = (today - timedelta(days=i)).date()
            db.session.add(Attendance(student_id=student1.id, class_id=c1.id, date=past_date, status='present'))
            db.session.add(Attendance(student_id=student2.id, class_id=c1.id, date=past_date, status='present' if i != 2 else 'absent'))
            db.session.add(Attendance(student_id=student3.id, class_id=c2.id, date=past_date, status='present'))

        print("Creating sample grades...")
        g1 = Grade(student_id=student1.id, class_id=c1.id, subject='Mathematics', exam_title='Midterm Exam', score=88.5, max_score=100.0, grade_letter='A')
        g2 = Grade(student_id=student1.id, class_id=c3.id, subject='Physics', exam_title='Quiz 1', score=92.0, max_score=100.0, grade_letter='A+')
        g3 = Grade(student_id=student2.id, class_id=c1.id, subject='Mathematics', exam_title='Midterm Exam', score=74.0, max_score=100.0, grade_letter='B')
        db.session.add_all([g1, g2, g3])

        print("Creating sample notices...")
        n1 = Notice(title='Annual Sports Meet 2024', content='The annual sports meet will be held next week. Registration open for all students.', category='Event', author_id=admin.id, target_role='all')
        n2 = Notice(title='Mathematics Assignment Deadline', content='Assignment 3 deadline has been extended to Friday 5:00 PM.', category='Academic', author_id=staff1.id, target_role='student')
        n3 = Notice(title='Staff Meeting on Monday', content='All teaching staff members are requested to join the department meeting at 3 PM in Conference Hall A.', category='Notice', author_id=admin.id, target_role='teaching_staff')
        db.session.add_all([n1, n2, n3])

        print("Creating default system settings...")
        s1 = SystemSetting(key='school_name', value='Greenwood High International School', description='School Name')
        s2 = SystemSetting(key='academic_year', value='2024 - 2025', description='Academic Year')
        s3 = SystemSetting(key='contact_email', value='admin@greenwood.edu', description='Contact Email')
        s4 = SystemSetting(key='default_fee', value='5000.00', description='Default Quarterly Tuition Fee')
        db.session.add_all([s1, s2, s3, s4])

        db.session.commit()
        print("Database successfully initialized with full sample data!")

if __name__ == '__main__':
    init_database()
