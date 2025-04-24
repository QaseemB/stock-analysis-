from stock_analysis.utils.sql_connect import connect_to_sql

conn = connect_to_sql()
print("Connected successfully 🎉")
conn.close()

