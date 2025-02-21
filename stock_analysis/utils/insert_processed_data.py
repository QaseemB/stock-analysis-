from psycopg2 import sql
from datetime import datetime
from utils.sql_connect import connect_to_sql

def insert_processed_data(stock_symbol, processed_data):
    conn = connect_to_sql()
    cursor = conn.cursor()
    symbol = stock_symbol

    # Get stock_id from `stocks` table
    cursor.execute("SELECT stock_id FROM stocks WHERE symbol = %s;", (stock_symbol,))
    stock = cursor.fetchone()

    if stock is None:
        print(f"🚫 stock {stock_symbol} not found in sql. Inserting it now ")
        cursor.execute("INSERT INTO stocks (symbol) VALUES (%s) RETURNING stock_id;", (stock_symbol,))
        stock = cursor.fetchone()
        conn.commit()
        
    
    stock_id = stock[0] # stock_id is the first element in the tuple

    # Handle date parsing with a fallback
    date_str = processed_data["date"]
    try:
        parsed_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f+00:00")
    except ValueError:
        parsed_date = datetime.strptime(date_str, "%Y-%m-%d")

    query = """
    INSERT INTO stock_analysis (
    stock_id, symbol, date, moving_avg_3, moving_avg_6, moving_avg_12,
    upper_band, lower_band, monthly_return, rolling_mean, rolling_std,
    ema12, ema26, macd, signal_line
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
) ON CONFLICT (stock_id, date)
DO UPDATE SET
    symbol = EXCLUDED.symbol,
    moving_avg_3 = EXCLUDED.moving_avg_3,
    moving_avg_6 = EXCLUDED.moving_avg_6,
    moving_avg_12 = EXCLUDED.moving_avg_12,
    upper_band = EXCLUDED.upper_band,
    lower_band = EXCLUDED.lower_band,
    monthly_return = EXCLUDED.monthly_return,
    rolling_mean = EXCLUDED.rolling_mean,
    rolling_std = EXCLUDED.rolling_std,
    ema12 = EXCLUDED.ema12,
    ema26 = EXCLUDED.ema26,
    macd = EXCLUDED.macd,
    signal_line = EXCLUDED.signal_line;
    """ 

    values = (
        stock_id,
        stock_symbol,
        parsed_date.date(),
        # processed_data["open"],
        # processed_data["close"],
        # processed_data["high"],
        # processed_data["low"],
        # processed_data["volume"],
        processed_data["moving_avg_3"],
        processed_data["moving_avg_6"],
        processed_data["moving_avg_12"],
        processed_data["upper_band"],
        processed_data["lower_band"],
        processed_data["monthly_return"],
        processed_data["rolling_mean"],
        processed_data["rolling_std"],
        processed_data["ema12"],
        processed_data["ema26"],
        processed_data["macd"],
        processed_data["signal_line"]
    )

    print("Executing SQL with values:", values)

    cursor.execute(query, values)
    conn.commit()


    print(f"✅ Processed data for {stock_symbol} on {processed_data['date']} inserted successfully!")

    cursor.close()
    conn.close()
