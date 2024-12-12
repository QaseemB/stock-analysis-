from flask import Blueprint, jsonify, request
import threading
import json
import pandas as pd
import os
import matplotlib.pyplot as plt
from analysis.data_retrieval import get_stock_data
from analysis.data_analysis import analyze_stock_data
from analysis.generate_summary import generate_summary
from analysis.data_visualization import generate_plots 

routes = Blueprint("routes", __name__)

# Ensure matplotlib runs in non-interactive mode to avoid GUI issues
import matplotlib
matplotlib.use('Agg')  # Use Agg backend for non-interactive plotting

# Function to generate plots in the main thread
def generate_plots_in_main_thread(symbol, df, plot_paths):
    # Your existing plot generation logic goes here
    try:
        plot_paths.update(generate_plots(symbol, df))
    except Exception as e:
        print(f"Error generating plots: {e}")

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
    
    plot_paths = {}
    thread = threading.Thread(target=generate_plots_in_main_thread, args=(symbol, df, plot_paths))
    thread.start()
    thread.join()  # Ensure that the plots are generated before returning the response
    
    # Step 5: Return the summary as JSON
    return jsonify({
        "summary": summary_json,
        "plots": plot_paths  # This will return the paths to the generated plots
    }), 200
