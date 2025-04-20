from stock_analysis.services.data_transformation import data_transformation
from stock_analysis.transfomer.sql_transform_data import transform_to_processed_data_sql
from stock_analysis.services.insert_processed_data import insert_processed_data
from stock_analysis.utils.format_for_sql_insert import format_for_sql_insert



def store_transformed_data(symbols: list):
    results = data_transformation(symbols)

    for result in results:
        symbol, df, summary = result
        print(f"🔍 Processing stock symbol: {symbol}")
        


        if df is None or df.empty:
            print(f"⚠️ Empty DataFrame for {symbol}")
            continue

        processed = transform_to_processed_data_sql(df, symbol)

        if not processed:
            print(f"🚫 No processed data for {symbol}")
            continue

        insert_processed_data(processed, symbol)


# store_transformed_data(['CRWD', 'DDOG', 'DOCU', 'FSLY'])

