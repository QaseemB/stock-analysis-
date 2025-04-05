from renderers.pdf_renderer import draw_pdf_report
from utils.file_helpers import create_pdf_folder, cleanup_temp_images

def create_pdf_report(symbol, plot_paths, df, generate_pdf=False, cleanup=False):
    if generate_pdf:

        # Create the subfolder for the symbol if it doesn't exist
        pdf_folder = create_pdf_folder(symbol)
         # Define the PDF file path in the symbol-specific folder
        pdf_filename = pdf_folder / f"{symbol}_stock_report.pdf"
        # Create a PDF canvas
        draw_pdf_report(symbol, plot_paths, df, str(pdf_filename))
        print(f"PDF report for {symbol} saved as {pdf_filename}")

    
    if cleanup:
        cleanup_temp_images(plot_paths)
        print(f"png files for {symbol} has been cleaned and discared")
    