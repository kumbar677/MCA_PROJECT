from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, User, Course, StudentDetails, Enrollment
from utils import generate_pdf_report, send_email_with_attachment
import os

student_bp = Blueprint('student', __name__)

# ... (student_required decorator stays here, skipped for brevity in tool call context if not targeting it, but targeting full block for safety in this case or just top and bottom)
# RE-READING user request: "send to email with description and one pdf of rukes and regulation" 
# Modifying top of file first for import
# ACTUALLY, I will use replace_file_content for specific chunks to be cleaner.

# First chunk: Update Import
# Second chunk: Update enroll function


student_bp = Blueprint('student', __name__)

def student_required(func):
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'student':
            flash('Access denied. Students only.', 'danger')
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return login_required(wrapper)

@student_bp.route('/dashboard')
@student_required
def dashboard():
    # Helper to get student details
    details = StudentDetails.query.filter_by(user_id=current_user.id).first()
    my_enrollments = Enrollment.query.filter_by(student_id=details.id).all() if details else []
    
    return render_template('student/dashboard.html', 
                           title='Student Dashboard',
                           details=details,
                           enrollments=my_enrollments)

@student_bp.route('/profile', methods=['GET', 'POST'])
@student_required
def profile():
    detail = StudentDetails.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        detail.phone = request.form.get('phone')
        detail.address = request.form.get('address')
        detail.dob = request.form.get('dob')
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('student.profile'))
        
    return render_template('student/profile.html', user=current_user, detail=detail)

@student_bp.route('/courses')
@student_required
def courses():
    search_query = request.args.get('search', '')
    query = Course.query
    
    if search_query:
        query = query.filter(
            (Course.name.ilike(f'%{search_query}%')) | 
            (Course.course_code.ilike(f'%{search_query}%'))
        )
        
    all_courses = query.all()
    
    # Get IDs of courses the student is already enrolled in
    student_details = StudentDetails.query.filter_by(user_id=current_user.id).first()
    enrolled_course_ids = []
    if student_details:
        enrolled = Enrollment.query.filter_by(student_id=student_details.id).all()
        enrolled_course_ids = [e.course_id for e in enrolled]
        
    return render_template('student/courses.html', courses=all_courses, enrolled_ids=enrolled_course_ids, search_query=search_query)

@student_bp.route('/enroll/<int:course_id>')
@student_required
def enroll(course_id):
    student_details = StudentDetails.query.filter_by(user_id=current_user.id).first()
    
    if not student_details:
         # Should not happen if registered correctly, but safeguard
         flash('Student details missing.', 'danger')
         return redirect(url_for('student.dashboard'))
         
    # Check if already enrolled
    existing = Enrollment.query.filter_by(student_id=student_details.id, course_id=course_id).first()
    if existing:
        flash('You are already enrolled in this course.', 'warning')
        return redirect(url_for('student.courses'))
        
    # Check seats
    course = Course.query.get_or_404(course_id)
    if course.seats <= 0:
        flash('This course is full.', 'danger')
        return redirect(url_for('student.courses'))
        
    # Enroll
    enrollment = Enrollment(student_id=student_details.id, course_id=course.id)
    course.seats -= 1
    db.session.add(enrollment)
    db.session.commit()
    
    # Send email with attachment
    subject = f"Enrollment Confirmed: {course.name}"
    body = f"""Hello {current_user.name},

You have successfully enrolled in the following course:

Course: {course.name} ({course.course_code})
Credits: {course.credits}
Description: {course.description}

Please find attached the University Rules and Regulations.

Happy Learning!
University Admin"""
    
    # Path to the PDF file
    pdf_path = os.path.join('static', 'files', 'rules.pdf')
    
    send_email_with_attachment(current_user.email, subject, body, attachment_path=pdf_path, attachment_name='University_Rules.pdf')
    
    flash(f'Successfully enrolled in {course.name}!', 'success')
    return redirect(url_for('student.dashboard'))
