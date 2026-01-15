from app import create_app, db
from models import User
import time

app = create_app()

print("Starting login query test...")
with app.app_context():
    try:
        start = time.time()
        print("Querying for admin user...")
        # Force a fresh connection/query
        user = User.query.filter_by(email='admin@university.com').first()
        print(f"Query finished in {time.time() - start:.4f}s")
        if user:
            print(f"User found: {user.name}, Role: {user.role}")
        else:
            print("User not found")
    except Exception as e:
        print(f"Error: {e}")
