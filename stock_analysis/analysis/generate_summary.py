import pandas as pd

def generate_summary(df, symbol):
    
    df.reset_index(inplace=True)  # This moves 'date' from the index to a column
    print(df.columns)
    print(df.head)
    if 'date' not in df.columns:
        raise KeyError("'date' column is missing from the DataFrame")
   
    # Format the summary data as a dictionary
    summary = {
        'symbol': symbol,
        'latest_date': df['date'].iloc[-1],
        'latest_close': df['close'].iloc[-1],
        'moving_avg_3': df['moving_avg_3'].iloc[-1],
        'moving_avg_6': df['moving_avg_6'].iloc[-1],
        'moving_avg_12': df['moving_avg_12'].iloc[-1],
        'upper_band': df['upper_band'].iloc[-1],
        'lower_band': df['lower_band'].iloc[-1],
        'monthly_return': df['monthly_return'].iloc[-1],
        'macd': df['macd'].iloc[-1],
        'signal_line': df['signal_line'].iloc[-1]
    }

    return summary

# Example usage:
# Assuming df is your DataFrame and 'AAPL' is the stock symbol
# df = pd.read_csv('your_data.csv')
# summary = generate_summary(df, 'AAPL')
# print(summary)
