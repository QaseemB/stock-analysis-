from flask import Blueprint, jsonify, request, send_from_directory, send_file, make_response
from flask_cors import cross_origin
from werkzeug.exceptions import NotFound
import mimetypes
import os
import threading
import pandas as pd
import json
from pydantic import ValidationError
from stock_analysis.services.data_retrieval import get_stock_data
from analysis.data_analysis import analyze_stock_data
from stock_analysis.transfomer.stock_summary_transformer import generate_summary
from stock_analysis.renderers.matplotlib_png_renderer import generate_plots
from stock_analysis.services.pdf_report_generation import create_pdf_report
from stock_analysis.renderers.interactive_plot_renderer import gen_interactive_plt
from utils.transform_data import transform_to_processed_data_sql
from stock_analysis.services.insert_processed_data import insert_processed_data
from utils.store_plots_in_sql import store_plot_in_db
from utils.sql_connect import connect_to_sql
# from utils.mongo_connect import db
from stock_analysis.config.settings import config
import matplotlib
import logging



## ideal setup for safe memory usage 
##def get_analysis(symbol):
 # Just grab precomputed values (JSON/summary/plot URLs)
   ## analysis = fetch_summary_from_db(symbol)
   ## graph_urls = get_plot_urls_from_s3(symbol)  
   ## return jsonify({
   ##     "symbol": symbol,
   ##     "summary": analysis,
    ##    "plots": graph_urls
   ## })

# Configure Matplotlib for non-interactive mode
matplotlib.use('Agg')

# Set up logging
logging.basicConfig(level=logging.INFO)

routes = Blueprint("routes", __name__)

def generate_plots_in_main_thread(symbol, df):
    try:
        return generate_plots(symbol, df)
    except Exception as e:
        logging.error(f"Error generating plots for {symbol}: {e}")
        return {}
    
def create_pdf_report_in_main_thread(symbol, plot_paths, df):
    try:
        print (f"Creating PDF report for {symbol}...")
        return create_pdf_report(symbol, plot_paths, df)
    except Exception as e:
        logging.error(f"Error generating PDF report for {symbol}: {e}")
        return {}
    
@routes.route("/api/analyze/<symbol>", methods=["GET"])
def analyze(symbol):
    if not symbol:
        return jsonify({'error': 'Stock symbol is required'}), 400
   
    try:
        # Step 1: Get stock data
        data = get_stock_data(symbol)
        if data is None or data.empty:
            return jsonify({"error": f"No data found for {symbol}"}), 404

        # Step 2: Ensure 'date' column exists and is valid
        if "date" not in data.columns or data['date'].isnull().all():
            return jsonify({"error": "'date' column is missing or contains invalid entries"}), 400
        data['date'] = pd.to_datetime(data['date'], errors='coerce')

        # Step 3: Analyze the data
        df = analyze_stock_data(data, symbol)
        if df is None:
            return jsonify({"error": "Data analysis failed."}), 500
        
        df.reset_index(inplace=True)
        
        
      

        processed_data = transform_to_processed_data_sql(df,symbol)

        for entry in processed_data:
            insert_processed_data(symbol, entry)  # Your SQL insertion function
    

        # Step 4: Generate summary
        summary_json = generate_summary(df, symbol)

        # Step 5: Generate plots
        plot_paths = generate_plots_in_main_thread(symbol, df)

        if plot_paths: 
            pdf_report = create_pdf_report_in_main_thread(symbol, plot_paths, df)
            
        else: 
            logging.warning(f"skipping pdf generation for {symbol} due to missing plots")




        df_json = df.to_json(orient='records', date_format='iso')  # Use 'records' for a list of row objects

        # Generate interactive plot this will now return json
        interactive_plot_json = gen_interactive_plt(symbol,df)

        # Parse the JSON string into a Python dictionary
        interactive_plot_object = json.loads(interactive_plot_json)

        if interactive_plot_object:
            store_plot_in_DB = store_plot_in_db(symbol, interactive_plot_object,)
            print(f"storing plots for {symbol} in postgreSql")
        else: 
            logging.warning(f"skipping plot storage for {symbol} due to missing plot")

        # Parse the JSON string into a Python dictionary
        # interactive_plot_object = json.loads(interactive_plot_json)

        response = {
            "summary": summary_json,
            "static_plots": plot_paths,
            "interactive_plot": interactive_plot_object,
            "data": df_json,
            "message": f"Data for {symbol} analyzed and saved to PostgreSql successfully.",
            # "inserted_ids": [str(_id) for _id in insert_result.inserted_ids],  # Return inserted IDs
        }


        # Step 6: Return response
        return jsonify(response), 200
    except ValidationError as e:
        logging.error(f"Validation error: {e}")
        return jsonify({"error": "Data validation failed","details": str(e)}), 400 
    except Exception as e:
        logging.error(f"An error occurred during analysis: {e}")
        return jsonify({"error": "An internal error occurred", "details": str(e)}), 500
    


@routes.route('/stockreport/<symbol>/<filename>', methods=['GET'])
@cross_origin()  # ← this handles CORS for most cases
def serve_stock_report(symbol, filename):
    directory = os.path.join('stockreport', symbol)
    filepath = filepath = os.path.join(directory, filename)
    try:
       # Guess MIME type using file extension
        mime_type, _ = mimetypes.guess_type(filepath)
        response = make_response(send_from_directory(directory, filename))
        response.headers['Access-Control-Allow-Origin'] = '*'
        if mime_type:
            response.headers['Content-Type'] = mime_type
        return response
    except NotFound:
        return jsonify({"error": "File not found"}), 404
    # return send_from_directory(directory, filename, as_attachment=True)


@routes.route("/api/analyze/all", methods=["GET"])
def analyze_all_stocks():
    stock_symbols = [
  'AAPL', 'GOOG', 'MSFT', 'AMZN', 'META', 
  'IBM','TSLA','NVDA','AVGO','TSM','JPM','MA',
  'COST','PG','NFLX','JNJ','BAC','CRM','TM','KO','ORCL', 'D', 'HD', 'ABBV', 'PLTR', 'ABT', 'MRK', 'AXP', 'QCOM', 'ADBE',
  'AMD', 'T', 'VZ', 'DIS', 'NKE', 'PFE', 'PEP', 'CSCO', 'CMCSA', 'XOM', 
  'WMT', 'BMY', 'INTC', 'UNH', 'CVX', 'LLY', 'MCD', 'HON', 'NEE', 'TXN', 
  'PM', 'LOW', 'UPS', 'SCHW', 'MS', 'AMGN', 'CAT', 'GS', 'RTX', 'SPGI', 
  'BLK', 'BKNG', 'ISRG', 'MDT', 'SYK', 'LMT', 'DE', 'ADP', 'NOW', 'TMO', 
  'UNP', 'AMT', 'CB', 'CCI', 'ZTS', 'GILD', 'FIS', 'EL', 'MO', 'DUK', 
  'SO', 'MMM', 'BDX', 'APD', 'C', 'USB', 'PNC', 'CL', 'DHR', 'ITW', 'WM', 
  'SHW', 'ECL', 'FISV', 'AON', 'HUM', 'PSA', 'NSC', 'ETN', 'ROP', 'MAR', 
  'KMB', 'AEP', 'SBUX', 'LRCX', 'ATVI', 'ORLY', 'MCO', 'KLAC', 'CTAS', 
  'EQIX', 'ILMN', 'REGN', 'IDXX', 'MTD', 'CDNS', 'SNPS', 'FTNT', 'PAYC', 
  'ANSS', 'VRSK', 'MSCI', 'FLT', 'CPRT', 'TDG', 'WST', 'RMD', 'ALGN', 
  'STE', 'TECH', 'BIO', 'TER', 'KEYS', 'HUBS', 'SEDG', 'ENPH', 'TEAM', 
  'OKTA', 'ZS', 'CRWD', 'DDOG', 'DOCU', 'FSLY', 'NET', 'PLUG', 'BLD', 
  'PTON', 'ROKU', 'SQ', 'TWLO', 'U', 'ZM', 'ZSAN', 'VOO','QQQ','DIA', 'VTI'
];  # Add your complete list of stocks
    results = []
    for symbol in stock_symbols:
        try:
            response = analyze(symbol)  # Directly calling the analyze function
            results.append({"symbol": symbol, "status": "Success", "data": response})
        except Exception as e:
            results.append({"symbol": symbol, "status": "Failed", "error": str(e)})
    return jsonify(results), 200

@routes.route("/api/plots/<symbol>", methods=["GET"])

def get_plot(symbol):
    conn = connect_to_sql()
    cur = conn.cursor()

    query = "SELECT interactive_plot FROM stock_visualizations WHERE symbol = %s;"
    cur.execute(query, (symbol,))
    result = cur.fetchone()

    cur.close()
    conn.close()

    if result:
        return jsonify({"interactive_plot": result[0]})
    return jsonify({"error": "Plot not found"}), 404

