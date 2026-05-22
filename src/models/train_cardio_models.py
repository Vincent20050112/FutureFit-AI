import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from src.models.evaluate import evaluate_model


def train_cardio_models():
    df = pd.read_csv("data/processed/cardio_cleaned.csv")

    X = df[[
        "age_years",
        "BMI",
        "smoking",
        "alcohol",
        "exercise",
        "lifestyle_score"
    ]]

    X_bp = df[[
        "age_years",
        "BMI",
        "smoking",
        "alcohol",
        "exercise",
        "lifestyle_score",
        "ap_hi",
        "ap_lo"
    ]]

    y_bp = df["bp_category_encoded"]
    y_chol = df["cholesterol"]
    y_cardio = df["cardio"]

    X_train, X_test, y_chol_train, y_chol_test, y_cardio_train, y_cardio_test = train_test_split(
        X,
        y_chol,
        y_cardio,
        test_size=0.2,
        random_state=42
    )

    X_bp_train, X_bp_test, y_bp_train, y_bp_test = train_test_split(
        X_bp,
        y_bp,
        test_size=0.2,
        random_state=42
    )

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    X_bp_train_scaled = scaler.fit_transform(X_bp_train)
    X_bp_test_scaled = scaler.transform(X_bp_test)

    bp_model = LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)
    bp_model.fit(X_bp_train_scaled, y_bp_train)
    bp_pred = bp_model.predict(X_bp_test_scaled)

    print("=== Blood Pressure Model ===")
    evaluate_model(y_bp_test, bp_pred)

    cholesterol_model = RandomForestClassifier(
        n_estimators=100,
        class_weight="balanced",
        random_state=42
    )
    cholesterol_model.fit(X_train, y_chol_train)
    chol_pred = cholesterol_model.predict(X_test)

    print("=== Cholesterol Model ===")
    evaluate_model(y_chol_test, chol_pred)

    cardio_model = RandomForestClassifier(
        n_estimators=100,
        class_weight="balanced",
        random_state=42
    )
    cardio_model.fit(X_train, y_cardio_train)
    cardio_pred = cardio_model.predict(X_test)

    print("=== Cardiovascular Disease Model ===")
    evaluate_model(y_cardio_test, cardio_pred)

    joblib.dump(bp_model, "saved_models/bp_model.pkl")
    joblib.dump(cholesterol_model, "saved_models/cholesterol_model.pkl")
    joblib.dump(cardio_model, "saved_models/cardio_model.pkl")
    joblib.dump(scaler, "saved_models/cardio_scaler.pkl")

    print("Cardio models saved successfully.")


if __name__ == "__main__":
    train_cardio_models()