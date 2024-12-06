from flask import Blueprint, jsonify, request
from analysis.data_retrieval import get_stock_data
from analysis.data_analysis import analyze_stock_data

routes = Blueprint("routes", __name__)

@routes.route("/analyze/<symbol>", methods=["GET"])
def analyze(symbol):
    data = get_stock_data(symbol)
    if not data:
        return jsonify({"error": f"No data found for {symbol}"}), 404

    df = analyze_stock_data(data)
    return jsonify(df.to_dict())
