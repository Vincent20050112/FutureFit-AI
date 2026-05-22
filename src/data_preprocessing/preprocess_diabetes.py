import pandas as pd
from src.feature_engineering.features import bmi_category


def preprocess_diabetes(input_path, output_path):
    df = pd.read_csv(input_path)

    df = df.drop_duplicates()

    df["smoking_history"] = df["smoking_history"].replace(
        ["No Info", "unknown"], "Unknown"
    )

    for col in ["bmi", "HbA1c_level", "blood_glucose_level"]:
        mean = df[col].mean()
        std = df[col].std()

        lower_bound = mean - 3 * std
        upper_bound = mean + 3 * std

        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]

    df["BMI_Category"] = df["bmi"].apply(bmi_category)

    df = pd.get_dummies(
        df,
        columns=["gender", "smoking_history", "BMI_Category"],
        drop_first=False
    )

    df.to_csv(output_path, index=False)
    print(f"Diabetes data saved to {output_path}")


if __name__ == "__main__":
    preprocess_diabetes(
        "data/raw/diabetes_prediction_dataset.csv",
        "data/processed/diabetes_cleaned.csv"
    )