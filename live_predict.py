import asyncio
import websockets
import json
import pandas as pd
import numpy as np
import joblib
import time

URI = "ws://10.199.115.128:8080/sensor/connect?type=android.sensor.accelerometer"

rf = joblib.load("rf_model.pkl")

WINDOW_SIZE = 50
SLIDE_SIZE = 25


def extract_features(df):

    ax = df["ax"]
    ay = df["ay"]
    az = df["az"]

    features = {
        "ax_mean": ax.mean(),
        "ax_std": ax.std(),
        "ax_min": ax.min(),
        "ax_max": ax.max(),

        "ay_mean": ay.mean(),
        "ay_std": ay.std(),
        "ay_min": ay.min(),
        "ay_max": ay.max(),

        "az_mean": az.mean(),
        "az_std": az.std(),
        "az_min": az.min(),
        "az_max": az.max(),

        "ax_energy": np.sum(ax**2),
        "ay_energy": np.sum(ay**2),
        "az_energy": np.sum(az**2),

        # SMA feature
        "sma": (ax.abs() + ay.abs() + az.abs()).mean()
    }

    return pd.DataFrame([features])


async def live_prediction():

    buffer = []

    async with websockets.connect(URI) as ws:

        print("Connected to ESP32")
        print("Waiting for gestures...\n")

        while True:

            msg = json.loads(await ws.recv())

            ax, ay, az = msg["values"]

            buffer.append([ax, ay, az])

            if len(buffer) >= WINDOW_SIZE:

                df = pd.DataFrame(
                    buffer[-WINDOW_SIZE:],
                    columns=["ax", "ay", "az"]
                )

                features = extract_features(df)

                start_time = time.perf_counter()

                prediction = rf.predict(features)[0]

                confidence = np.max(
                    rf.predict_proba(features)
                )

                latency_ms = (
                    time.perf_counter() - start_time
                ) * 1000

                print(
                    f"Prediction: {prediction:15s} "
                    f"Confidence: {confidence:.2%} "
                    f"Latency: {latency_ms:.2f} ms"
                )

                buffer = buffer[SLIDE_SIZE:]


asyncio.run(live_prediction())