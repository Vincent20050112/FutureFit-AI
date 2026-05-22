GLUCOSE_DIABETES = 126
GLUCOSE_PREDIABETES = 100
HBA1C_DIABETES = 6.5
HBA1C_PREDIABETES = 5.7
BMI_OBESE = 30
BMI_OVERWEIGHT = 25

def get_risk_level(glucose, hba1c, bmi, age=35, hypertension=False, smoking=False):
    score = 0

    # Glucose scoring
    if glucose >= GLUCOSE_DIABETES:       # ≥126 — diabetic range
        score += 3
    elif glucose >= GLUCOSE_PREDIABETES:  # 100–125 — prediabetes range
        score += 1.5

    # HbA1c scoring
    if hba1c >= HBA1C_DIABETES:           # ≥6.5 — diabetic range
        score += 3
    elif hba1c >= HBA1C_PREDIABETES:      # 5.7–6.4 — prediabetes range
        score += 1.5

    # BMI scoring
    if bmi >= BMI_OBESE:
        score += 2
    elif bmi >= BMI_OVERWEIGHT:
        score += 1

    # Additional risk factors
    if age >= 45:
      score += 1
    if hypertension:
      score += 1
    if smoking:
      score += 0.5

    if score >= 5:
      return "high"
    elif score >= 2:
      return "moderate"
    else:
      return "low"
  
RECOMMENDATIONS = {
    "high": {
        "label": "Diabetes Risk: High",
        "summary": "Your indicators suggest elevated diabetes risk. Immediate lifestyle changes are strongly advised.",
        "daily": [
            ("07:00 AM", "Morning walk – 30 minutes", "exercise"),
            ("10:00 AM", "Water reminder – drink 500ml", "hydration"),
            ("01:30 PM", "10-min post-lunch walk", "exercise"),
            ("03:00 PM", "Water reminder – drink 500ml", "hydration"),
            ("06:00 PM", "Evening workout – 20 min light cardio", "exercise"),
            ("09:00 PM", "Log today's meals and blood sugar reading", "monitoring"),
        ],
        "weekly": [
            ("Wednesday", "Mid-week glucose check + log results", "monitoring"),
            ("Friday", "Check blood sugar after fasting (morning)", "monitoring"),
            ("Saturday", "Review weekly food log – identify sugar spikes", "monitoring"),
            ("Sunday", "Schedule doctor visit / blood work reminder", "medical"),
        ],
        "monthly": [
            "HbA1c lab test – schedule with physician",
            "Review BMI progress and adjust goals",
            "Consult nutritionist for personalized meal plan",
        ],
        "tips": [
            "Swap sugary drinks for water or unsweetened tea",
            "Replace white carbs with whole grains (brown rice, quinoa)",
            "Eat smaller portions 5–6 times/day instead of 3 large meals",
            "Avoid eating 3 hours before bed",
            "Track your food intake with a free app like MyFitnessPal",
        ],
    },

    "moderate": {
        "label": "Diabetes Risk: Moderate",
        "summary": "Some indicators are in a pre-diabetes range. Proactive habits now can prevent progression.",
        "daily": [
            ("07:30 AM", "Morning walk or light jog – 20 minutes", "exercise"),
            ("03:00 PM", "Water reminder – drink 500ml", "hydration"),
            ("06:00 PM", "Evening activity – 15 min walk/stretching", "exercise"),
            ("09:00 PM", "Log daily meals and note energy levels", "monitoring"),
        ],
        "weekly": [
            ("Friday", "Weekly weigh-in and BMI check", "monitoring"),
            ("Sunday", "Plan next week's exercise schedule", "exercise"),
        ],
        "monthly": [
            "Check fasting blood glucose levels",
            "Assess lifestyle changes – what's working?",
        ],
        "tips": [
            "Reduce refined sugar gradually – don't go cold turkey",
            "Add 10-minute walks after each meal",
            "Eat more fiber: beans, lentils, vegetables",
            "Limit alcohol – it can spike blood sugar",
            "Get 7–8 hours of sleep; poor sleep worsens insulin sensitivity",
        ],
    },

    "low": {
        "label": "Diabetes Risk: Low",
        "summary": "Your diabetes risk is low. Keep up your healthy habits and monitor occasionally.",
        "daily": [
            ("07:00 AM", "Any physical activity – 20–30 minutes", "exercise"),
        ],
        "weekly": [
            ("Wednesday", "Physical activity check – hit 150 min/week?", "exercise"),
        ],
        "monthly": [
            "Annual blood glucose screening (if over 40)",
            "Maintain healthy weight – monitor BMI quarterly",
        ],
        "tips": [
            "Continue regular exercise – it's your best prevention tool",
            "Maintain your current healthy eating patterns",
            "Monitor blood sugar occasionally, especially if family history exists",
            "Stay up to date with annual health checkups",
            "Manage stress – chronic stress can raise blood sugar over time",
        ],
    },
}

def get_diabetes_report(name, glucose, hba1c, bmi, age=35, hypertension=False, smoking=False):
    risk = get_risk_level(glucose, hba1c, bmi, age, hypertension, smoking)
    recs = RECOMMENDATIONS[risk]

    glucose_flag = "Diabetes" if glucose >= GLUCOSE_DIABETES else (
        "Prediabetes" if glucose >= GLUCOSE_PREDIABETES else "Normal"
    )
    hba1c_flag = "Diabetes" if hba1c >= HBA1C_DIABETES else (
        "Prediabetes" if hba1c >= HBA1C_PREDIABETES else "Normal"
    )
    bmi_flag = "Obese" if bmi >= BMI_OBESE else (
        "Overweight" if bmi >= BMI_OVERWEIGHT else "Normal"
    )

    return {
        "name": name,
        "risk": risk,
        "label": recs["label"],
        "summary": recs["summary"],
        "indicators": {
            "Blood Glucose": f"{glucose} mg/dL → {glucose_flag}",
            "HbA1c": f"{hba1c}% → {hba1c_flag}",
            "BMI": f"{bmi} → {bmi_flag}",
            "Age": age,
            "Hypertension": "Yes" if hypertension else "No",
            "Smoking": "Yes" if smoking else "No",
        },
        "daily": recs["daily"],
        "weekly": recs["weekly"],
        "monthly": recs["monthly"],
        "tips": recs["tips"],
    }