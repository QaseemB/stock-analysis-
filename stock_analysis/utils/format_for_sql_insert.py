def format_for_sql_insert(processed_list: list) -> list:
    """
    Converts a list of processed row dicts into a list of tuples,
    in the correct column order for SQL insert.
    """
    return [
        (
            row["date"],
            row["symbol"],
            row["open"],
            row["close"],
            row["high"],
            row["low"],
            row["volume"],
            row["moving_avg_3"],
            row["moving_avg_6"],
            row["moving_avg_12"],
            row["upper_band"],
            row["lower_band"],
            row["monthly_return"],
            row["rolling_mean"],
            row["rolling_std"],
            row["ema12"],
            row["ema26"],
            row["MACD"],
            row["signal_line"],
            row["OBV"],
            row["RSI"]
        )
        for row in processed_list
    ]
