Gesture Recognizer Magic Wand

A real-time hand-gesture recognition system built with an ESP32 microcontroller and an MPU6050 accelerometer, paired with a Python machine learning pipeline for data collection, feature engineering, model training, and live inference.

The wand recognizes five distinct gestures:


Rest
Clockwise Rotation
Double Tap
Figure-8
Lightning Bolt



Overview
The ESP32 reads raw accelerometer data from the MPU6050 over I2C at 50 Hz, converts it to m/s², and streams it as JSON frames over a WebSocket connection. On the Python side, this stream is segmented into 1-second windows (50 frames), summarized into statistical/signal-based features, and fed into a trained classifier for gesture prediction — either during offline training or live in real time.


System Components

Hardware
ComponentPurposeESP32Microcontroller — reads sensor data & hosts WebSocket serverMPU60503-axis accelerometer (I2C) for motion sensingWi-Fi networkTransport for streaming sensor data to the host PC


How It Works — Pipeline Steps


Sensor Integration — MPU6050 is interfaced with the ESP32 via I2C.
Wireless Streaming — ESP32 broadcasts accelerometer readings over Wi-Fi via WebSocket (port 8080).
Dataset Collection — 30 samples × 5 gestures = 150 labeled samples, each a 1-second (50-frame) window, saved as CSV.
Visualization — Each gesture's raw signal is plotted to inspect distinguishing motion patterns.
Feature Extraction — Each sample is reduced to 17 features (mean, std, min, max, energy per axis + SMA).
Model Training — KNN and Random Forest classifiers are trained on a trial-based split (samples 1–21 = train, 22–30 = test) and evaluated.
Model Evaluation — Confusion matrices, precision, recall, and F1-scores are generated.
Live Prediction — A sliding window over the live sensor stream feeds the trained Random Forest model for real-time gesture classification, reporting prediction, confidence, and inference latency.



Getting Started

1. Flash the ESP32


Open the ESP32 firmware in the Arduino IDE (or PlatformIO).
Update WIFI_SSID and WIFI_PASSWORD with your network credentials.
Wire the MPU6050 to the ESP32 (SDA → GPIO 21, SCL → GPIO 22).
Upload the sketch and note the IP address printed in Serial Monitor.


2. Set Up the Python Environment

bashpip install websockets pandas numpy matplotlib scikit-learn joblib

3. Update the WebSocket URI

In each Python script, replace the URI variable with your ESP32's IP address:

pythonURI = "ws://<ESP32_IP>:8080/sensor/connect?type=android.sensor.accelerometer"

4. Collect Data

bashpython collect_dataset.py

Follow the prompts to record 30 samples for each gesture label.

5. Visualize Samples (optional)

bashpython plot_samples.py

6. Extract Features

bashpython extract_features.py

Produces features.csv (150 rows × 18 columns).

7. Train Models

bashpython train_models.py

Saves knn_model.pkl and rf_model.pkl.

8. Plot Confusion Matrix (optional)

bashpython plot_confusion_matrix.py

9. Run Live Prediction

bashpython live_prediction.py


Results

ModelAccuracyKNN (k=3)88.9%Random Forest100%

Random Forest was selected for live prediction due to superior generalization and its ability to model non-linear decision boundaries between gesture classes.
