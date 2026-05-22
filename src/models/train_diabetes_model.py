import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report

from imblearn.over_sampling import SMOTE


def train_diabetes_model():
    df = pd.read_csv("data/processed/diabetes_cleaned.csv")

    X = df.drop("diabetes", axis=1)
    y = df["diabetes"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=42
    )

    smote = SMOTE(random_state=42)
    X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

    scaler = StandardScaler()

    cols_to_scale = [
        "age",
        "bmi",
        "HbA1c_level",
        "blood_glucose_level"
    ]

    X_train_res[cols_to_scale] = scaler.fit_transform(X_train_res[cols_to_scale])
    X_test[cols_to_scale] = scaler.transform(X_test[cols_to_scale])

    logistic_model = LogisticRegression(max_iter=1000, random_state=42)
    logistic_model.fit(X_train_res, y_train_res)

    lr_pred = logistic_model.predict(X_test)
    lr_proba = logistic_model.predict_proba(X_test)[:, 1]

    print("=== Logistic Regression ===")
    print("Accuracy:", accuracy_score(y_test, lr_pred))
    print("ROC-AUC:", roc_auc_score(y_test, lr_proba))
    print(classification_report(y_test, lr_pred))

    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train_res, y_train_res)

    rf_pred = rf_model.predict(X_test)
    rf_proba = rf_model.predict_proba(X_test)[:, 1]

    print("=== Random Forest ===")
    print("Accuracy:", accuracy_score(y_test, rf_pred))
    print("ROC-AUC:", roc_auc_score(y_test, rf_proba))
    print(classification_report(y_test, rf_pred))

    joblib.dump(logistic_model, "saved_models/diabetes_logistic_model.pkl")
    joblib.dump(rf_model, "saved_models/diabetes_random_forest_model.pkl")
    joblib.dump(scaler, "saved_models/diabetes_scaler.pkl")

    print("Diabetes models saved successfully.")


if __name__ == "__main__":
    train_diabetes_model()