import os
import io
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from django.http import FileResponse

FONT_PATH = os.path.dirname(os.path.abspath(__file__))
times_font = os.path.join(FONT_PATH, 'times.ttf')
pdfmetrics.registerFont(TTFont('times', times_font))


def pdf_shopping_list_maker(shopping_list):
    """Creates pdf tamplate > printing strings > response pdf as attachment"""
    # pagesize=(595.27,841.89)
    start_x = 72
    start_y = 700
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.setFont('times', 24)
    pdf.drawString(150, 800, "Список покупок Foodgram")
    pdf.setFont('times', 16)
    for ingredient, count in shopping_list.items():
        pdf.drawString(start_x, start_y, ingredient.capitalize()+" "+count)
        start_y -= 30
    pdf.setFont('Helvetica', 14)
    pdf.setFillColorRGB(1, 0, 0)
    pdf.drawString(140, 20, "YASHCH with love to Yandex Praktikum Team <3")
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='foodgram.pdf')
