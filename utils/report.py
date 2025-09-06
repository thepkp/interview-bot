from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_report(questions, answers, feedback):
    pdf_path = "interview_report.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    y = height - 50

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Interview Report")
    y -= 30

    c.setFont("Helvetica", 10)
    for i, (q, ans, fb) in enumerate(zip(questions, answers, feedback)):
        c.drawString(50, y, f"Q{i+1}: {q}")
        y -= 15
        c.drawString(70, y, f"Answer: {ans}")
        y -= 15
        c.drawString(70, y, f"Feedback: {fb['feedback']}")
        y -= 15
        c.drawString(70, y, f"Score: {fb['score']}/10")
        y -= 25
        if y < 100:  # New page
            c.showPage()
            y = height - 50

    c.save()
    return pdf_path
