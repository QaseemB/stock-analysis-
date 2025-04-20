from stock_analysis.utils.sql_connect import connect_to_sql
import json

def upsert_plotly(symbol, plot_json):
    # Connect to the database
    conn = connect_to_sql()
    cur = conn.cursor()

    query = """
    INSERT INTO stock_visualizations (symbol, interactive_plot) 
    VALUES (%s, %s)
    ON CONFLICT (symbol) DO UPDATE SET interactive_plot = EXCLUDED.interactive_plot;
    """
    cur.execute(query, (symbol, json.dumps(plot_json)))
    
    conn.commit()
    cur.close()
    conn.close()