from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone, timedelta
import io
import json

app = Flask(__name__, static_folder='styles', static_url_path='/static')
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.context_processor
def inject_now():
    return {'now': datetime.now(timezone.utc)}


# ==========================================
# Database Models
# ==========================================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # student, teaching_staff, non_teaching_staff
    enrollment_id = db.Column(db.String(100), unique=True, nullable=True)
    department = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'enrollment_id': self.enrollment_id,
            'department': self.department,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else ''
        }


class FeesRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    student_name = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    paid_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, paid, overdue
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', backref=db.backref('fees', lazy=True))


class FeeTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fees_record_id = db.Column(db.Integer, db.ForeignKey('fees_record.id'), nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    transaction_id = db.Column(db.String(100), unique=True)
    payment_method = db.Column(db.String(50))  # online, cash, cheque, credit_card, upi
    notes = db.Column(db.Text)

    fees_record = db.relationship('FeesRecord', backref=db.backref('transactions', lazy=True))


class ClassRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # e.g., Class 10-A
    subject = db.Column(db.String(100), nullable=False)  # e.g., Mathematics
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    schedule_time = db.Column(db.String(100), default='09:00 AM - 10:00 AM')

    teacher = db.relationship('User', backref=db.backref('taught_classes', lazy=True))


class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class_room.id'), nullable=False)

    student = db.relationship('User', backref=db.backref('enrollments', lazy=True))
    classroom = db.relationship('ClassRoom', backref=db.backref('enrolled_students', lazy=True))


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class_room.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=lambda: datetime.now(timezone.utc).date())
    status = db.Column(db.String(20), nullable=False)  # present, absent, late
    remarks = db.Column(db.String(255), nullable=True)

    student = db.relationship('User', backref=db.backref('attendances', lazy=True))
    classroom = db.relationship('ClassRoom', backref=db.backref('attendance_records', lazy=True))


class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class_room.id'), nullable=True)
    subject = db.Column(db.String(100), nullable=False)
    exam_title = db.Column(db.String(100), nullable=False)  # e.g., Midterm, Final Exam, Quiz 1
    score = db.Column(db.Float, nullable=False)
    max_score = db.Column(db.Float, default=100.0)
    grade_letter = db.Column(db.String(10), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    student = db.relationship('User', backref=db.backref('grades', lazy=True))
    classroom = db.relationship('ClassRoom', backref=db.backref('class_grades', lazy=True))


class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default='General')  # Academic, Exam, Notice, Urgent
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    target_role = db.Column(db.String(50), default='all')  # all, student, teaching_staff
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    author = db.relationship('User', backref=db.backref('notices', lazy=True))


class SystemSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(255), nullable=True)


@login_manager.user_loader
def load_user(user_id: str) -> User | None:
    return User.query.get(int(user_id))


# ==========================================
# Authentication & Main Routes
# ==========================================

@app.route('/')
def home():
    if current_user.is_authenticated:
        if current_user.role == 'student':
            return redirect(url_for('student_dashboard'))
        elif current_user.role == 'teaching_staff':
            return redirect(url_for('teaching_staff_dashboard'))
        else:
            return redirect(url_for('non_teaching_staff_dashboard'))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_type = request.form.get('user_type')

        user = User.query.filter_by(username=username).first()

        if user and (not user_type or user.role == user_type) and user.check_password(password):
            login_user(user)
            flash(f'Welcome back, {user.full_name}!', 'success')
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid credentials or user role selection')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not current_user.check_password(current_password):
            flash('Current password is incorrect.', 'error')
        elif new_password != confirm_password:
            flash('New passwords do not match.', 'error')
        elif len(new_password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
        else:
            current_user.set_password(new_password)
            db.session.commit()
            flash('Password updated successfully!', 'success')

    return render_template('profile.html', user=current_user)


# ==========================================
# Dashboards
# ==========================================

@app.route('/student/dashboard')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        return redirect(url_for('home'))

    fees = FeesRecord.query.filter_by(user_id=current_user.id).all()
    total_due = sum(f.amount for f in fees if f.status in ['pending', 'overdue'])
    
    # Student specific details
    grades = Grade.query.filter_by(student_id=current_user.id).all()
    attendances = Attendance.query.filter_by(student_id=current_user.id).all()
    total_classes = len(attendances)
    present_count = sum(1 for a in attendances if a.status == 'present')
    attendance_rate = round((present_count / total_classes * 100), 1) if total_classes > 0 else 100.0

    notices = Notice.query.filter(Notice.target_role.in_(['all', 'student'])).order_by(Notice.created_at.desc()).limit(5).all()

    return render_template(
        'student.html', 
        user=current_user, 
        fees=fees, 
        total_due=total_due,
        grades=grades,
        attendances=attendances,
        attendance_rate=attendance_rate,
        notices=notices
    )


@app.route('/teaching-staff/dashboard')
@login_required
def teaching_staff_dashboard():
    if current_user.role != 'teaching_staff':
        return redirect(url_for('home'))

    my_classes = ClassRoom.query.filter_by(teacher_id=current_user.id).all()
    all_students = User.query.filter_by(role='student').all()
    notices = Notice.query.filter(Notice.target_role.in_(['all', 'teaching_staff'])).order_by(Notice.created_at.desc()).limit(5).all()

    # Calculate metrics
    total_students_taught = len(set(
        enroll.student_id 
        for c in my_classes 
        for enroll in c.enrolled_students
    )) if my_classes else len(all_students)

    recent_grades = Grade.query.order_by(Grade.created_at.desc()).limit(5).all()

    return render_template(
        'staff_teaching.html', 
        user=current_user, 
        classes=my_classes,
        students=all_students,
        total_students=total_students_taught,
        notices=notices,
        recent_grades=recent_grades
    )


@app.route('/non-teaching-staff/dashboard')
@login_required
def non_teaching_staff_dashboard():
    if current_user.role != 'non_teaching_staff':
        return redirect(url_for('home'))

    students_count = User.query.filter_by(role='student').count()
    teaching_staff_count = User.query.filter_by(role='teaching_staff').count()
    all_fees = FeesRecord.query.all()
    
    total_collected = sum(f.amount for f in all_fees if f.status == 'paid')
    total_pending = sum(f.amount for f in all_fees if f.status in ['pending', 'overdue'])

    recent_transactions = FeeTransaction.query.order_by(FeeTransaction.payment_date.desc()).limit(5).all()
    notices = Notice.query.order_by(Notice.created_at.desc()).limit(5).all()
    settings = {s.key: s.value for s in SystemSetting.query.all()}

    return render_template(
        'non_teaching_staff.html', 
        user=current_user,
        students_count=students_count,
        staff_count=teaching_staff_count,
        total_collected=total_collected,
        total_pending=total_pending,
        recent_transactions=recent_transactions,
        notices=notices,
        settings=settings
    )


@app.route('/fees')
@login_required
def fees():
    if current_user.role != 'student':
        return redirect(url_for('home'))
    fees_record = FeesRecord.query.filter_by(user_id=current_user.id).first()
    return render_template('fees_payment.html', user=current_user, fees=fees_record)


@app.route('/admin/users')
@login_required
def admin_users():
    if current_user.role != 'non_teaching_staff':
        return redirect(url_for('home'))
    
    students = User.query.filter_by(role='student').all()
    teaching_staff = User.query.filter_by(role='teaching_staff').all()
    admin_staff = User.query.filter_by(role='non_teaching_staff').all()
    
    return render_template(
        'admin_users.html', 
        students=students, 
        teaching_staff=teaching_staff,
        admin_staff=admin_staff,
        user=current_user
    )


# ==========================================
# REST API Endpoints for Complete Functionality
# ==========================================

# 1. User Management APIs
@app.route('/api/users/add', methods=['POST'])
@login_required
def add_user():
    if current_user.role != 'non_teaching_staff':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    data = request.get_json() or request.form
    username = data.get('username')
    email = data.get('email')
    full_name = data.get('full_name')
    role = data.get('role')
    password = data.get('password', 'password123')
    enrollment_id = data.get('enrollment_id')
    department = data.get('department')

    if User.query.filter_by(username=username).first():
        return jsonify({'success': False, 'message': 'Username already exists'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'success': False, 'message': 'Email already exists'}), 400

    new_user = User(
        username=username,
        email=email,
        full_name=full_name,
        role=role,
        enrollment_id=enrollment_id if role == 'student' else None,
        department=department if role != 'student' else None
    )
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    # If student, create default fees record
    if role == 'student':
        fee = FeesRecord(
            user_id=new_user.id,
            student_name=new_user.full_name,
            amount=5000.0,
            due_date=datetime.now(timezone.utc) + timedelta(days=30),
            status='pending'
        )
        db.session.add(fee)
        db.session.commit()

    return jsonify({'success': True, 'message': 'User added successfully', 'user': new_user.to_dict()})


@app.route('/api/users/edit/<int:user_id>', methods=['POST'])
@login_required
def edit_user(user_id):
    if current_user.role != 'non_teaching_staff':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    target_user = User.query.get_or_404(user_id)
    data = request.get_json() or request.form

    target_user.full_name = data.get('full_name', target_user.full_name)
    target_user.email = data.get('email', target_user.email)
    target_user.username = data.get('username', target_user.username)
    if 'department' in data and data['department']:
        target_user.department = data['department']
    if 'enrollment_id' in data and data['enrollment_id']:
        target_user.enrollment_id = data['enrollment_id']

    db.session.commit()
    return jsonify({'success': True, 'message': 'User updated successfully'})


@app.route('/api/users/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'non_teaching_staff':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    if user_id == current_user.id:
        return jsonify({'success': False, 'message': 'Cannot delete your own active session account'}), 400

    target_user = User.query.get_or_404(user_id)
    # Clean dependent records
    FeesRecord.query.filter_by(user_id=user_id).delete()
    Grade.query.filter_by(student_id=user_id).delete()
    Attendance.query.filter_by(student_id=user_id).delete()
    Enrollment.query.filter_by(student_id=user_id).delete()

    db.session.delete(target_user)
    db.session.commit()
    return jsonify({'success': True, 'message': 'User deleted successfully'})


@app.route('/admin/users/export')
@login_required
def export_users():
    if current_user.role != 'non_teaching_staff':
        return redirect(url_for('home'))

    users = User.query.all()
    user_list = [u.to_dict() for u in users]
    
    mem = io.BytesIO()
    mem.write(json.dumps(user_list, indent=2).encode('utf-8'))
    mem.seek(0)
    
    return send_file(
        mem,
        mimetype='application/json',
        as_attachment=True,
        download_name='users_export.json'
    )


# 2. Fees APIs
@app.route('/api/pay-fees', methods=['POST'])
@login_required
def pay_fees():
    if current_user.role != 'student':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    data = request.get_json()
    amount = float(data.get('amount', 0))
    fees_id = data.get('fees_id')

    fees_record = FeesRecord.query.get(fees_id)
    if not fees_record or fees_record.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Fees record not found'}), 404

    try:
        transaction = FeeTransaction(
            fees_record_id=fees_id,
            amount_paid=amount,
            transaction_id=f"TXN{int(datetime.now(timezone.utc).timestamp())}",
            payment_method=data.get('payment_method', 'online')
        )
        db.session.add(transaction)

        if amount >= fees_record.amount:
            fees_record.status = 'paid'
            fees_record.paid_date = datetime.now(timezone.utc)

        db.session.commit()
        return jsonify({'success': True, 'message': 'Payment processed successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/fees/create', methods=['POST'])
@login_required
def create_fee_record():
    if current_user.role != 'non_teaching_staff':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    data = request.get_json() or request.form
    student_id = data.get('student_id')
    amount = float(data.get('amount', 0))
    due_days = int(data.get('due_days', 30))

    student = User.query.get(student_id)
    if not student:
        return jsonify({'success': False, 'message': 'Student not found'}), 404

    fee = FeesRecord(
        user_id=student.id,
        student_name=student.full_name,
        amount=amount,
        due_date=datetime.now(timezone.utc) + timedelta(days=due_days),
        status='pending'
    )
    db.session.add(fee)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Fee record created successfully'})


# 3. Grade & Attendance APIs for Teaching Staff
@app.route('/api/grades/submit', methods=['POST'])
@login_required
def submit_grade():
    if current_user.role not in ['teaching_staff', 'non_teaching_staff']:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    data = request.get_json() or request.form
    student_id = data.get('student_id')
    subject = data.get('subject', 'General')
    exam_title = data.get('exam_title', 'Assessment')
    score = float(data.get('score', 0))
    max_score = float(data.get('max_score', 100))

    # Calculate letter grade
    pct = (score / max_score) * 100 if max_score > 0 else 0
    if pct >= 90:
        grade_letter = 'A+'
    elif pct >= 80:
        grade_letter = 'A'
    elif pct >= 70:
        grade_letter = 'B'
    elif pct >= 60:
        grade_letter = 'C'
    elif pct >= 50:
        grade_letter = 'D'
    else:
        grade_letter = 'F'

    grade = Grade(
        student_id=student_id,
        subject=subject,
        exam_title=exam_title,
        score=score,
        max_score=max_score,
        grade_letter=grade_letter
    )
    db.session.add(grade)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Grade submitted successfully', 'grade_letter': grade_letter})


@app.route('/api/attendance/mark', methods=['POST'])
@login_required
def mark_attendance():
    if current_user.role not in ['teaching_staff', 'non_teaching_staff']:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    data = request.get_json() or request.form
    student_id = data.get('student_id')
    class_id = data.get('class_id', 1)
    status = data.get('status', 'present')
    remarks = data.get('remarks', '')

    attendance = Attendance(
        student_id=student_id,
        class_id=class_id,
        date=datetime.now(timezone.utc).date(),
        status=status,
        remarks=remarks
    )
    db.session.add(attendance)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Attendance marked successfully'})


# 4. Notice & Setting APIs
@app.route('/api/notices/create', methods=['POST'])
@login_required
def create_notice():
    if current_user.role not in ['teaching_staff', 'non_teaching_staff']:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    data = request.get_json() or request.form
    title = data.get('title')
    content = data.get('content')
    category = data.get('category', 'General')
    target_role = data.get('target_role', 'all')

    notice = Notice(
        title=title,
        content=content,
        category=category,
        author_id=current_user.id,
        target_role=target_role
    )
    db.session.add(notice)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Notice created successfully'})


@app.route('/api/settings/update', methods=['POST'])
@login_required
def update_settings():
    if current_user.role != 'non_teaching_staff':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    data = request.get_json() or request.form
    for key, val in data.items():
        setting = SystemSetting.query.filter_by(key=key).first()
        if setting:
            setting.value = str(val)
        else:
            setting = SystemSetting(key=key, value=str(val))
            db.session.add(setting)

    db.session.commit()
    return jsonify({'success': True, 'message': 'System settings updated successfully'})


# Initialize database
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
