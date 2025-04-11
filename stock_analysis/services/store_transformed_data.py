from stock_analysis.services.data_transformation import data_transformation
from stock_analysis.transfomer.sql_transform_data import transform_to_processed_data_sql
from stock_analysis.services.insert_processed_data import insert_processed_data


def store_transformed_data(symbol):
    df, summary = data_transformation(symbol)
    if df is None:
        print(f"Error: tranformation failed for {symbol}")
        return
    processed_data_transformed_sql = transform_to_processed_data_sql(df, symbol)
    
    # print(processed_data_transformed_sql)
    
    sqltest = insert_processed_data(processed_data_transformed_sql,symbol)
    print(f"{symbol} data stored in SQL successfully")
    return


testing = store_transformed_data('TSLA')

print(f"testing sql storing  processed: {testing}")