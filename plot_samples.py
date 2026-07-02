import pandas as pd
import matplotlib.pyplot as plt

files = [
    "data/rest_1.csv",
    "data/rotate_1.csv",
    "data/doubletap_1.csv",
    "data/figure8_1.csv",
    "data/lightningbolt_1.csv"
]

for file in files:

    df = pd.read_csv(file)

    plt.figure(figsize=(10,4))

    plt.plot(df["ax"], label="ax")
    plt.plot(df["ay"], label="ay")
    plt.plot(df["az"], label="az")

    plt.title(file)
    plt.xlabel("Frame")
    plt.ylabel("Acceleration (m/s²)")
    plt.legend()

    plt.show()