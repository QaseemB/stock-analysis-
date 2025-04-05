from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def draw_pdf_report(symbol, plot_paths, df, pdf_filename):
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.drawString(100, 750, f"{symbol} Stock Analysis Report")

    y_position = 650
    margin_left = 50

    for plot_type, plot_path in plot_paths.items():
        if os.path.exists(plot_path):
            if y_position < 130:
                c.showPage()
                y_position = 650

            c.drawImage(plot_path, margin_left, y_position, width=500, height=140)
            y_position -= 180

    stats = df.describe().to_string()
    text_object = c.beginText(50, y_position)
    text_object.setFont("Helvetica", 10)
    text_object.textLines(stats)
    c.drawText(text_object)

    c.save()