from datetime import datetime
import pandas as pd

def safe_float(val):
    """
    Safely convert a value to a native float or return None if not convertible.
    Handles NaN, pd.NA, and NumPy float types.
    """
    if pd.isnull(val):
        return None
    try:
        return float(val)
    except (TypeError, ValueError):
        return None

def transform_to_processed_data_sql(df: pd.DataFrame, symbol: str) -> list:
    """
    Transforms analyzed stock data into a list of dictionaries suitable for SQL insertion.
    Converts all numeric values to native floats and replaces NaNs with None.
    """
    if "date" not in df.columns:
        raise ValueError(f"Missing 'date' column in DataFrame! Available columns: {df.columns.tolist()}")
    
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    
    processed_list = []
    
    for _, row in df.iterrows():
        try:
            processed_row = {
                "date": row["date"].strftime("%Y-%m-%d") if pd.notnull(row["date"]) else None,
                "symbol": symbol,
                "open": safe_float(row.get("open")),
                "close": safe_float(row.get("close")),
                "high": safe_float(row.get("high")),
                "low": safe_float(row.get("low")),
                "volume": safe_float(row.get("volume")),
                "moving_avg_3": safe_float(row.get("moving_avg_3")),
                "moving_avg_6": safe_float(row.get("moving_avg_6")),
                "moving_avg_12": safe_float(row.get("moving_avg_12")),
                "upper_band": safe_float(row.get("upper_band")),
                "lower_band": safe_float(row.get("lower_band")),
                "monthly_return": safe_float(row.get("monthly_return")),
                "rolling_mean": safe_float(row.get("rolling_mean")),
                "rolling_std": safe_float(row.get("rolling_std")),
                "ema12": safe_float(row.get("ema12")),
                "ema26": safe_float(row.get("ema26")),
                "MACD": safe_float(row.get("macd")),
                "signal_line": safe_float(row.get("signal_line")),
                "OBV": safe_float(row.get("obv")),
                "RSI": safe_float(row.get("rsi")),
            }
            processed_list.append(processed_row)
            # print(pd.dataframe(processed_list).head(3))
        except Exception as e:
            print(f"❌ Error processing row: {e}")
    
    return processed_list
