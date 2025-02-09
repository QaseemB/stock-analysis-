from flask import Flask
from flask_cors import CORS
from app.routes import routes
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.register_blueprint(routes)

load_dotenv()
# Allow specific origins

# CORS(app, resources={r"/*": {"origins": "https://stock-analysis-0f8t.onrender.com"}})


@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    port =  os.getenv("PORT_PYTHON", 5000)
    app.run(debug=True, host='0.0.0.0', port=int(port)+ 1 )
