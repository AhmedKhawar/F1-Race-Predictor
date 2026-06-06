# F1 Race Predictor Backend Documentation

## Overview

This project predicts the expected finishing position of a Formula 1 driver using historical race data and a trained Random Forest machine learning model.

The backend is built using Flask and exposes REST APIs that can be consumed by a Flutter frontend.

---

# Architecture

Dataset (CSV Files)
↓
Data Preprocessing
↓
Random Forest Training
↓
model.pkl
↓
Flask API
↓
Flutter Frontend

---

# Project Structure

F1-Race-Predictor/

backend/

* app.py
* requirements.txt
* test_api.py

dataset/raw/

* circuits.csv
* constructors.csv
* drivers.csv
* qualifying.csv
* races.csv
* results.csv

ml/

* train_model.py
* model.pkl

---

# Installation

Install dependencies:

pip install -r backend/requirements.txt

---

# Train Model

From project root:

cd ml

python train_model.py

This generates:

model.pkl

---

# Run Backend

From project root:

cd backend

python app.py

Server starts at:

http://127.0.0.1:5000

---

# Available APIs

## GET /drivers

Returns all drivers.

Example Response:

[
{
"driverId": 1,
"name": "Lewis Hamilton"
}
]

---

## GET /constructors

Returns all constructors.

Example Response:

[
{
"constructorId": 131,
"name": "Mercedes"
}
]

---

## GET /circuits

Returns all circuits.

Example Response:

[
{
"circuitId": 1,
"name": "Albert Park Grand Prix Circuit"
}
]

---

## POST /predict

Predicts finishing position.

Request:

{
"driverId": 1,
"constructorId": 131,
"circuitId": 1,
"qualifyingPosition": 2
}

Response:

{
"predicted_position": 3
}

---

# Flutter Integration Flow

1. Load drivers from:

GET /drivers

2. Load constructors from:

GET /constructors

3. Load circuits from:

GET /circuits

4. User selects:

* Driver
* Constructor
* Circuit
* Qualifying Position

5. Flutter sends:

POST /predict

6. Backend returns:

predicted_position

7. Display result on Result Screen.

---

# Expected Flutter Screens

Home Screen

* Driver Dropdown
* Constructor Dropdown
* Circuit Dropdown
* Qualifying Position Input
* Predict Button

Result Screen

Predicted Finish Position

P3

---

# Notes

The machine learning model is trained using historical Formula 1 data from the Ergast dataset.

Current prediction features:

* Driver ID
* Constructor ID
* Circuit ID
* Qualifying Position

Target:

* Final Race Finishing Position
