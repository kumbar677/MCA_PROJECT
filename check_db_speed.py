import time
from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("Checking database connection and speed...")
    start_time = time.time()
    try:
        # Check if column exists by selecting from it
        with db.engine.connect() as conn:
            result = conn.execute(text("SELECT id, link FROM courses LIMIT 1"))
            print("Query executed successfully.")
            for row in result:
                print(f"Course link found: {row[1]}")
    except Exception as e:
        print(f"Error executing query: {e}")
    
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.4f} seconds")
