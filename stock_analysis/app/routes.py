from flask import Blueprint, jsonify, request, send_from_directory
import os
import threading
import pandas as pd
import json
from pydantic import ValidationError
from analysis.data_retrieval import get_stock_data
from analysis.data_analysis import analyze_stock_data
from analysis.generate_summary import generate_summary
from analysis.data_visualization import generate_plots
from analysis.report_generation import create_pdf_report
from analysis.gen_interactive_plt import gen_interactive_plt
from utils.data_transform import transform_to_processed_data
from utils.mongo_connect import db
from utils.config import config
import matplotlib
import logging

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
        
        
      

        processed_data = transform_to_processed_data(df,symbol)

        processed_data_collection = db[config['DB_PROCESSED_COLLECTION']]

        insert_result = processed_data_collection.insert_one(processed_data)

        # Step 4: Generate summary
        summary_json = generate_summary(df, symbol)

        # Step 5: Generate plots
        plot_paths = generate_plots_in_main_thread(symbol, df)




        df_json = df.to_json(orient='records', date_format='iso')  # Use 'records' for a list of row objects

        # Generate interactive plot this will now return json
        interactive_plot_json = gen_interactive_plt(symbol,df)

        # Parse the JSON string into a Python dictionary
        interactive_plot_object = json.loads(interactive_plot_json)

        response = {
            "summary": summary_json,
            "static_plots": plot_paths,
            "interactive_plot": interactive_plot_object,
            "data": df_json,
            "message": f"Data for {symbol} analyzed and saved to MongoDB successfully.",
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
def serve_stock_report(symbol, filename):
    directory = os.path.join('stockreport', symbol)
    if not os.path.exists(os.path.join(directory, filename)):
        return jsonify({"error": "File not found"}), 404
    return send_from_directory(directory, filename, as_attachment=True)