from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf_report(data, title="Report"):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 50, title)
    
    p.setFont("Helvetica", 12)
    y = height - 80
    
    for line in data:
        p.drawString(100, y, line)
        y -= 20
        if y < 50:
            p.showPage()
            y = height - 50
            
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return buffer

from flask_mail import Message
from flask import current_app

def send_email_with_attachment(to_email, subject, body, attachment_path=None, attachment_name='document.pdf'):
    """
    Sends an email using Flask-Mail.
    """
    try:
        msg = Message(subject, recipients=[to_email])
        msg.body = body
        msg.sender = current_app.config.get('MAIL_USERNAME')
        
        if attachment_path:
            with current_app.open_resource(attachment_path) as fp:
                msg.attach(attachment_name, "application/pdf", fp.read())
        
        mail = current_app.extensions.get('mail')
        if mail:
            mail.send(msg)
            print(f"Email sent to {to_email}")
            return True
        else:
            print("Mail extension not found.")
            return False
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
