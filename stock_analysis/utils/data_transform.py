from datetime import datetime
from models.ProcessedDataSchema import ProcessedDataSchema, AnalysisSchema
import pandas as pd




def transform_to_processed_data(df: pd.DataFrame, symbol: str) -> dict:
    """
    Transforms analyzed stock data into the schema required for MongoDB.

    Args:
        df (pd.DataFrame): The analyzed stock data as a DataFrame.
        symbol (str): The stock symbol (e.g., "META").

    Returns:
        dict: A dictionary representing the processed data in the required schema.
    """

    # ✅ Ensure 'date' exists and is in correct format
    if "date" not in df.columns:
        raise ValueError(f"Missing 'date' column in DataFrame! Available columns: {df.columns.tolist()}")
    

    df["date"] = pd.to_datetime(df["date"], errors= "coerce")

    
    # Create a list to hold analysis data for each row
    analysis_data = []

    # Iterate over each row in the DataFrame
    for _, row in df.iterrows():
        try: # Try to create an Analysis object

            analysis = AnalysisSchema(
                date=row.get("date", None) if isinstance(row["date"], datetime) else None,  # Ensure datetime
                open =row["open"],
                high = row["high"],
                low = row["low"],
                close = row["close"],
                volume = row["volume"],
                moving_avg_3 = row.get("moving_avg_3", 0.0),
                moving_avg_6 = row.get("moving_avg_6", 0.0),
                moving_avg_12 = row.get("moving_avg_12", 0.0),
                upper_band = row.get("upper_band", 0.0),
                lower_band = row.get("lower_band", 0.0),
                monthly_return = row["monthly_return"],
                rolling_mean = row["rolling_mean"],
                rolling_std = row["rolling_std"],
                ema12 = row.get("ema12", 0.0),
                ema26 = row.get("ema26", 0.0),
                macd = row.get("macd", 0.0),
                signal_line = row.get("signal_line", 0.0)
            )
            analysis_data.append(analysis.dict())
        except Exception as e:
            print(f"Missing key in row: {e}")

            
     
    processed_data = ProcessedDataSchema( 
            symbol=symbol,
            latestRefresh = datetime.now().isoformat(),
            analysis = analysis_data # Current timestamp
        )
    
    return processed_data.dict()
