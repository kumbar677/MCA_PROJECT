from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem, PageBreak, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import os

def create_report():
    pdf_file = "Session_Report_Jan15.pdf"
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # --- Styles ---
    title_style = styles['Title']
    h1_style = styles['Heading1']
    h2_style = styles['Heading2']
    normal_style = styles['BodyText']
    
    code_style = ParagraphStyle(
        'Code',
        parent=styles['BodyText'],
        fontName='Courier',
        fontSize=8,
        leading=10,
        backColor=colors.whitesmoke,
        borderPadding=5
    )

    # ==========================
    # PAGE 1: EXECUTIVE SUMMARY
    # ==========================
    story.append(Paragraph("Full Session Activity Report", title_style))
    story.append(Paragraph("Development & Debugging Log", styles['Heading2']))
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>Date:</b> January 15, 2026", normal_style))
    story.append(Paragraph("<b>Summary:</b> This report documents the entire development session, including feature implementations, critical bug fixes, and system configuration updates.", normal_style))
    story.append(Spacer(1, 20))

    # ==========================
    # CHRONOLOGICAL TIMELINE
    # ==========================
    story.append(Paragraph("1. Chronological Activity Log", h1_style))
    
    events = [
        ["Phase", "Action / Details"],
        ["1. Admin Login Debugging", "<b>Issue:</b> Admin login was stuck on 'loading' state.\n<b>Debug:</b> Traced redirect flow, verified database user.\n<b>Fix:</b> Resolved `NameError` in `auth_routes.py` and fixed DB locking issue caused by stuck script."],
        ["2. Profile Image Feature", "<b>Req:</b> Allow students to upload profile pics.\n<b>Action:</b> Added `profile_image` col to DB. Updated `student_routes.py` for uploads. Added file input to `profile.html`.\n<b>Outcome:</b> Students can now upload and view profile images."],
        ["3. Admin Panel Updates", "<b>Req:</b> Show student images in Admin List.\n<b>Action:</b> Modified `admin/students.html` to show images or a default FontAwesome icon if missing."],
        ["4. Admin Credentials", "<b>Req:</b> Change Admin to ACV@gmail.com.\n<b>Action:</b> Ran `update_admin.py` to update DB. Updated `app.py` seed logic."],
        ["5. Enrollment Numbers", "<b>Req:</b> Fix NULL enrollment numbers.\n<b>Action:</b> Created `fix_enrollment.py` to backfill existing users (`UNIV2026xxx`). Updated `register` route to auto-generate for new users."]
    ]
    
    t_events = Table(events, colWidths=[120, 320])
    t_events.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_events)
    story.append(PageBreak())

    # ==========================
    # INSTALLED PACKAGES
    # ==========================
    story.append(Paragraph("2. Installed Packages & Environment", h1_style))
    story.append(Paragraph("The following Python packages were installed and used during development:", normal_style))
    story.append(Spacer(1, 10))
    
    pkgs = [
        ["Package", "Purpose"],
        ["Flask", "Web Framework"],
        ["Flask-SQLAlchemy", "Database ORM"],
        ["Flask-Login", "User Session Management"],
        ["Flask-Migrate", "Database Migrations"],
        ["Flask-Mail", "Email Notifications"],
        ["reportlab", "PDF Generation"],
        ["mysql-connector-python", "MySQL Driver"],
        ["pyngrok", "Public URL Tunneling"]
    ]
    t_pkgs = Table(pkgs, colWidths=[150, 250])
    t_pkgs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.darkgreen),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    story.append(t_pkgs)
    story.append(Spacer(1, 20))

    # ==========================
    # PAGE 3: COMMAND CHEAT SHEET
    # ==========================
    story.append(PageBreak())
    story.append(Paragraph("<b>3. Session Command Log</b>", h1_style))
    story.append(Paragraph("Commands executed during this session for reference:", normal_style))
    story.append(Spacer(1, 10))

    cmds = [
        ["Action", "Command / Script"],
        ["Start Server", "python app.py"],
        ["Update Admin Creds", "python update_admin.py"],
        ["Add New Admin", "python add_admin.py <email> <pass>"],
        ["Backfill Enroll Nos", "python fix_enrollment.py"],
        ["Check Database", "python inspect_db.py"]
    ]
    t = Table(cmds, colWidths=[150, 300])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t)
    
    doc.build(story)
    print(f"Report generated: {os.path.abspath(pdf_file)}")

if __name__ == "__main__":
    create_report()
