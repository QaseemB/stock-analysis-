from services.data_retrieval import get_stock_data
from transfomer.stock_analysis_transformer import analyze_stock_data
from transfomer.stock_summary_transformer import generate_summary
from utils.file_helpers import get_summary_json_path

def data_transformation(symbol):
    cleaned_monthly_data = get_stock_data(symbol)
    if cleaned_monthly_data is None:
        print(f"Error: No data returned for symbol {symbol}")
        return None
    df = analyze_stock_data(cleaned_monthly_data,symbol)
    if df is None:
        print(f"error: analysis failed something is wrong with the analyze_stock function")
        return None
    summary = generate_summary(df,symbol)

    

    return summary


summary = data_transformation("AAPL")

print(summary)
