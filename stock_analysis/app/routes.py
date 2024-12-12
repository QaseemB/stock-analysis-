from flask import Blueprint, jsonify, request
import threading
import pandas as pd
from analysis.data_retrieval import get_stock_data
from analysis.data_analysis import analyze_stock_data
from analysis.generate_summary import generate_summary
from analysis.data_visualization import generate_plots
from analysis.report_generation import create_pdf_report
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
        df = analyze_stock_data(data)
        if df is None:
            return jsonify({"error": "Data analysis failed."}), 500

        # Step 4: Generate summary
        summary_json = generate_summary(df, symbol)

        # Step 5: Generate plots
        plot_paths = generate_plots_in_main_thread(symbol, df)

        plot_pdf_path = create_pdf_report_in_main_thread(symbol, plot_paths, df)

        df_json = df.to_json(orient='records', date_format='iso')  # Use 'records' for a list of row objects

        # Step 6: Return response
        return jsonify({
            "summary": summary_json,
            "plots": plot_paths,
            "pdf_report": plot_pdf_path,
            "data": df_json,
        }), 200

    except Exception as e:
        logging.error(f"An error occurred during analysis: {e}")
        return jsonify({"error": "An internal error occurred"}), 500
