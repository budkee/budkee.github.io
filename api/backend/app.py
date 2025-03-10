from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/portfolio")
def portfolio():
    return jsonify({"message": "Portfolio Page", "url": "https://budkee.github.io/"})

@app.route("/sales")
def sales():
    return jsonify({"message": "Sales Page", "url": "https://budkee.github.io/sales"})

if __name__ == "__main__":
    app.run(debug=True)