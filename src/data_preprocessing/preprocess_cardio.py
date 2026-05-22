import pandas as pd
from src.feature_engineering.features import bmi_category, lifestyle_score


def preprocess_cardio(input_path, output_path):
    df = pd.read_csv(input_path)

    df["bp_category_encoded"] = df["bp_category_encoded"].map({
        "Normal": 1,
        "Elevated": 2,
        "Hypertension Stage 1": 3,
        "Hypertension Stage 2": 4
    })

    df["height"] = df["height"] / 100

    df.rename(columns={
        "alco": "alcohol",
        "smoke": "smoking",
        "bmi": "BMI",
        "gluc": "glucose",
        "active": "exercise"
    }, inplace=True)

    df["BMI_Category"] = df["BMI"].apply(bmi_category)

    df["lifestyle_score"] = df.apply(
        lambda row: lifestyle_score(
            row["exercise"],
            row["alcohol"],
            row["smoking"]
        ),
        axis=1
    )

    df_cleaned = df[[
        "age_years",
        "BMI",
        "BMI_Category",
        "smoking",
        "alcohol",
        "exercise",
        "lifestyle_score",
        "gender",
        "cholesterol",
        "glucose",
        "cardio",
        "bp_category_encoded",
        "ap_hi",
        "ap_lo"
    ]]

    df_cleaned.to_csv(output_path, index=False)
    print(f"Cardio data saved to {output_path}")


if __name__ == "__main__":
    preprocess_cardio(
        "data/raw/cardio_data_processed.csv",
        "data/processed/cardio_cleaned.csv"
    )