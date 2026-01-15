from app import create_app, User, db
import time

app = create_app()

with app.app_context():
    print("Checking DB connection...")
    try:
        # 1. Check raw connection
        start = time.time()
        with db.engine.connect() as conn:
            conn.execute(db.text("SELECT 1"))
        print(f"Raw connection check took: {time.time() - start:.4f}s")
        
        # 2. Check Admin User Query
        print("Querying for admin user...")
        start = time.time()
        user = User.query.filter_by(email='admin@university.com').first()
        print(f"Admin query took: {time.time() - start:.4f}s")
        
        if user:
            print(f"User found: {user.name}")
            # 3. Check password verify
            print("Verifying password...")
            start = time.time()
            is_valid = user.check_password('admin123')
            print(f"Password check took: {time.time() - start:.4f}s")
            print(f"Password valid: {is_valid}")
        else:
            print("Admin user NOT found!")
            
    except Exception as e:
        print(f"ERROR: {e}")
