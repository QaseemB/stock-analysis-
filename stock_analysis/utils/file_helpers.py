from pathlib import Path
import os



def create_png_folder(symbol):
	BASE_URL = Path.home() /'Desktop'/'CODING'
	pdf_folder = BASE_URL /'APPLICATION_FILE_BASE_SYSTEMS'/'STOCKMARKET_FBS'/ 'png_storage'/symbol
	pdf_folder.mkdir(parents=True, exist_ok=True)
	return pdf_folder



def create_pdf_folder(symbol):
	BASE_URL = Path.home() /'Desktop'/'CODING'
	pdf_folder = BASE_URL /'APPLICATION_FILE_BASE_SYSTEMS'/'STOCKMARKET_FBS'/ 'pdf_storage'/symbol
	pdf_folder.mkdir(parents=True, exist_ok=True)
	return pdf_folder


def cleanup_temp_images(plot_paths):
    for path in plot_paths.values():
        if os.path.exists(path):
            os.remove(path)