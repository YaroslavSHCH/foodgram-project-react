import io
import os

from django.http import FileResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

FONT_PATH = os.path.dirname(os.path.abspath(__file__))
times_font = os.path.join(FONT_PATH, 'times.ttf')
pdfmetrics.registerFont(TTFont('times', times_font))


def pdf_shopping_list_maker(shopping_list):
    """Creates pdf tamplate > printing strings > response pdf as attachment"""
    start_x = 72
    start_y = 700
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.setFont('times', 24)
    pdf.drawString(150, 800, "Список покупок Foodgram")
    pdf.setFont('times', 16)
    for ingredient, count in shopping_list.items():
        pdf.drawString(start_x, start_y, ingredient.capitalize() + " " + count)
        start_y -= 30
        if start_y <= 40:
            pdf.showPage()
            start_y = 700
            pdf.setFont('times', 16)
    pdf.setFont('Helvetica', 14)
    pdf.setFillColorRGB(1, 0, 0)
    pdf.drawString(140, 20, "YASHCH with love to Yandex Praktikum Team <3")
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='foodgram.pdf')
