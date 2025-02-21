from datetime import datetime
import pandas as pd

def transform_to_processed_data_sql(df: pd.DataFrame, symbol: str) -> list:
    """
    Transforms analyzed stock data into a list of dictionaries suitable for SQL insertion.
    
    Each dictionary represents one row for the SQL table `stock_analysis` and includes:
    - date
    - moving_avg_3, moving_avg_6, moving_avg_12
    - upper_band, lower_band
    - monthly_return, rolling_mean, rolling_std
    - ema12, ema26, macd, signal_line
    
    Args:
        df (pd.DataFrame): The analyzed stock data as a DataFrame.
        symbol (str): The stock symbol (e.g., "META").
        
    Returns:
        list: A list of dictionaries, each representing a processed row.
    """
    # Ensure the 'date' column exists and convert it to datetime
    if "date" not in df.columns:
        raise ValueError(f"Missing 'date' column in DataFrame! Available columns: {df.columns.tolist()}")
        
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    
    processed_list = []
    
    # Iterate over each row in the DataFrame
    for _, row in df.iterrows():
        try:
            # Build a dictionary for the current row with the required fields.
            processed_row = {
                "date": row["date"].strftime("%Y-%m-%d") if pd.notnull(row["date"]) else None,
                "symbol": symbol,
                # "open": row.get("open", 0.0),
                # "close": row["close"],
                # "high": row["high"],
                # "low": row["low"],
                # "volume": row.get("volume", 0.0),
                "moving_avg_3": row.get("moving_avg_3", 0.0),
                "moving_avg_6": row.get("moving_avg_6", 0.0),
                "moving_avg_12": row.get("moving_avg_12", 0.0),
                "upper_band": row.get("upper_band", 0.0),
                "lower_band": row.get("lower_band", 0.0),
                "monthly_return": row.get("monthly_return", 0.0),
                "rolling_mean": row.get("rolling_mean", 0.0),
                "rolling_std": row.get("rolling_std", 0.0),
                "ema12": row.get("ema12", 0.0),
                "ema26": row.get("ema26", 0.0),
                "macd": row.get("macd", 0.0),
                "signal_line": row.get("signal_line", 0.0)
            }
            processed_list.append(processed_row)
        except Exception as e:
            print(f"Error processing row: {e}")
    
    return processed_list
