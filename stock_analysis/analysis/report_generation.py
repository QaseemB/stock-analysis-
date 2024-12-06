from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_pdf_report(symbol, plot_path):
    pdf_path = f"stockreport/{symbol}_report.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.drawString(100, 750, f"{symbol} Stock Analysis Report")
    c.drawImage(plot_path, 50, 400, width=500, height=300)
    c.save()
    print(f"Report saved: {pdf_path}")
