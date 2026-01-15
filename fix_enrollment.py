from app import create_app, db
from models import StudentDetails
from datetime import datetime

app = create_app()

with app.app_context():
    # Get all students without enrollment number
    students_without_enroll = StudentDetails.query.filter(StudentDetails.enrollment_no == None).all()
    
    current_year = datetime.now().year
    
    print(f"Found {len(students_without_enroll)} students without enrollment number.")
    
    count = 0
    for student in students_without_enroll:
        count += 1
        # Format: UNIV + Year + 3-digit-sequence (starting from user_id to ensure uniqueness)
        # Using user_id guarantees uniqueness even if we run this simply
        enroll_no = f"UNIV{current_year}{student.user_id:03d}"
        
        student.enrollment_no = enroll_no
        print(f"Assigned {enroll_no} to StudentDetails ID {student.id}")
        
    db.session.commit()
    print("Done! All students have enrollment numbers.")
