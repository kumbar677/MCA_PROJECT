from app import create_app, db, User

app = create_app()

with app.app_context():
    # Find existing admin
    admin = User.query.filter_by(role='admin').first()
    
    if admin:
        print(f"Found admin: {admin.email}")
        admin.email = 'ACV@gmail.com'
        admin.set_password('ACV123')
        db.session.commit()
        print("Admin credentials updated successfully.")
        print(f"New Email: {admin.email}")
    else:
        # Create if doesn't exist (though it should)
        print("Admin user not found. Creating new one...")
        admin = User(name='Admin User', email='ACV@gmail.com', role='admin')
        admin.set_password('ACV123')
        db.session.add(admin)
        db.session.commit()
        print("New Admin user created.")
