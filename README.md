# 🏎️ F1 Race Predictor

Predict where a Formula 1 driver will finish a race, based on where they qualified.

Give the model a **driver**, a **constructor**, a **circuit** and a **qualifying position**, and it returns a **predicted finishing position**. This repository contains the full backend: the training pipeline, the trained model and the Flask REST API that serves predictions to a Flutter app.

⚙️ **Live API:** [f1-race-predictor-l291.onrender.com](https://f1-race-predictor-l291.onrender.com/) (free to use, no API key needed)

---

## Table of Contents

- [Live API](#live-api)
- [How It Works](#how-it-works)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Flutter Integration](#flutter-integration)
- [Model Details](#model-details)
- [Limitations](#limitations)

---

## Live API

The backend is hosted, so you can call it directly from your own app, script or terminal without running anything locally.

**Base URL**

```
https://f1-race-predictor-l291.onrender.com
```

**Check that it's running**

```bash
curl https://f1-race-predictor-l291.onrender.com/
```

```json
{ "message": "F1 Race Predictor API Running" }
```

> If the service has been idle, the first request may take a few seconds while it wakes up. Later requests are fast.

### Try it in three steps

**1. Find the IDs you need.** Predictions use IDs, not names, so look them up first:

```bash
curl https://f1-race-predictor-l291.onrender.com/drivers
curl https://f1-race-predictor-l291.onrender.com/constructors
curl https://f1-race-predictor-l291.onrender.com/circuits
```

**2. Request a prediction.**

```bash
curl -X POST https://f1-race-predictor-l291.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"driverId": 1, "constructorId": 131, "circuitId": 1, "qualifyingPosition": 2}'
```

**3. Read the result.**

```json
{ "predicted_position": 3 }
```

### Use it from code

**JavaScript**

```javascript
const res = await fetch("https://f1-race-predictor-l291.onrender.com/predict", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    driverId: 1,
    constructorId: 131,
    circuitId: 1,
    qualifyingPosition: 2,
  }),
});
const data = await res.json();
console.log(data.predicted_position);
```

**Python**

```python
import requests

res = requests.post(
    "https://f1-race-predictor-l291.onrender.com/predict",
    json={"driverId": 1, "constructorId": 131, "circuitId": 1, "qualifyingPosition": 2},
)
print(res.json()["predicted_position"])
```

---

## How It Works

```
Ergast CSV data  →  Preprocessing  →  Random Forest training  →  model.pkl  →  Flask API  →  Flutter app
```

1. Historical race data (results, qualifying, drivers, constructors, circuits, races) is loaded from CSV files.
2. The data is preprocessed into one training row per driver per race.
3. A Random Forest model is trained and saved as `model.pkl`.
4. The Flask API loads the model and exposes endpoints for lookups and predictions.
5. The Flutter frontend lets users pick their inputs and displays the predicted result.

---

## Tech Stack

| Layer       | Technology                              |
| ----------- | --------------------------------------- |
| Language    | Python                                  |
| Backend     | Flask (REST API)                        |
| ML model    | Random Forest, serialized to `model.pkl` |
| Data        | Ergast historical F1 dataset (CSV)      |
| Frontend    | Flutter (consumes this API)             |
| Hosting     | Render                                  |

---

## Project Structure

```
F1-Race-Predictor/
├── backend/
│   ├── app.py              # Flask API
│   ├── requirements.txt    # Python dependencies
│   └── test_api.py         # API tests
├── dataset/
│   └── raw/
│       ├── circuits.csv
│       ├── constructors.csv
│       ├── drivers.csv
│       ├── qualifying.csv
│       ├── races.csv
│       └── results.csv
├── ml/
│   ├── train_model.py      # Model training script
│   └── model.pkl           # Trained model (generated)
└── README.md
```

---

## Getting Started

Want to run it yourself instead of using the hosted API?

### 1. Install dependencies

From the project root:

```bash
pip install -r backend/requirements.txt
```

### 2. Train the model

```bash
cd ml
python train_model.py
```

This generates `model.pkl`.

### 3. Run the backend

```bash
cd backend
python app.py
```

The server starts at **http://127.0.0.1:5000**.

---

## API Reference

| Environment | Base URL                                        |
| ----------- | ----------------------------------------------- |
| Live        | `https://f1-race-predictor-l291.onrender.com`   |
| Local       | `http://127.0.0.1:5000`                         |

The examples below use the local URL. Swap in the live one to call the hosted API.

### `GET /`

Health check. Returns a message confirming the API is running.

```json
{ "message": "F1 Race Predictor API Running" }
```

### `GET /drivers`

Returns all drivers.

```json
[
  { "driverId": 1, "name": "Lewis Hamilton" }
]
```

### `GET /constructors`

Returns all constructors.

```json
[
  { "constructorId": 131, "name": "Mercedes" }
]
```

### `GET /circuits`

Returns all circuits.

```json
[
  { "circuitId": 1, "name": "Albert Park Grand Prix Circuit" }
]
```

### `POST /predict`

Predicts the finishing position for the given inputs.

**Request body**

| Field                | Type | Description                        |
| -------------------- | ---- | ---------------------------------- |
| `driverId`           | int  | ID from `GET /drivers`             |
| `constructorId`      | int  | ID from `GET /constructors`        |
| `circuitId`          | int  | ID from `GET /circuits`            |
| `qualifyingPosition` | int  | Grid position the driver qualified in |

```json
{
  "driverId": 1,
  "constructorId": 131,
  "circuitId": 1,
  "qualifyingPosition": 2
}
```

**Response**

```json
{
  "predicted_position": 3
}
```

**Example with curl**

```bash
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"driverId": 1, "constructorId": 131, "circuitId": 1, "qualifyingPosition": 2}'
```

---

## Flutter Integration

The app follows a simple flow:

1. On launch, load dropdown options from `GET /drivers`, `GET /constructors` and `GET /circuits`.
2. The user selects a driver, constructor and circuit, and enters a qualifying position.
3. The app sends the selections to `POST /predict`.
4. The backend returns `predicted_position`, which the app shows on the result screen.

**Home screen:** driver, constructor and circuit dropdowns, a qualifying position input and a Predict button.
**Result screen:** the predicted finishing position (for example, **P3**).

---

## Model Details

- **Algorithm:** Random Forest
- **Training data:** historical Formula 1 data from the Ergast dataset
- **Features:** driver ID, constructor ID, circuit ID, qualifying position
- **Target:** final race finishing position

---

## Limitations

- The model uses only four inputs. It does not account for weather, tyre strategy, safety cars, penalties, mechanical failures or recent form.
- Driver, constructor and circuit are fed in as IDs, so the model can only work with entities that appear in the training data.
- Output is a single predicted position, with no confidence score or probability distribution.

---

## Future Improvements

- Add form-based features such as recent results and team performance trends
- Report model accuracy metrics (for example, mean absolute error of predicted vs. actual position)
- Return prediction confidence alongside the position
- Add input validation and clearer error responses to `/predict`

---

## Data Source

Historical race data comes from the Ergast Formula 1 dataset.
