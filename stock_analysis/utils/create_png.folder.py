from pathlib import Path



def create_png_folder(symbol):
	BASE_URL = Path.home() /'Desktop'/'CODING'
	pdf_folder = BASE_URL /'APPLICATION_FILE_BASE_SYSTEMS'/'STOCKMARKET_FBS'/ 'png_storage'/symbol
	pdf_folder.mkdir(parents=True, exist_ok=True)
	return pdf_folder