from stock_analysis.services.data_retrieval import get_stock_data
from stock_analysis.transfomer.stock_analysis_transformer import analyze_stock_data
from stock_analysis.transfomer.stock_summary_transformer import generate_summary
from stock_analysis.utils.file_helpers import get_summary_json_path

def data_transformation(symbols: list):
    transformation_results = []
    for symbol in symbols:
        print(f"🔍 Processing: {symbol}")
        cleaned_monthly_data = get_stock_data(symbol)
        if cleaned_monthly_data is None:
            print(f"Error: No data returned for symbol {symbol}")
            continue

        df = analyze_stock_data(cleaned_monthly_data,symbol)
    # print(df)
        if df is None:
            print(f"error: analysis failed something is wrong with the analyze_stock function")
            continue

        summary = generate_summary(df,symbol)
        transformation_results.append((symbol,df,summary))
    

    return {transformation_results}


# summary = data_transformation(['TSM','BAC'])

# print(summary)
