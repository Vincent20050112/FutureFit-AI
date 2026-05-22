import streamlit as st
import joblib
import pandas as pd
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_DIR = BASE_DIR / "saved_models"

CSS_PATH = Path(__file__).parent / "styles.css"
st.markdown(f"<style>{CSS_PATH.read_text()}</style>", unsafe_allow_html=True)

st.set_page_config(
    page_title="FutureFit AI",
    page_icon="🩺",
    layout="centered"
)

st.title("🩺 FutureFit AI")
st.write("Enter your health details once and get predictions for multiple health risks.")


def set_bmi_category(input_data, bmi_value):
    if bmi_value < 18.5:
        col = "BMI_Category_Underweight"
    elif bmi_value < 25:
        col = "BMI_Category_Normal"
    elif bmi_value < 30:
        col = "BMI_Category_Overweight"
    else:
        col = "BMI_Category_Obese"

    if col in input_data.columns:
        input_data[col] = 1

    return input_data


def set_one_hot_column(input_data, column_name):
    if column_name in input_data.columns:
        input_data[column_name] = 1
    return input_data


with st.form("health_form"):
   with st.container(key="basic_info"):
    
        st.markdown('<p class="serif-italic">Basic Info</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=1, max_value=120, value=25)
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])


   
        st.markdown('<p class="serif-italic">Body Measurements</p>', unsafe_allow_html=True)
        col1, col2 = st.columns([3,2], vertical_alignment="bottom")
        with col1:
            st.write('Height')
            hcol1, hcol2 = st.columns(2)
        
            with hcol1:
                feet = st.number_input("ft", min_value=0, max_value=6, step=1, key="h_feet", value=5)
            with hcol2:
                inches = st.number_input("in", min_value=0, max_value=11, step=1, key="h_inches", value=5)
        with col2:
            st.write('Weight')
            weight = st.number_input("lbs", min_value = 0, max_value=1000, key="weight", value=120)
            
        # bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=24.0)

        st.markdown('<p class="serif-italic">Diabetes Indicator</p>', unsafe_allow_html=True)

        col1, col2 = st.columns([2,1])
        with col1:
            hbA1c = st.number_input("HbA1c Level", min_value=3.0, max_value=15.0, value=5.5)
        with col2:
            glucose = st.number_input("Blood Glucose Level", min_value=50, max_value=300, value=120)

        smoking_history = st.selectbox(
            "Smoking History",
            ["never", "former", "current", "not current", "ever", "Unknown"]
        )
    

        st.markdown('<p class="serif-italic">Lifestyle Habits</p>', unsafe_allow_html=True)
        
        smoking = st.segmented_control("Do you smoke?", ["Yes", "No"], selection_mode="single")
        alcohol = st.segmented_control("Do you consume alcohol?", ["Yes", "No"], selection_mode="single")
        exercise = st.segmented_control("Do you exercise?", ["Yes", "No"], selection_mode="single")
        
        
        smoking_binary = 1 if smoking == "Yes" else 0
        alcohol_binary = 1 if alcohol == "Yes" else 0
        exercise_binary = 1 if exercise == "Yes" else 0

        st.markdown('<p class="serif-italic">Blood Pressure</p>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            ap_hi = st.number_input("Systolic Blood Pressure", min_value=80, max_value=250, value=120)
        with col2:
            ap_lo = st.number_input("Diastolic Blood Pressure", min_value=40, max_value=150, value=80)

        submit = st.form_submit_button("Predict All Health Risks")
    
    # with st.container():
    #     st.markdown("""
    #         <div class="output-container">
    #             <h2>Prediction Results</h2>
    #             <div class="outputs">
    #                 <p>{diabetes_output}</p>
    #                 <p>{bp_output}</p>
    #                 <p>{cholesterol_output}</p>
    #                 <p>{cardio_output}</p>
    #                 <p>Lifestyle Score: 3{lifestyle_score}</p>
    #                 <p>{lifestyle_output}</p>
    #             </div>
    #         </div>
    #     """, unsafe_allow_html=True)


if submit:
    lifestyle_score = exercise_binary - alcohol_binary - smoking_binary
    
    height_inches = feet*12 + inches
    height_squared = height_inches ** 2
    bmi = (weight * 703) / height_squared
    
    # Diabetes Prediction
    diabetes_model = joblib.load(MODEL_DIR / "diabetes_random_forest_model.pkl")

    diabetes_input = pd.DataFrame(columns=diabetes_model.feature_names_in_)
    diabetes_input.loc[0] = 0

    diabetes_input["age"] = age
    diabetes_input["bmi"] = bmi
    diabetes_input["HbA1c_level"] = hbA1c
    diabetes_input["blood_glucose_level"] = glucose

    diabetes_input = set_bmi_category(diabetes_input, bmi)
    diabetes_input = set_one_hot_column(diabetes_input, f"gender_{gender}")
    diabetes_input = set_one_hot_column(diabetes_input, f"smoking_history_{smoking_history}")

    diabetes_prediction = diabetes_model.predict(diabetes_input)[0]

    
    if diabetes_prediction == 1:
        diabetes_output = "High"
    else:
        diabetes_output = "Low"

    # Blood Pressure Prediction
    bp_model = joblib.load(MODEL_DIR / "bp_model.pkl")

    bp_input = pd.DataFrame([{
        "age_years": age,
        "BMI": bmi,
        "smoking": smoking_binary,
        "alcohol": alcohol_binary,
        "exercise": exercise_binary,
        "lifestyle_score": lifestyle_score,
        "ap_hi": ap_hi,
        "ap_lo": ap_lo
    }])

    bp_prediction = bp_model.predict(bp_input)[0]

    
    if bp_prediction == 1:
        bp_output = "Normal"
    elif bp_prediction == 2:
        bp_output = "Elevated"
    elif bp_prediction == 3:
        bp_output = "Hypertension Stage 1"
    elif bp_prediction == 4:
        bp_output = "Hypertension Stage 2"

    # Cholesterol Prediction
    cholesterol_model = joblib.load(MODEL_DIR / "cholesterol_model.pkl")

    cholesterol_input = pd.DataFrame([{
        "age_years": age,
        "BMI": bmi,
        "smoking": smoking_binary,
        "alcohol": alcohol_binary,
        "exercise": exercise_binary,
        "lifestyle_score": lifestyle_score
    }])

    cholesterol_prediction = cholesterol_model.predict(cholesterol_input)[0]

    
    if cholesterol_prediction == 1:
        cholesterol_output = "Normal"
    elif cholesterol_prediction == 2:
        cholesterol_output = "Above Normal"
    elif cholesterol_prediction == 3:
        cholesterol_output = "Well Above Normal"

    # Cardiovascular Prediction
    cardio_model = joblib.load(MODEL_DIR / "cardio_model.pkl")

    cardio_input = pd.DataFrame([{
        "age_years": age,
        "BMI": bmi,
        "smoking": smoking_binary,
        "alcohol": alcohol_binary,
        "exercise": exercise_binary,
        "lifestyle_score": lifestyle_score
    }])

    cardio_prediction = cardio_model.predict(cardio_input)[0]

   
    if cardio_prediction == 1:
        cardio_output = "High"
    else:
        cardio_output = "Low"

    # Lifestyle Score
    

    if lifestyle_score >= 1:
        lifestyle_output = "Your lifestyle score looks good. Keep maintaining healthy habits."
    elif lifestyle_score == 0:
        lifestyle_output = "Try to improve consistency with exercise and reduce unhealthy habits."
    else:
        lifestyle_output = "Consider reducing smoking/alcohol and increasing physical activity."
        
    with st.container():
        st.markdown(f"""
            <div class="output-container">
                <div class="outputs">
                    <p class="serif-italic">Prediction Results</p>
                    <p>Diabetes Risk: <strong>{diabetes_output}</strong></p>
                    <p>Blood Pressure Category: <strong>{bp_output}</strong></p>
                    <p>Cholesterol Level: <strong>{cholesterol_output}</strong></p>
                    <p>Cardiovascular Risk: <strong>{cardio_output}</strong></p>
                    <p>Lifestyle Score: <strong>{lifestyle_score}</strong></p>
                    <p>Lifestyle Recommendation: <strong>{lifestyle_output}</strong></p>
                </div>
                <button id="add_to_cal">Add to Calendar</button>
            </div>
        """, unsafe_allow_html=True)