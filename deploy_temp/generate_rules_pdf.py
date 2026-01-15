from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def create_rules_pdf():
    file_path = os.path.join('static', 'files', 'rules.pdf')
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "University Rules and Regulations")
    
    c.setFont("Helvetica", 12)
    y = height - 80
    
    rules = [
        "1. Attendance: 75% attendance is mandatory for all courses.",
        "2. Assignments: All assignments must be submitted by the due date.",
        "3. Exams: Malpractice in exams will lead to immediate suspension.",
        "4. Fees: Course fees must be paid before the start of the semester.",
        "5. Conduct: Students must maintain discipline and respect towards staff.",
        "6. Library: Books must be returned within the stipulated time.",
        "7. Labs: Safety protocols must be followed strictly in laboratories.",
        "8. ID Card: Students must carry their ID cards at all times on campus.",
        "9. Anti-Ragging: Ragging is strictly prohibited and is a criminal offense.",
        "10. IT Policy: University Wi-Fi is for academic purposes only."
    ]
    
    for rule in rules:
        c.drawString(50, y, rule)
        y -= 20
        
    c.save()
    print(f"PDF created at: {file_path}")

if __name__ == "__main__":
    create_rules_pdf()
