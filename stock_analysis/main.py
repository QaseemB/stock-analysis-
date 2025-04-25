from flask import Flask
from flask_cors import CORS
from stock_analysis.app.routes import routes
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.register_blueprint(routes)

load_dotenv()
# Allow specific origins

CORS(app, resources={r"/*": {"origins": "https://stock-analysis-0f8t.onrender.com"}})


@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    port =  int(os.getenv("PORT_FLASK", 5001))
    app.run(debug=True, host='0.0.0.0', port=port )

    # port=int(port)+ 1 