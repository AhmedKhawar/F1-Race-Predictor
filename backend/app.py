from flask import Flask, request, jsonify
import pickle
import os
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://f1-race-predictor-52a4d.web.app"])
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "ml", "model.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

drivers = pd.read_csv(os.path.join(BASE_DIR, "dataset", "raw", "drivers.csv"))
constructors = pd.read_csv(os.path.join(BASE_DIR, "dataset", "raw", "constructors.csv"))
circuits = pd.read_csv(os.path.join(BASE_DIR, "dataset", "raw", "circuits.csv"))


@app.route("/")
def home():
    return {
        "message": "F1 Race Predictor API Running"
    }


@app.route("/drivers", methods=["GET"])
def get_drivers():
    data = drivers[["driverId", "forename", "surname"]].copy()
    data["name"] = data["forename"] + " " + data["surname"]

    result = data[["driverId", "name"]].to_dict(orient="records")

    return jsonify(result)


@app.route("/constructors", methods=["GET"])
def get_constructors():
    result = constructors[
        ["constructorId", "name"]
    ].to_dict(orient="records")

    return jsonify(result)


@app.route("/circuits", methods=["GET"])
def get_circuits():
    result = circuits[
        ["circuitId", "name"]
    ].to_dict(orient="records")

    return jsonify(result)


@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    required = [
        "driverId",
        "constructorId",
        "circuitId",
        "qualifyingPosition"
    ]

    for field in required:
        if field not in data:
            return jsonify({
                "error": f"{field} is required"
            }), 400

    features = [[
        int(data["driverId"]),
        int(data["constructorId"]),
        int(data["circuitId"]),
        int(data["qualifyingPosition"])
    ]]

    prediction = model.predict(features)

    return jsonify({
        "predicted_position": round(float(prediction[0]))
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
