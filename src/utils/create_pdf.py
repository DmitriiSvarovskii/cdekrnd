from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import io


def create_pdf(text):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
    c.setFont("Arial", 12)

    lines = text.split('\n')
    y = 750
    for line in lines:
        c.drawString(100, y, line)
        y -= 15

    c.save()
    buffer.seek(0)
    return buffer.getvalue()
