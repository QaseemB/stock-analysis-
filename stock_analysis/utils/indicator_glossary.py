indicator_glossary = {
    "macd": {
        "description": "Momentum indicator comparing short vs long term EMAs",
        "insight": lambda v: "⬆️ Bullish momentum" if v > 0 else "⬇️ Bearish momentum"
    },
    "rsi": {
        "description": "Measures strength/speed of price changes",
        "insight": lambda v: (
            "⚠️ Overbought (possible reversal)" if v > 70 else
            "✅ Neutral" if 30 <= v <= 70 else
            "📉 Oversold (possible bounce)"
        )
    },
    "bollinger": {
        "description": "Volatility range based on moving average",
        "insight": lambda row: (
            "🔼 Price hitting upper band → strong uptrend"
            if row["close"] >= row["upper_band"] else
            "🔽 Price hitting lower band → possible reversal"
            if row["close"] <= row["lower_band"] else
            "✅ Price within normal range"
        )
    },
    "moving_avg": {
        "description": "Smooths price data to show trend direction",
        "insight": lambda row: (
            "📈 Short-term above long-term → upward trend"
            if row["moving_avg_3"] > row["moving_avg_12"] else
            "📉 Short-term below long-term → downward pressure"
        )
    },
    "obv": {
    "description": "Combines price direction and volume to show buying/selling pressure",
    "insight": lambda row: (
        "📈 OBV increasing → potential accumulation"
        if row["obv"] > row["obv"] - row["volume"] else
        "📉 OBV decreasing → potential distribution"
    )
}
}