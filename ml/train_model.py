import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle

print("Loading datasets...")

races = pd.read_csv("../dataset/raw/races.csv")
results = pd.read_csv("../dataset/raw/results.csv")
qualifying = pd.read_csv("../dataset/raw/qualifying.csv")

print("Merging datasets...")

# Merge qualifying and results
df = qualifying.merge(
    results,
    on=["raceId", "driverId", "constructorId"],
    how="inner"
)

# Add circuit information
df = df.merge(
    races[["raceId", "circuitId"]],
    on="raceId",
    how="left"
)

print("Selecting features...")

df = df[[
    "driverId",
    "constructorId",
    "circuitId",
    "position_x",
    "positionOrder"
]]

df.columns = [
    "driverId",
    "constructorId",
    "circuitId",
    "qualifyingPosition",
    "finishPosition"
]

# Remove missing values
df = df.dropna()

print(f"Training samples: {len(df)}")

X = df[[
    "driverId",
    "constructorId",
    "circuitId",
    "qualifyingPosition"
]]

y = df["finishPosition"]

print("Training model...")

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

print("Saving model...")

with open("model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model saved successfully!")