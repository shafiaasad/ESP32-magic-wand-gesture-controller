import pandas as pd
import numpy as np
import glob
import os

rows = []

for file in glob.glob("data/*.csv"):

    df = pd.read_csv(file)

    ax = df["ax"]
    ay = df["ay"]
    az = df["az"]

    label = df["label"].iloc[0]

    features = {

        # Needed for trial-based splitting later
        "filename": os.path.basename(file),

        # X-axis
        "ax_mean": ax.mean(),
        "ax_std": ax.std(),
        "ax_min": ax.min(),
        "ax_max": ax.max(),

        # Y-axis
        "ay_mean": ay.mean(),
        "ay_std": ay.std(),
        "ay_min": ay.min(),
        "ay_max": ay.max(),

        # Z-axis
        "az_mean": az.mean(),
        "az_std": az.std(),
        "az_min": az.min(),
        "az_max": az.max(),

        # Energy
        "ax_energy": np.sum(ax**2),
        "ay_energy": np.sum(ay**2),
        "az_energy": np.sum(az**2),

        # SMA (Signal Magnitude Area)
        "sma": (ax.abs() + ay.abs() + az.abs()).mean(),

        "label": label
    }

    rows.append(features)

feature_df = pd.DataFrame(rows)

feature_df.to_csv("features.csv", index=False)

print("Features extracted successfully.")
print("Shape:", feature_df.shape)
print(feature_df.head())