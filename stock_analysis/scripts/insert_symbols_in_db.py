from stock_analysis.utils.sql_connect import connect_to_sql
from stock_analysis.utils.stock_list import stock_list

conn = connect_to_sql()
cursor = conn.cursor()

for symbol in stock_list:
    cursor.execute("""
        INSERT INTO stocks (symbol)
        VALUES (%s)
        ON CONFLICT (symbol) DO NOTHING;
    """, (symbol,))

conn.commit()
cursor.close()
conn.close()

print("✅ Stock symbols inserted.")