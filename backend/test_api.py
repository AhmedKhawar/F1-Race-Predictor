import requests

url = "http://127.0.0.1:5000/predict"

data = {
    "driverId": 1,
    "constructorId": 1,
    "circuitId": 1,
    "qualifyingPosition": 2
}

response = requests.post(url, json=data)

print(response.json())