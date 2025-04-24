from pathlib import Path
import os



from pathlib import Path

def get_base_symbol_folder(symbol):
    return Path.home() / 'Desktop' / 'CODING' / 'APPLICATION_FILE_BASE_SYSTEMS' / 'STOCKMARKET_FBS' / symbol

def get_pdf_path(symbol):
    folder = get_base_symbol_folder(symbol) / 'pdf'
    folder.mkdir(parents=True, exist_ok=True)
    return folder / f"{symbol}_report.pdf"

def get_csv_path(symbol):
    folder = get_base_symbol_folder(symbol) / 'csv'
    folder.mkdir(parents=True, exist_ok=True)
    return folder / f"{symbol}_data.csv"

def get_summary_json_path(symbol):
    folder = get_base_symbol_folder(symbol) / 'json'
    folder.mkdir(parents=True, exist_ok=True)
    return folder / f"{symbol}_summary.json"

def get_png_folder(symbol):
    folder = get_base_symbol_folder(symbol) / 'png'
    folder.mkdir(parents=True, exist_ok=True)
    return folder

def get_plotly_path(symbol, name):
    folder = get_base_symbol_folder(symbol) / 'plotly'
    folder.mkdir(parents=True, exist_ok=True)
    return folder / f"{symbol}_{name}.html"

def cleanup_temp_images(plot_paths):
    for path in plot_paths.values():
        if os.path.exists(path):
            os.remove(path)

def cleanup_symbol_folder(symbol):
    folder = get_base_symbol_folder(symbol)
    if folder.exists():
        shutil.rmtree(folder)