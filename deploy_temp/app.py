from flask import Flask, render_template, redirect, url_for
from config import Config
from models import db, User
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    mail = Mail(app)
    app.extensions['mail'] = mail # Explicitly adding to extensions just in case (optional, Mail(app) usually does this)
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import and register blueprints
    # Note: These files will be created in the next steps
    try:
        from routes.auth_routes import auth_bp
        from routes.admin_routes import admin_bp
        from routes.student_routes import student_bp
        
        app.register_blueprint(auth_bp)
        app.register_blueprint(admin_bp, url_prefix='/admin')
        app.register_blueprint(student_bp, url_prefix='/student')
    except ImportError:
        print("Blueprints not fully implemented yet.")

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # Create tables for testing/dev (migrations are better for prod)
        try:
            db.create_all()
            
            # Seed Admin User if not exists
            if not User.query.filter_by(email='admin@university.com').first():
                admin = User(name='Admin User', email='admin@university.com', role='admin')
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("Admin user created.")
        except Exception as e:
            print(f"Database error (ensure MySQL is running): {e}")

    app.run(debug=True, host='0.0.0.0')
