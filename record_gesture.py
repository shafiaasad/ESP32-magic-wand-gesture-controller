import asyncio
import websockets
import json
import csv
import time
import os

URI = "ws://192.168.0.11:8080/sensor/connect?type=android.sensor.accelerometer"

async def record_sample(label, sample_num):

    filename = f"data/{label}_{sample_num}.csv"

    async with websockets.connect(URI) as ws:

        with open(filename, "w", newline="") as f:

            writer = csv.writer(f)

            writer.writerow(
                ["timestamp_ns", "ax", "ay", "az", "label"]
            )

            start = time.time()

            while time.time() - start < 1:

                msg = json.loads(await ws.recv())

                ts = msg["timestamp"]
                ax, ay, az = msg["values"]

                writer.writerow(
                    [ts, ax, ay, az, label]
                )

async def main():

    os.makedirs("data", exist_ok=True)

    label = input("Gesture name: ")

    for i in range(1, 31):

        input(f"\nPress ENTER for sample {i}")

        print("Perform gesture NOW")

        await record_sample(label, i)

        print(f"Saved sample {i}")

asyncio.run(main())