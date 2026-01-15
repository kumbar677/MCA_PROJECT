from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    # Use raw SQL to add the column, which is safer than relying on create_all (which effectively skips existing tables)
    # and easier than setting up a full migration environment from scratch if not already perfectly configured.
    print("Attempting to add profile_image column to student_details table...")
    try:
        with db.engine.connect() as conn:
            conn.execute(text("ALTER TABLE student_details ADD COLUMN profile_image VARCHAR(255)"))
            print("Column 'profile_image' added successfully.")
    except Exception as e:
        print(f"Error (might already exist): {e}")
        
    print("Done.")
