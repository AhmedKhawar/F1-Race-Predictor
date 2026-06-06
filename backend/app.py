from flask import Flask, request, jsonify
import pickle
import os
import pandas as pd


app = Flask(__name__)

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "../ml/model.pkl"
)

with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)


drivers = pd.read_csv("../dataset/raw/drivers.csv")
constructors = pd.read_csv("../dataset/raw/constructors.csv")
circuits = pd.read_csv("../dataset/raw/circuits.csv")


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
    app.run(debug=True)