from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # student, teaching_staff, non_teaching_staff
    enrollment_id = db.Column(db.String(100), unique=True)
    department = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class FeesRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    student_name = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    paid_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='pending')  # pending, paid, overdue
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('fees', lazy=True))


class FeeTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fees_record_id = db.Column(db.Integer, db.ForeignKey('fees_record.id'), nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    transaction_id = db.Column(db.String(100), unique=True)
    payment_method = db.Column(db.String(50))  # online, cash, cheque
    notes = db.Column(db.Text)

    fees_record = db.relationship('FeesRecord', backref=db.backref('transactions', lazy=True))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Routes
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

        user = User.query.filter_by(username=username, role=user_type).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/student/dashboard')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        return redirect(url_for('home'))
    fees = FeesRecord.query.filter_by(user_id=current_user.id).all()
    total_due = sum(f.amount for f in fees if f.status == 'pending')
    return render_template('student.html', user=current_user, fees=fees, total_due=total_due)


@app.route('/teaching-staff/dashboard')
@login_required
def teaching_staff_dashboard():
    if current_user.role != 'teaching_staff':
        return redirect(url_for('home'))
    return render_template('staff_teaching.html', user=current_user)


@app.route('/non-teaching-staff/dashboard')
@login_required
def non_teaching_staff_dashboard():
    if current_user.role != 'non_teaching_staff':
        return redirect(url_for('home'))
    return render_template('non_teaching_staff.html', user=current_user)


@app.route('/fees')
@login_required
def fees():
    if current_user.role != 'student':
        return redirect(url_for('home'))
    fees_record = FeesRecord.query.filter_by(user_id=current_user.id).first()
    return render_template('fees_payment.html', user=current_user, fees=fees_record)


@app.route('/api/pay-fees', methods=['POST'])
@login_required
def pay_fees():
    if current_user.role != 'student':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    data = request.get_json()
    amount = data.get('amount')
    fees_id = data.get('fees_id')

    fees_record = FeesRecord.query.get(fees_id)
    if not fees_record or fees_record.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Fees record not found'}), 404

    try:
        transaction = FeeTransaction(
            fees_record_id=fees_id,
            amount_paid=amount,
            transaction_id=f"TXN{datetime.utcnow().timestamp()}",
            payment_method='online'
        )
        db.session.add(transaction)

        if fees_record.amount <= amount:
            fees_record.status = 'paid'
            fees_record.paid_date = datetime.utcnow()

        db.session.commit()
        return jsonify({'success': True, 'message': 'Payment processed successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/admin/users')
@login_required
def admin_users():
    if current_user.role != 'non_teaching_staff':
        return redirect(url_for('home'))
    
    students = User.query.filter_by(role='student').all()
    teaching_staff = User.query.filter_by(role='teaching_staff').all()
    
    return render_template('admin_users.html', 
                         students=students, 
                         teaching_staff=teaching_staff,
                         user=current_user)


# Initialize database
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
