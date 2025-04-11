import pandas as pd

def generate_summary(df, symbol):
    
    df.reset_index(inplace=True)  # This moves 'date' from the index to a column
    # print(df.columns)
    # print(df.head)
    if 'date' not in df.columns:
        raise KeyError("'date' column is missing from the DataFrame")
   
    # Format the summary data as a dictionary
    summary = {
        'symbol': symbol,
        'latest_date': df['date'].iloc[-1],
        'latest_open': round(df['open'].iloc[-1],2),
        'latest_close': round(df['close'].iloc[-1],2),
        'moving_avg_3':round(df['moving_avg_3'].iloc[-1],2),
        'moving_avg_6': round(df['moving_avg_6'].iloc[-1],2),
        'moving_avg_12': round(df['moving_avg_12'].iloc[-1],2),
        'upper_band': round(df['upper_band'].iloc[-1],2),
        'lower_band':round(df['lower_band'].iloc[-1],2),
        'monthly_return':round(df['monthly_return'].iloc[-1],2),
        'MACD': round(df['macd'].iloc[-1],2),
        'signal_line': round(df['signal_line'].iloc[-1],2),
        'OBV': round(df['obv'].iloc[-1],2),
        'RSI': round(df['rsi'].iloc[-1],2) if 'rsi' in df.columns else None
    }

    return summary

# Example usage:
# Assuming df is your DataFrame and 'AAPL' is the stock symbol
# df = pd.read_csv('your_data.csv')
# summary = generate_summary(df, 'AAPL')
# print(summary)
