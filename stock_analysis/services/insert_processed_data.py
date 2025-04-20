from psycopg2.extras import execute_values
from datetime import datetime
from stock_analysis.utils.sql_connect import connect_to_sql

def insert_processed_data(processed_data: list,stock_symbol: str):
    conn = connect_to_sql()
    cursor = conn.cursor()

    # Get or insert stock_id
    cursor.execute("SELECT stock_id FROM stocks WHERE symbol = %s;", (stock_symbol,))
    stock = cursor.fetchone()

    if stock is None:
        print(f"🚫 Stock '{stock_symbol}' not found. Inserting it now.")
        cursor.execute(
            "INSERT INTO stocks (symbol) VALUES (%s) RETURNING stock_id;",
            (stock_symbol,)
        )
        stock = cursor.fetchone()
        conn.commit()

    if stock is None:
        print(f"❌ Could not insert or fetch stock '{stock_symbol}'.")
        cursor.close()
        conn.close()
        return

    stock_id = stock[0]


    insert_query = """
        INSERT INTO stock_analysis (
            stock_id, symbol, date, open_price, high_price, low_price, close_price, volume,
            moving_avg_3, moving_avg_6, moving_avg_12, upper_band, lower_band,
            monthly_return, rolling_mean, rolling_std, ema12, ema26,
            MACD, signal_line, RSI, OBV
        ) VALUES %s
        ON CONFLICT (stock_id, date)
        DO UPDATE SET
            symbol = EXCLUDED.symbol,
            open_price = EXCLUDED.open_price,
            high_price = EXCLUDED.high_price,
            low_price = EXCLUDED.low_price,
            close_price = EXCLUDED.close_price,
            volume = EXCLUDED.volume,
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
            signal_line = EXCLUDED.signal_line,
            rsi = EXCLUDED.rsi,
            obv = EXCLUDED.obv;
            
        """

    values = []
    for data in processed_data:
        date_str = data["date"]
        try: 
            parsed_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f+00:00")
        except ValueError:
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
    
        row= (
            stock_id,
            stock_symbol,
            parsed_date.date(),
            data["open"],
            data["high"],
            data["low"],
            data["close"],
            data["volume"],
            data["moving_avg_3"],
            data["moving_avg_6"],
            data["moving_avg_12"],
            data["upper_band"],
            data["lower_band"],
            data["monthly_return"],
            data["rolling_mean"],
            data["rolling_std"],
            data["ema12"],
            data["ema26"],
            data["MACD"],
            data["signal_line"],
            data['RSI'],
            data['OBV'],
        )
        values.append(row)

        # Debug logging to ensure matching values
    # print(f"\n🔹 Executing insert for {stock_symbol} on {parsed_date.date()}")
    # print(f"🔹 Values ({len(values)}): {values}")

    try:
        execute_values(cursor, insert_query, values)
        conn.commit()
        print(f"✅ Batch insert/update complete for {stock_symbol}: {len(values)} rows.")
    except Exception as e:
        conn.rollback()
        print(f"❌ SQL error: {e}")
    finally:
        cursor.close()
        conn.close()
