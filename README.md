# Advanced Student Enrollment System

A full-stack web application for managing student enrollments, courses, and administrative tasks.

## Tech Stack
- **Backend**: Python (Flask)
- **Database**: MySQL (SQLAlchemy ORM)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Reporting**: ReportLab (PDF), Chart.js (Visuals)

## Setup Instructions

1.  **Prerequisites**:
    - Python 3.x
    - MySQL Server

2.  **Installation**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configuration**:
    - Edit `config.py` if your MySQL password is not empty.
    - Default connection: `mysql+mysqlconnector://root:@localhost/enrollment_db`

4.  **Run**:
    ```bash
    python app.py
    ```
    - Access at `http://localhost:5000`

## Default Admin Credentials
- **Email**: `admin@university.com`
- **Password**: `admin123`
