from flask import Flask, request, jsonify
import joblib
import numpy as np

model = joblib.load("model.pkl")

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the ML Model API"})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"})   


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    features = np.array(data["features"]).reshape(1, -1)
    prediction = model.predict(features)[0]
    return jsonify({"prediction": prediction})

if __name__ == "__main__":
    app.run(debug=True)

