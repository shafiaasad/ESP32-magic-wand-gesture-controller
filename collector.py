import asyncio
import websockets
import json
import csv
import time
import os

URI = "ws://192.168.0.11:8080/sensor/connect?type=android.sensor.accelerometer"

async def record_sample(label, sample_num):
    os.makedirs("data", exist_ok=True)
    filename = f"data/{label}_{sample_num}.csv"

    async with websockets.connect(URI) as ws:
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp_ns", "ax", "ay", "az", "label"])

            frames = []
            prev_ts = None

            while len(frames) < 50:
                msg = json.loads(await ws.recv())
                ts = msg["timestamp"]
                ax, ay, az = msg["values"]

                # Check for packet loss — discard window if gap > 25ms
                if prev_ts is not None:
                    gap_ms = (ts - prev_ts) / 1_000_000
                    if gap_ms > 25:
                        print(f"  [!] Packet loss detected ({gap_ms:.1f}ms gap) — restarting window")
                        frames = []
                        prev_ts = None
                        continue

                prev_ts = ts
                frames.append([ts, ax, ay, az, label])

            for row in frames:
                writer.writerow(row)

    print(f"  Saved {filename}")

async def main():
    label = input("Enter gesture name: ")
    for i in range(1, 31):
        input(f"\nPress ENTER for sample {i}/{30}")
        print("  Perform gesture NOW...")
        await record_sample(label, i)

asyncio.run(main())