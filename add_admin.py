from app import create_app, db, User
import sys

app = create_app()

with app.app_context():
    print("--- Create New Admin User ---")
    # Check if arguments provided
    if len(sys.argv) == 3:
        email = sys.argv[1]
        password = sys.argv[2]
    else:
        # Interactive mode
        email = input("Enter email for new admin: ")
        password = input("Enter password for new admin: ")

    if User.query.filter_by(email=email).first():
        print(f"Error: User with email {email} already exists!")
    else:
        new_admin = User(name='Admin User', email=email, role='admin')
        new_admin.set_password(password)
        db.session.add(new_admin)
        db.session.commit()
        print(f"Successfully created new admin: {email}")
