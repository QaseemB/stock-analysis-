from stock_analysis.services.insert_processed_data import insert_processed_data

def populate_database_from_analysis(analysis_results):
    for stock_symbol, stock_data in analysis_results.items():
        for entry in stock_data:
            insert_processed_data(stock_symbol, entry)