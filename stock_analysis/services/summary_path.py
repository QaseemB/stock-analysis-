from stock_analysis.services.data_retrieval import get_stock_data
from stock_analysis.transfomer.stock_analysis_transformer import analyze_stock_data
from stock_analysis.transfomer.stock_summary_transformer import generate_summary
from stock_analysis.utils.file_helpers import get_summary_json_path
from stock_analysis.utils.s3_helper import save_summary_to_s3, delete_local_file
from stock_analysis.utils.stock_list import stock_list
import json


def gen_summary_path(symbols: list, upload=True,):
    result_map = {}
    for symbol in symbols: 
        print(f"Processing summary for: {symbol}")

        cleaned_data = get_stock_data(symbol)
        if cleaned_data is None:
            print(f" Failed to retrieve data for {symbol}")
            continue

        df = analyze_stock_data(cleaned_data, symbol)
        if df is None:
            print(f" Failed to analyze data for {symbol}")
            continue

        summary = generate_summary(df, symbol)
        summary_path = get_summary_json_path(symbol)

        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=4, default=str)

        print(f"summary report for {symbol} saved as {summary_path}")

        if upload:
            s3_uri = save_summary_to_s3(summary_path,symbol)
            if s3_uri:
                delete_local_file(summary_path)
                print(f"local path to summary json for {symbol} have been deleted and has beeen saved to aws s3: {s3_uri}")
                result_map[symbol] = s3_uri
            else:
                result_map[symbol] = summary_path  
    return result_map


gen_summary_path(stock_list)
    
    
  
    

