from flask import Flask
from app.routes import routes
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.register_blueprint(routes)

load_dotenv()


@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    port =  os.getenv("PORT", 5000)
    app.run(debug=True, host='0.0.0.0', port=int(port))
