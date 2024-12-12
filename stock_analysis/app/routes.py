from flask import Blueprint, jsonify, request
import threading
import json
import pandas as pd
from analysis.data_retrieval import get_stock_data
from analysis.data_analysis import analyze_stock_data
from analysis.generate_summary import generate_summary
from analysis.data_visualization import generate_plots 

routes = Blueprint("routes", __name__)

@routes.route("/analyze/<symbol>", methods=["GET"])
def analyze(symbol):
    # Step 1: Get stock data
    data = get_stock_data(symbol)
    if data is None or data.empty:
        return jsonify({"error": f"No data found for {symbol}"}), 404

    # Step 2: Ensure 'date' column exists and convert it to datetime
    # print("First rows of data:", data.head())
    # print("columns in data", data.columns)
    if "date" not in data.columns or data['date'].isnull().all():
       
        return jsonify({"error": "'date' column is missing or contains invalid entries"}), 400

    data['date'] = pd.to_datetime(data['date'], errors='coerce')
    
    # Step 3: Perform analysis on the stock data
    df = analyze_stock_data(data)
    if df is None:
        return jsonify({"error": "Data analysis failed."}), 500

    # Step 4: Generate summary of the analysis
    try:
        summary_json = generate_summary(df, symbol)
    except KeyError as e:
        return jsonify({"error": str(e)}), 500
    
    # plot_paths = generate_plots(symbol, df)
    
    # Step 5: Return the summary as JSON
    return jsonify(summary_json), 200

