from app import create_app, db
from sqlalchemy import text
import time

app = create_app()

with app.app_context():
    try:
        start = time.time()
        with db.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print(f"Database connection successful. Response time: {time.time() - start:.4f}s")
    except Exception as e:
        print(f"Database error: {e}")
