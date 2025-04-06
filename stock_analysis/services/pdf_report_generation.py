from renderers.pdf_renderer import draw_pdf_report
from utils.file_helpers import get_pdf_path, cleanup_temp_images

def create_pdf_report(symbol, plot_paths, df, generate_pdf=False, cleanup=False):
    if generate_pdf:
        # Create the subfolder for the symbol if it doesn't exist
        pdf_path = get_pdf_path(symbol)
        # Create a PDF canvas
        draw_pdf_report(symbol, plot_paths, df, str(pdf_path))
        print(f"PDF report for {symbol} saved as {pdf_path}")

    
    if cleanup:
        cleanup_temp_images(plot_paths)
        print(f"png files for {symbol} has been cleaned and discared")
    