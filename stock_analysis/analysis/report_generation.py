import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_pdf_report(symbol, plot_paths, df):
    # Create the subfolder for the symbol if it doesn't exist
    symbol_folder = os.path.join('stockreport', symbol)
    os.makedirs(symbol_folder, exist_ok=True)
    # Define the PDF file path in the symbol-specific folder
    pdf_filename = os.path.join(symbol_folder, f"{symbol}_stock_report.pdf")
    # Create a PDF canvas
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.drawString(100, 750, f"{symbol} Stock Analysis Report")

    y_position = 650
    margin_left = 50

    for plot_type, plot_path in plot_paths.items():
        if os.path.exists(plot_path):
            if y_position < 100:
                c.showPage()
                y_position = 650

            c.drawImage(plot_path, margin_left, y_position, width=500, height=300)
            y_position -= 320

    stats = df.describe().to_string()
    text_object = c.beginText(50, y_position)
    text_object.setFont("Helvetica", 10)
    text_object.textLines(stats)
    c.drawText(text_object)

    c.save()
    print(f"PDF report for {symbol} saved as {pdf_filename}")

    # Clean up image files
    # for plot_path in plot_paths.values():
    #     if os.path.exists(plot_path):
    #         os.remove(plot_path)