def bp_recommendation(bp_pred):

    reports = {

        0: {
            "risk_level": "Normal Blood Pressure",

            "summary":
                "Your blood pressure category appears to be within a normal range. "
                "Continue maintaining healthy habits to support long-term heart health.",

            "daily_schedule": [
                ("07:30 AM", "[EXERCISE]", "Morning walk – 20 minutes"),
                ("10:00 AM", "[HYDRATION]", "Drink 500ml of water"),
                ("01:00 PM", "[NUTRITION]", "Eat balanced meals with vegetables and lean protein"),
                ("06:00 PM", "[EXERCISE]", "Light stretching or physical activity"),
                ("09:00 PM", "[MONITORING]", "Log meals and daily activity")
            ],

            "weekly_reminders": [
                ("Wednesday", "[MONITORING]", "Check blood pressure once this week"),
                ("Friday", "[HEALTH]", "Review exercise consistency"),
                ("Sunday", "[NUTRITION]", "Prepare healthy meals for next week")
            ],

            "monthly_checkpoints": [
                "Review blood pressure trend",
                "Monitor BMI and physical activity goals",
                "Routine health checkup if needed"
            ],

            "tips": [
                "Maintain regular physical activity",
                "Continue balanced eating habits",
                "Limit excessive salt intake",
                "Stay hydrated throughout the day",
                "Maintain healthy sleep habits"
            ]
        },

        1: {
            "risk_level": "Elevated Blood Pressure",

            "summary":
                "Your blood pressure is slightly above the normal range. "
                "Lifestyle improvements are recommended to prevent progression into hypertension.",

            "daily_schedule": [
                ("07:00 AM", "[EXERCISE]", "Morning walk – 30 minutes"),
                ("10:00 AM", "[HYDRATION]", "Drink 500ml of water"),
                ("01:00 PM", "[NUTRITION]", "Choose lower-sodium meals"),
                ("03:00 PM", "[STRESS]", "Take a 5-minute breathing or relaxation break"),
                ("06:30 PM", "[EXERCISE]", "Evening light cardio – 20 minutes"),
                ("09:00 PM", "[MONITORING]", "Log meals, activity, and stress level")
            ],

            "weekly_reminders": [
                ("Monday", "[NUTRITION]", "Plan lower-sodium meals for the week"),
                ("Wednesday", "[MONITORING]", "Check blood pressure"),
                ("Friday", "[EXERCISE]", "Complete at least 4 workouts this week"),
                ("Sunday", "[HEALTH]", "Review sleep, stress, and activity habits")
            ],

            "monthly_checkpoints": [
                "Review blood pressure changes",
                "Monitor weight and BMI progress",
                "Schedule routine screening if blood pressure remains elevated"
            ],

            "tips": [
                "Reduce salty and processed foods",
                "Increase fruits, vegetables, and potassium-rich foods",
                "Exercise at least 4 times per week",
                "Manage stress with breathing or meditation",
                "Improve sleep consistency"
            ]
        },

        2: {
            "risk_level": "Hypertension Stage 1",

            "summary":
                "Your blood pressure category suggests Stage 1 hypertension. "
                "Consistent lifestyle changes and regular monitoring are recommended to reduce cardiovascular risk.",

            "daily_schedule": [
                ("07:00 AM", "[EXERCISE]", "Morning walk – 30 minutes"),
                ("10:00 AM", "[HYDRATION]", "Drink 500ml of water"),
                ("12:30 PM", "[NUTRITION]", "Eat a low-sodium, heart-healthy lunch"),
                ("03:00 PM", "[STRESS]", "Take a stress-management break"),
                ("06:00 PM", "[EXERCISE]", "Evening cardio – 25 minutes"),
                ("09:00 PM", "[MONITORING]", "Log blood pressure, meals, and exercise")
            ],

            "weekly_reminders": [
                ("Monday", "[MONITORING]", "Check blood pressure and body weight"),
                ("Wednesday", "[EXERCISE]", "Complete structured cardio session"),
                ("Friday", "[NUTRITION]", "Review sodium intake and food log"),
                ("Sunday", "[HEALTH]", "Review weekly BP trend and lifestyle progress")
            ],

            "monthly_checkpoints": [
                "Review blood pressure trend",
                "Assess BMI and exercise consistency",
                "Consider medical consultation if BP remains high"
            ],

            "tips": [
                "Reduce salt and processed foods",
                "Follow a heart-healthy diet",
                "Exercise consistently every week",
                "Limit caffeine if it affects your BP",
                "Monitor blood pressure regularly"
            ]
        },

        3: {
            "risk_level": "Hypertension Stage 2",

            "summary":
                "Your blood pressure category suggests Stage 2 hypertension. "
                "This may increase the risk of heart disease, stroke, and kidney problems. "
                "Stronger lifestyle changes and medical consultation are strongly recommended.",

            "daily_schedule": [
                ("07:00 AM", "[MONITORING]", "Check blood pressure in the morning"),
                ("07:30 AM", "[EXERCISE]", "Morning walk – 30 minutes"),
                ("10:00 AM", "[HYDRATION]", "Drink 500ml of water"),
                ("01:00 PM", "[NUTRITION]", "Eat a low-sodium, heart-healthy lunch"),
                ("06:00 PM", "[EXERCISE]", "Evening light cardio – 20 minutes"),
                ("09:00 PM", "[MONITORING]", "Log blood pressure, meals, symptoms, and exercise")
            ],

            "weekly_reminders": [
                ("Monday", "[MONITORING]", "Check blood pressure and body weight"),
                ("Wednesday", "[NUTRITION]", "Review sodium and processed food intake"),
                ("Friday", "[EXERCISE]", "Complete at least 5 exercise sessions this week"),
                ("Sunday", "[MEDICAL]", "Schedule doctor visit / blood pressure follow-up")
            ],

            "monthly_checkpoints": [
                "Blood pressure follow-up with healthcare provider",
                "Review cardiovascular risk factors",
                "Monitor BMI, exercise, and sodium reduction progress",
                "Discuss treatment plan with a healthcare professional if needed"
            ],

            "tips": [
                "Strongly reduce salt intake",
                "Avoid highly processed foods",
                "Exercise safely and consistently",
                "Manage stress and sleep quality",
                "Consult a healthcare provider for proper medical guidance"
            ]
        }
    }

    report = reports.get(int(bp_pred))

    return report