import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv("features.csv")

train_rows = []
test_rows = []

for _, row in df.iterrows():

    filename = row["filename"]

    trial_num = int(
        filename.split("_")[-1]
        .replace(".csv", "")
    )

    if trial_num <= 21:
        train_rows.append(row)
    else:
        test_rows.append(row)

train_df = pd.DataFrame(train_rows)
test_df = pd.DataFrame(test_rows)

X_train = train_df.drop(
    columns=["filename", "label"]
)

y_train = train_df["label"]

X_test = test_df.drop(
    columns=["filename", "label"]
)

y_test = test_df["label"]

print("\nTraining Samples:", len(X_train))
print("Testing Samples:", len(X_test))

# ==========================
# KNN
# ==========================

knn = KNeighborsClassifier(n_neighbors=3)

knn.fit(X_train, y_train)

knn_pred = knn.predict(X_test)

print("\n===== KNN =====")

print(
    "Accuracy:",
    accuracy_score(y_test, knn_pred)
)

print(
    confusion_matrix(y_test, knn_pred)
)

print(
    classification_report(
        y_test,
        knn_pred
    )
)

# ==========================
# Random Forest
# ==========================

rf = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

rf.fit(X_train, y_train)

rf_pred = rf.predict(X_test)

print("\n===== RANDOM FOREST =====")

print(
    "Accuracy:",
    accuracy_score(y_test, rf_pred)
)

print(
    confusion_matrix(y_test, rf_pred)
)

print(
    classification_report(
        y_test,
        rf_pred
    )
)

joblib.dump(
    knn,
    "knn_model.pkl"
)

joblib.dump(
    rf,
    "rf_model.pkl"
)

print("\nModels saved successfully.")