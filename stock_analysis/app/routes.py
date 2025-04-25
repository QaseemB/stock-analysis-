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
from stock_analysis.transfomer.stock_analysis_transformer import analyze_stock_data
from stock_analysis.transfomer.stock_summary_transformer import generate_summary
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

    
@routes.route("/api/analyze/<symbol>", methods=["GET"])
def analyze(symbol):
    if not symbol:
        return jsonify({'error': 'Stock symbol is required'}), 400
   
    try:
        cleaned_monthly_data = get_stock_data(symbol)
        if cleaned_monthly_data is None:
            print(f"Error: No data returned for symbol {symbol}")
            return None

        df = analyze_stock_data(cleaned_monthly_data,symbol)
    # print(df)
        if df is None:
            print(f"error: analysis failed something is wrong with the analyze_stock function")
            return None

        summary_json = generate_summary(df,symbol)

        response = {
            "summary": summary_json,
        }


        # Step 6: Return response
        return jsonify(response), 200
    except ValidationError as e:
        logging.error(f"Validation error: {e}")
        return jsonify({"error": "Data validation failed","details": str(e)}), 400 
    except Exception as e:
        logging.error(f"An error occurred during analysis: {e}")
        return jsonify({"error": "An internal error occurred", "details": str(e)}), 500
    





