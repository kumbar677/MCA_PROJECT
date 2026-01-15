from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from flask_login import login_required, current_user
from models import db, User, Course, StudentDetails, Enrollment
from utils import generate_pdf_report

admin_bp = Blueprint('admin', __name__)

def admin_required(func):
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Access denied. Admins only.', 'danger')
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return login_required(wrapper)

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    total_students = User.query.filter_by(role='student').count()
    total_courses = Course.query.count()
    total_enrollments = Enrollment.query.count()
    
    return render_template('admin/dashboard.html', 
                           title='Admin Dashboard',
                           total_students=total_students,
                           total_courses=total_courses,
                           total_enrollments=total_enrollments)

@admin_bp.route('/students', methods=['GET', 'POST'])
@admin_required
def manage_students():
    search_query = request.args.get('search', '')
    query = db.session.query(User, StudentDetails).join(StudentDetails, User.id == StudentDetails.user_id).filter(User.role == 'student')
    
    if search_query:
        query = query.filter(
            (User.name.ilike(f'%{search_query}%')) | 
            (User.email.ilike(f'%{search_query}%'))
        )
        
    students = query.all()
    return render_template('admin/students.html', students=students, search_query=search_query)

@admin_bp.route('/students/delete/<int:user_id>')
@admin_required
def delete_student(user_id):
    user = User.query.get_or_404(user_id)
    if user.role != 'student':
        flash('Cannot delete non-student users from here.', 'warning')
        return redirect(url_for('admin.manage_students'))
        
    db.session.delete(user)
    db.session.commit()
    flash('Student deleted successfully.', 'success')
    return redirect(url_for('admin.manage_students'))

@admin_bp.route('/courses', methods=['GET', 'POST'])
@admin_required
def manage_courses():
    if request.method == 'POST':
        course_code = request.form.get('course_code')
        name = request.form.get('name')
        credits = request.form.get('credits')
        seats = request.form.get('seats')
        
        existing = Course.query.filter_by(course_code=course_code).first()
        if existing:
            flash('Course Code already exists.', 'warning')
        else:
            new_course = Course(course_code=course_code, name=name, credits=credits, seats=seats)
            db.session.add(new_course)
            db.session.commit()
            flash('Course added successfully.', 'success')
            
    courses = Course.query.all()
    return render_template('admin/courses.html', courses=courses)

@admin_bp.route('/courses/delete/<int:course_id>')
@admin_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash('Course deleted successfully.', 'success')
    return redirect(url_for('admin.manage_courses'))

@admin_bp.route('/report')
@admin_required
def generate_report():
    enrollments = db.session.query(Enrollment, User, Course).select_from(Enrollment).join(StudentDetails).join(User).join(Course).all()
    data = ["Enrollment Report"]
    for enr, user, course in enrollments:
        data.append(f"{user.name} ({user.email}) - {course.name} [{course.course_code}] - Status: {enr.status}")
        
    pdf = generate_pdf_report(data, title="University Enrollment Report")
    return send_file(pdf, as_attachment=True, download_name='report.pdf', mimetype='application/pdf')

@admin_bp.route('/settings', methods=['GET', 'POST'])
@admin_required
def settings():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not current_user.check_password(current_password):
            flash('Incorrect current password.', 'danger')
            return redirect(url_for('admin.settings'))

        if new_password != confirm_password:
            flash('New passwords do not match.', 'danger')
            return redirect(url_for('admin.settings'))

        current_user.set_password(new_password)
        db.session.commit()
        flash('Password updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/settings.html')

@admin_bp.route('/enrollments')
@admin_required
def enrollments():
    # Helper to avoid ambiguous join: start from Enrollment, join StudentDetails, then User, then Course
    all_enrollments = db.session.query(Enrollment, User, Course).select_from(Enrollment).join(StudentDetails).join(User).join(Course).all()
    return render_template('admin/enrollments.html', enrollments=all_enrollments)
