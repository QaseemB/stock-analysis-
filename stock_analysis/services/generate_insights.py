from utils.indicator_glossary import indicator_glossary

def generate_insights(df):
    latest = df.iloc[-1]
    insights = {}

    for key, info in indicator_glossary.items():
        try:
            insight = info["insight"](latest)
            insights[key] = insight
        except Exception as e:
            insights[key] = f"⚠️ Error generating {key} insight: {e}"
    
    return insights