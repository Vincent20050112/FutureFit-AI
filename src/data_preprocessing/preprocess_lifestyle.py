import pandas as pd
from src.feature_engineering.features import bmi_category, lifestyle_score


def preprocess_lifestyle(input_path, output_path):
    df = pd.read_csv(input_path)

    df["Height_m"] = df["Height_cm"] / 100

    df["Smoker"] = df["Smoker"].map({
        "No": 0,
        "Yes": 1
    })

    df["Exercise_Freq"] = df["Exercise_Freq"].map({
        "1-2 times/week": 1,
        "3-5 times/week": 2,
        "Daily": 3
    })

    df["Diet_Quality"] = df["Diet_Quality"].map({
        "Poor": 1,
        "Average": 2,
        "Good": 3,
        "Excellent": 4
    })

    df["Alcohol_Consumption"] = df["Alcohol_Consumption"].map({
        "Low": 1,
        "Moderate": 2,
        "High": 3
    })

    df["Chronic_Disease"] = df["Chronic_Disease"].map({
        "No": 0,
        "Yes": 1
    })

    df["Exercise_Freq"] = df["Exercise_Freq"].fillna(0)
    df["Alcohol_Consumption"] = df["Alcohol_Consumption"].fillna(0)

    df["lifestyle_score"] = df.apply(
        lambda row: lifestyle_score(
            row["Exercise_Freq"],
            row["Alcohol_Consumption"],
            row["Smoker"]
        ),
        axis=1
    )

    df["BMI_Category"] = df["BMI"].apply(bmi_category)

    df.rename(columns={"Height_m": "height"}, inplace=True)

    df_cleaned = df[[
        "Age",
        "BMI",
        "BMI_Category",
        "Smoker",
        "Alcohol_Consumption",
        "Exercise_Freq",
        "lifestyle_score",
        "Gender",
        "Diet_Quality",
        "Chronic_Disease",
        "Stress_Level",
        "Sleep_Hours"
    ]]

    df_cleaned.to_csv(output_path, index=False)
    print(f"Lifestyle data saved to {output_path}")


if __name__ == "__main__":
    preprocess_lifestyle(
        "data/raw/synthetic_health_lifestyle_dataset.csv",
        "data/processed/lifestyle_cleaned.csv"
    )