from app import create_app, db
from models import User, StudentDetails

app = create_app()

with app.app_context():
    print(f"{'ID':<5} {'Name':<20} {'Email':<30} {'EnrollNo':<12} {'Phone':<12} {'Image':<30}")
    print("-" * 110)
    
    results = db.session.query(User, StudentDetails).join(StudentDetails, User.id == StudentDetails.user_id).all()
    
    for user, detail in results:
        img = detail.profile_image if detail.profile_image else "NULL"
        eno = detail.enrollment_no if detail.enrollment_no else "NULL"
        phone = detail.phone if detail.phone else "NULL"
        print(f"{user.id:<5} {user.name[:19]:<20} {user.email[:29]:<30} {eno:<12} {phone:<12} {img:<30}")
