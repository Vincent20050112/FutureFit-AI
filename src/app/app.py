import streamlit as st
import joblib
import pandas as pd
from pathlib import Path
import time
from io import BytesIO
import sys

from recommendations.diabetes import get_diabetes_report

from recommendations.cardio import cardio_recommendation
from recommendations.bp import bp_recommendation
from recommendations.cholesterol import cholesterol_recommendation

# Automatically add the root directory (FutureFit-AI) to Python's search path
sys.path.append(str(Path(__file__).resolve().parents[2]))
from interface_downloadable_cal.build_ics import build_ics

st.set_page_config(
    page_title="FutureFit AI",
    page_icon="🩺",
    layout="centered"
)

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_DIR = BASE_DIR / "saved_models"

CSS_PATH = Path(__file__).parent / "styles.css"
st.markdown(f"<style>{CSS_PATH.read_text()}</style>", unsafe_allow_html=True)


col1, col2 = st.columns([2, 1])

with col1:

    st.title("FutureFit AI")

    st.markdown(
        '''
        <div class="tagline">
            Helping you stay <strong class="mytext"> one step ahead </strong> of your health.
        </div>
        ''',
        unsafe_allow_html=True
    )

    st.write(
        "Enter your health details once and get predictions for multiple health risks."
    )
    
    

with col2:
    st.image("src/run.jpeg", use_container_width=True)

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

results_placeholder = st.empty()
with st.form("health_form"):
   with st.container(key="basic_info"):
        with st.container(border=True, key="basic_card"):
            st.markdown('<p class="serif-italic">1. Basic Info</p>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                age = st.number_input("Age", min_value=1, max_value=120, value=25)
            with col2:
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])


        with st.container(border=True, key="body_card"):
            st.markdown('<p class="serif-italic">2. Body Measurements</p>', unsafe_allow_html=True)
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

        with st.container(border=True, key="blood_card"):
            st.markdown('<p class="serif-italic">3. Diabetes Indicator</p>', unsafe_allow_html=True)

            col1, col2 = st.columns([2,1])
            with col1:
                hbA1c = st.number_input("HbA1c Level", min_value=3.0, max_value=15.0, value=5.5)
            with col2:
                glucose = st.number_input("Blood Glucose Level", min_value=50, max_value=300, value=120)

            smoking_history = st.selectbox(
                "Smoking History",
                ["Never", "Former", "Current", "Not Current", "Ever", "Unknown"]
            )
        
        with st.container(border=True, key="lifestyle_card"):
            st.markdown('<p class="serif-italic">4. Lifestyle Habits</p>', unsafe_allow_html=True)
            
            smoking = st.segmented_control("Do you smoke?", ["Yes", "No"], selection_mode="single", key="form_smoke")
            alcohol = st.segmented_control("Do you consume alcohol?", ["Yes", "No"], selection_mode="single", key="form_alcohol")
            exercise = st.segmented_control("Do you exercise?", ["Yes", "No"], selection_mode="single", key="form_exercise")
            
            
            smoking_binary = 1 if smoking == "Yes" else 0
            alcohol_binary = 1 if alcohol == "Yes" else 0
            exercise_binary = 1 if exercise == "Yes" else 0
            
        with st.container(border=True, key="bp_card"):
            st.markdown('<p class="serif-italic">5. Blood Pressure</p>', unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                ap_hi = st.number_input("Systolic Blood Pressure", min_value=80, max_value=250, value=120)
            with col2:
                ap_lo = st.number_input("Diastolic Blood Pressure", min_value=40, max_value=150, value=80)

        submit = st.form_submit_button("Predict All Health Risks")
    
        # with st.container():
        #     st.markdown("""
        #         <div class="output-container">
        #             <p class="serif-italic pred">Prediction Summary</p>
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

if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False
if submit:
    st.session_state.form_submitted = True

if st.session_state.form_submitted:
    with st.spinner("Analyzing your health profile..."):
        time.sleep(1.2)
        
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
    
    
    st.title("Health Report and Recommendations")
    
    with st.container():
        st.markdown(f"""
            <div class="output-container">
                <div class="outputs">
                    <p class="serif-italic">Result Summary</p>
                    <p>Diabetes Risk: <strong>{diabetes_output}</strong></p>
                    <p>Blood Pressure Category: <strong>{bp_output}</strong></p>
                    <p>Cholesterol Level: <strong>{cholesterol_output}</strong></p>
                    <p>Cardiovascular Risk: <strong>{cardio_output}</strong></p>
                    <p>Lifestyle Score: <strong>{lifestyle_score}</strong></p>
                    <p>Lifestyle Recommendation: <strong>{lifestyle_output}</strong></p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    cardio_recs = cardio_recommendation(cardio_prediction)
    cholesterol_recs = cholesterol_recommendation(cholesterol_prediction)
    bp_recs = bp_recommendation(bp_prediction-1)
    diabetes_recs = get_diabetes_report(
        name="User",
        glucose=glucose,
        hba1c=hbA1c,
        bmi=bmi,
        age=age,
        hypertension=(bp_output == "Normal"),
        smoking=smoking == "Yes"
    )
    
    # -------------------------------------------------------------------------
    # MASTER CALENDAR SETUP: Initialize master schedule bucket in session state
    # -------------------------------------------------------------------------
    st.session_state.custom_schedule = []

    st.write("---")
    st.subheader("📅 Customize & Export Your Master Schedule")
    
    # Render layout configuration bar for the calendar download options
    col_tz, col_tip = st.columns([1, 2])
    with col_tz:
        user_tz = st.selectbox("Select Your Timezone", ["US/Pacific", "US/Eastern", "Europe/London", "Asia/Shanghai"])
    with col_tip:
        st.caption("💡 **How it works:** Uncheck any individual task inside the cards below if you want to skip it. Then click the master export button at the bottom of the page to download your custom calendar!")

    # =========================================================================
    # 1. DIABETES RECOMMENDATIONS SECTION
    # =========================================================================
    st.markdown(f"""
    <div class="result-card">
        <h2>{diabetes_recs["label"]}</h2>
        <p>{diabetes_recs["summary"]}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")

    with col1:
        with st.container(border=True):
            st.subheader("Daily Schedule")
            # Loop through diabetes tasks and generate an interactive checkbox for each item
            for i, (time_str, task, category) in enumerate(diabetes_recs["daily"]):
                is_checked = st.checkbox(
                    f"**{time_str}** [{category.upper()}] — {task}", 
                    value=True, 
                    key=f"chk_dia_{i}"
                )
                # Flatten structure and add to the master container if user checked it
                if is_checked:
                    st.session_state.custom_schedule.append((time_str, category.upper(), task))
            
    with col2:
        with st.container(border=True):
            st.subheader("Personalized Health Tips")
            for tip in diabetes_recs["tips"]:
                st.write(f"- {tip}")

    # =========================================================================
    # 2. CARDIOVASCULAR RECOMMENDATIONS SECTION
    # =========================================================================
    st.markdown(f"""
    <div class="output-card">
        <h2>{cardio_recs["risk_level"]}</h2>
        <p>{cardio_recs["summary"]}</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        with st.container(border=True):
            st.subheader("Daily Schedule")
            # Loop through cardiovascular tasks and generate an interactive checkbox for each item
            for i, (time_str, category, task) in enumerate(cardio_recs["daily_schedule"]):
                is_checked = st.checkbox(
                    f"**{time_str}** {category} — {task}", 
                    value=True, 
                    key=f"chk_cardio_{i}"
                )
                if is_checked:
                    st.session_state.custom_schedule.append((time_str, category, task))

    with col2:
        with st.container(border=True):
            st.subheader("Personalized Health Tips")
            for tip in cardio_recs["tips"]:
                st.write(f"- {tip}")
    
    # =========================================================================
    # 3. CHOLESTEROL RECOMMENDATIONS SECTION
    # =========================================================================
    st.markdown(f"""
    <div class="output-card">
        <h2>{cholesterol_recs["risk_level"]}</h2>
        <p>{cholesterol_recs["summary"]}</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        with st.container(border=True):
            st.subheader("Daily Schedule")
            # Loop through cholesterol tasks and generate an interactive checkbox for each item
            for i, (time_str, category, task) in enumerate(cholesterol_recs["daily_schedule"]):
                is_checked = st.checkbox(
                    f"**{time_str}** {category} — {task}", 
                    value=True, 
                    key=f"chk_chol_{i}"
                )
                if is_checked:
                    st.session_state.custom_schedule.append((time_str, category, task))

    with col2:
        with st.container(border=True):
            st.subheader("Personalized Health Tips")
            for tip in cholesterol_recs["tips"]:
                st.write(f"- {tip}")
    
    # =========================================================================
    # 4. BLOOD PRESSURE RECOMMENDATIONS SECTION
    # =========================================================================
    st.markdown(f"""
    <div class="output-card">
        <h2>{bp_recs["risk_level"]}</h2>
        <p>{bp_recs["summary"]}</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        with st.container(border=True):
            st.subheader("Daily Schedule")
            # Loop through blood pressure tasks and generate an interactive checkbox for each item
            for i, (time_str, category, task) in enumerate(bp_recs["daily_schedule"]):
                is_checked = st.checkbox(
                    f"**{time_str}** {category} — {task}", 
                    value=True, 
                    key=f"chk_bp_{i}"
                )
                if is_checked:
                    st.session_state.custom_schedule.append((time_str, category, task))

    with col2:
        with st.container(border=True):
            st.subheader("Personalized Health Tips")
            for tip in bp_recs["tips"]:
                st.write(f"- {tip}")

    # =========================================================================
    # MASTER DOWNLOAD GENERATOR: Final action button to export checked elements
    # =========================================================================
    st.write("---")
    
    # Using an empty placeholder container to dynamically render the master button
    download_placeholder = st.container()
    
    if st.session_state.custom_schedule:
        final_ics_bytes = build_ics(st.session_state.custom_schedule, timezone_str=user_tz)
        
        # Render the button inside the placeholder container
        download_placeholder.download_button(
            label=f"⚡ Download My Custom Schedule ({len(st.session_state.custom_schedule)} Tasks)",
            data=BytesIO(final_ics_bytes),
            file_name="my_custom_health_schedule.ics",
            mime="text/calendar",
            key="final_master_download_btn",
            use_container_width=True
        )
    else:
        download_placeholder.warning("⚠️ You have unchecked all tasks! Please check at least one task to export your calendar.")