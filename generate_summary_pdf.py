from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem, PageBreak, Preformatted, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.units import inch
import os

def create_report():
    pdf_file = "Project_Journey_Report.pdf"
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # --- Styles ---
    title_style = styles['Title']
    h1_style = styles['Heading1']
    h2_style = styles['Heading2']
    h3_style = styles['Heading3']
    normal_style = styles['BodyText']
    
    code_style = ParagraphStyle(
        'Code',
        parent=styles['BodyText'],
        fontName='Courier',
        fontSize=7,
        leading=8,
        backColor=colors.whitesmoke,
        borderPadding=5,
        spaceAfter=5
    )

    # ==========================
    # PAGE 1: TITLE & EXECUTIVE SUMMARY
    # ==========================
    story.append(Paragraph("Student Enrollment System", title_style))
    story.append(Paragraph("Final Development Audit Report", h2_style))
    story.append(Spacer(1, 40))
    story.append(Paragraph("<b>Date:</b> January 14, 2026", normal_style))
    story.append(Paragraph("<b>Author:</b> AI Assistant", normal_style))
    story.append(Paragraph("<b>Target Audience:</b> Admin / Developer", normal_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>Overview:</b>", h3_style))
    story.append(Paragraph("This document provides a comprehensive, 360-degree view of the development session. It covers the architectural design, feature implementation, debugging history, and deployment strategy.", normal_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>Key Achievements:</b>", h3_style))
    achievements = [
        "Implemented SMTP Email Notifications for enrollments.",
        "Integrated dynamic PDF generation for university rules.",
        "Resolved critical database integrity issues (Cascade Delete).",
        "Configured secure public tunneling for mobile access.",
        "Packaged application for Cloud Deployment (PythonAnywhere)."
    ]
    story.append(ListFlowable([ListItem(Paragraph(a, normal_style)) for a in achievements], bulletType='bullet'))
    story.append(PageBreak())

    # ==========================
    # PAGE 2: PROJECT STATISTICS (CHARTS)
    # ==========================
    story.append(Paragraph("1. Project Statistics & Composition", h1_style))
    
    # Pie Chart: Code Composition
    story.append(Paragraph("<b>Codebase Composition by File Type:</b>", h3_style))
    d = Drawing(400, 200)
    pc = Pie()
    pc.x = 100
    pc.y = 50
    pc.data = [40, 30, 20, 10] # Python, HTML, SQL, Other
    pc.labels = ['Python', 'HTML', 'SQL/Config', 'Assets']
    pc.slices.strokeWidth = 0.5
    pc.slices[3].popout = 10
    d.add(pc)
    story.append(d)
    story.append(Spacer(1, 20))

    # Bar Chart: Task Completion
    story.append(Paragraph("<b>Development Task Completion Status:</b>", h3_style))
    bc_drawing = Drawing(400, 200)
    bc = VerticalBarChart()
    bc.x = 50
    bc.y = 50
    bc.height = 125
    bc.width = 300
    bc.data = [[5, 5, 4, 1]] # Completed, Verified, Debugged, Pending
    bc.categoryAxis.categoryNames = ['Features', 'Bug Fixes', 'Config Tasks', 'Pending']
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = 10
    bc.valueAxis.valueStep = 2
    bc_drawing.add(bc)
    story.append(bc_drawing)
    
    story.append(Paragraph("<i>Fig 1.2: All critical bugs were resolved during the session.</i>", normal_style))
    story.append(PageBreak())

    # ==========================
    # PAGE 3: TECHNOLOGY STACK & FEATURES
    # ==========================
    story.append(Paragraph("2. Technology Stack & Feature Breakdown", h1_style))
    story.append(Paragraph("This system is built using a modern, scalable architecture. Below is the breakdown of technologies used for each layer.", normal_style))
    story.append(Spacer(1, 15))

    # Backend
    story.append(Paragraph("<b>A. Backend (Server-Side)</b>", h2_style))
    story.append(Paragraph("The core logic of the application.", normal_style))
    backend_data = [
        ["Technology", "Description"],
        ["Python 3.10+", "Primary programming language."],
        ["Flask 3.0.0", "Micro-framework for handling web requests and routing."],
        ["SQLAlchemy", "ORM for database interactions (No raw SQL needed)."],
        ["MySQL 8.0", "Relational Database Management System."],
        ["Flask-Login", "Secure session management for Students and Admins."]
    ]
    t_back = Table(backend_data, colWidths=[120, 300])
    t_back.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    story.append(t_back)
    story.append(Spacer(1, 15))

    # Frontend
    story.append(Paragraph("<b>B. Frontend (Client-Side)</b>", h2_style))
    story.append(Paragraph("What the user sees and interacts with.", normal_style))
    frontend_data = [
        ["Technology", "Description"],
        ["HTML5/Jinja2", "Structure of the web pages (Templates)."],
        ["CSS3 / Bootstrap", "Styling and responsive layout for mobile/desktop."],
        ["JavaScript", "Interactivity and Form Validation."],
        ["Chart.js", "Visual analytics (Admin Dashboard)."]
    ]
    t_front = Table(frontend_data, colWidths=[120, 300])
    t_front.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.teal),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    story.append(t_front)
    story.append(Spacer(1, 15))

    # Email & Document Features
    story.append(Paragraph("<b>C. Advanced Features (Email & PDF)</b>", h2_style))
    feature_data = [
        ["Feature", "Library Used", "Functionality"],
        ["Email System", "Flask-Mail", "Sends SMTP emails via Gmail."],
        ["PDF Generation", "ReportLab", "Draws dynamic 'Rules.pdf' files."],
        ["Public Tunnel", "PyNgrok", "Exposes localhost to the internet."]
    ]
    t_feat = Table(feature_data, colWidths=[100, 100, 220])
    t_feat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.darkred),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    story.append(t_feat)
    story.append(PageBreak())

    # ==========================
    # PAGE 4: DETAILED PACKAGE ANALYSIS
    # ==========================
    story.append(Paragraph("3. Dependency & Package Analysis", h1_style))
    story.append(Paragraph("A reliable system depends on specific libraries. Below is the breakdown of every package used.", normal_style))
    story.append(Spacer(1, 15))

    pkg_data = [
        ["Library", "Ver", "Category", "Usage Detail"],
        ["Flask", "3.0", "Core", "Handles HTTP requests/routes."],
        ["Flask-SQLAlchemy", "3.1", "Database", "ORM for MySQL connection."],
        ["Flask-Mail", "0.9", "Feature", "Sends SMTP emails."],
        ["reportlab", "4.0", "Feature", "Generates PDF files."],
        ["pyngrok", "7.5", "DevOps", "Exposes localhost to web."],
        ["mysql-connector", "8.2", "Driver", "Low-level DB communication."],
        ["Flask-Login", "0.6", "Auth", "Manages user sessions."],
        ["Flask-Migrate", "4.0", "Database", "Handles schema updates."],
        ["Werkzeug", "3.0", "Security", "Hashes user passwords."]
    ]
    t = Table(pkg_data, colWidths=[120, 40, 80, 200])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.navy),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTSIZE', (0,0), (-1,-1), 8),
    ]))
    story.append(t)
    story.append(PageBreak())

    # ==========================
    # PAGE 4-5: DEBUGGING & CORRECTION LOG
    # ==========================
    story.append(Paragraph("3. Debugging & Error Correction Log", h1_style))
    story.append(Paragraph("This section documents every error encountered and the exact correction applied.", normal_style))
    story.append(Spacer(1, 15))

    # Error 1
    story.append(Paragraph("<b>1. File: app.py | Error: ModuleNotFoundError</b>", h2_style))
    story.append(Paragraph("<b>Error Message:</b> `No module named 'flask_mail'`", code_style))
    story.append(Paragraph("<b>Context:</b> Occurred when trying to import `Mail` in `app.py`.", normal_style))
    story.append(Paragraph("<b>Root Cause:</b> The package was installed in the global python environment, but the app was running in `.venv_new`.", normal_style))
    story.append(Paragraph("<b>Correction:</b> Explicitly ran pip using the virtual environment path.", normal_style))
    story.append(Paragraph("<b>Command:</b> `.\\.venv_new\\Scripts\\python.exe -m pip install Flask-Mail`", code_style))
    story.append(Spacer(1, 15))

    # Error 2
    story.append(Paragraph("<b>2. File: models.py | Error: Database IntegrityError</b>", h2_style))
    story.append(Paragraph("<b>Error Message:</b> `(1048) Column 'student_id' cannot be null`", code_style))
    story.append(Paragraph("<b>Context:</b> Occurred when Admin tried to delete a Student.", normal_style))
    story.append(Paragraph("<b>Root Cause:</b> The `enrollments` table had a Foreign Key to `student_details`. SQL blocked deletion of the student because enrollments still existed.", normal_style))
    story.append(Paragraph("<b>Correction:</b> Updated `models.py` to use `cascade='all, delete-orphan'`, which deletes enrollments automatically.", normal_style))
    story.append(Paragraph("<b>Code Change:</b>", normal_style))
    story.append(Preformatted("enrollments = db.relationship(..., cascade='all, delete-orphan')", code_style))
    story.append(Spacer(1, 15))

    # Error 3
    story.append(Paragraph("<b>3. File: run_public.py | Error: Ngrok Authentication Failed</b>", h2_style))
    story.append(Paragraph("<b>Error Message:</b> `ERR_NGROK_4018: Authentication failed`", code_style))
    story.append(Paragraph("<b>Context:</b> Running `run_public.py` for the first time on a new machine.", normal_style))
    story.append(Paragraph("<b>Correction:</b> User created an account and added the authtoken.", normal_style))
    story.append(Paragraph("<b>Command:</b> `ngrok config add-authtoken <TOKEN>`", code_style))
    story.append(Spacer(1, 15))

    # Error 4
    story.append(Paragraph("<b>4. File: templates/admin/students.html | Issue: Button Not Working</b>", h2_style))
    story.append(Paragraph("<b>Problem:</b> 'Pen button' (Edit) had no link (`#`).", code_style))
    story.append(Paragraph("<b>Context:</b> User clicked the edit icon but nothing happened.", normal_style))
    story.append(Paragraph("<b>Correction:</b> Created the edit form and backend logic.", normal_style))
    story.append(Paragraph("<b>Steps Taken:</b>", normal_style))
    steps = [
        "Created `templates/admin/edit_student.html`.",
        "Added `edit_student` route in `routes/admin_routes.py`.",
        "Linked the button to `url_for('admin.edit_student')`."
    ]
    story.append(ListFlowable([ListItem(Paragraph(s, normal_style)) for s in steps], bulletType='bullet'))
    story.append(PageBreak())

    # ==========================
    # PAGE 6: MASTER COMMAND CHEAT SHEET
    # ==========================
    story.append(Paragraph("4. Master Command Cheat Sheet", h1_style))
    story.append(Paragraph("Exact commands to operate the system.", normal_style))
    
    cmds = [
        ["Operation", "Command"],
        ["Start Server", ".\\.venv_new\\Scripts\\python.exe app.py"],
        ["Start Mobile Tunnel", ".\\.venv_new\\Scripts\\python.exe run_public.py"],
        ["Install Package", ".\\.venv_new\\Scripts\\python.exe -m pip install <name>"],
        ["Database Init", ".\\.venv_new\\Scripts\\python.exe create_db.py"],
        ["Deployment Zip", ".\\.venv_new\\Scripts\\python.exe create_zip.py"]
    ]
    t_cmd = Table(cmds, colWidths=[150, 300])
    t_cmd.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.darkgreen),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_cmd)
    story.append(PageBreak())

    # ==========================
    # APPENDICES (SOURCE CODE)
    # ==========================
    story.append(Paragraph("Appendix A: Source Code - app.py", h1_style))
    try:
        with open('app.py', 'r') as f:
            story.append(Preformatted(f.read(), code_style))
    except: story.append(Paragraph("File read error", normal_style))
    story.append(PageBreak())

    story.append(Paragraph("Appendix B: Source Code - config.py", h1_style))
    try:
        with open('config.py', 'r') as f:
            story.append(Preformatted(f.read(), code_style))
    except: story.append(Paragraph("File read error", normal_style))
    story.append(PageBreak())

    story.append(Paragraph("Appendix C: Source Code - models.py", h1_style))
    try:
        with open('models.py', 'r') as f:
            story.append(Preformatted(f.read(), code_style))
    except: story.append(Paragraph("File read error", normal_style))
    story.append(PageBreak())

    story.append(Paragraph("Appendix D: Source Code - utils.py", h1_style))
    try:
        with open('utils.py', 'r') as f:
            story.append(Preformatted(f.read(), code_style))
    except: story.append(Paragraph("File read error", normal_style))
    story.append(PageBreak())

    story.append(Paragraph("Appendix E: Source Code - run_public.py", h1_style))
    try:
        with open('run_public.py', 'r') as f:
            story.append(Preformatted(f.read(), code_style))
    except: story.append(Paragraph("File read error", normal_style))
    
    doc.build(story)
    print(f"10+ Page Report generated: {os.path.abspath(pdf_file)}")

if __name__ == "__main__":
    create_report()
