def cardio_recommendation(cardio_pred):

    reports = {

        0: {
            "risk_level": "Cardiovascular Risk: Low",

            "summary":
                "Your indicators suggest a lower likelihood of cardiovascular disease. "
                "Maintaining healthy lifestyle habits is important for long-term heart health.",

            "daily_schedule": [
                ("07:30 AM", "[EXERCISE]", "Morning walk – 20 minutes"),
                ("10:00 AM", "[HYDRATION]", "Drink 500ml of water"),
                ("01:00 PM", "[NUTRITION]", "Eat balanced meals with vegetables and lean protein"),
                ("06:00 PM", "[EXERCISE]", "Light stretching or physical activity"),
                ("09:00 PM", "[MONITORING]", "Log daily meals and exercise")
            ],

            "weekly_reminders": [
                ("Wednesday", "[MONITORING]", "Track body weight and activity progress"),
                ("Friday", "[HEALTH]", "Review exercise consistency"),
                ("Sunday", "[NUTRITION]", "Prepare healthy meals for next week")
            ],

            "monthly_checkpoints": [
                "Monitor blood pressure regularly",
                "Review BMI and physical activity goals",
                "Routine health checkup if needed"
            ],

            "tips": [
                "Maintain regular physical activity",
                "Continue balanced eating habits",
                "Stay hydrated throughout the day",
                "Limit excessive fast food intake",
                "Maintain healthy sleep habits"
            ]
        },



        1: {
            "risk_level": "Cardiovascular Risk: High",

            "summary":
                "Your indicators suggest an elevated risk of cardiovascular disease. "
                "Lifestyle changes, regular monitoring, and medical consultation are strongly recommended "
                "to reduce future heart-related complications.",

            "daily_schedule": [
                ("07:00 AM", "[EXERCISE]", "Morning walk – 30 minutes"),
                ("10:00 AM", "[HYDRATION]", "Drink 500ml of water"),
                ("01:00 PM", "[NUTRITION]", "Choose low-salt and heart-healthy meals"),
                ("03:00 PM", "[MONITORING]", "Check stress level and avoid prolonged sitting"),
                ("06:00 PM", "[EXERCISE]", "Evening light cardio – 20 minutes"),
                ("09:00 PM", "[MONITORING]", "Log blood pressure, meals, and exercise")
            ],

            "weekly_reminders": [
                ("Monday", "[MONITORING]", "Check blood pressure and body weight"),
                ("Wednesday", "[EXERCISE]", "Complete at least 4 exercise sessions this week"),
                ("Friday", "[NUTRITION]", "Review sodium and fat intake"),
                ("Sunday", "[MEDICAL]", "Schedule doctor visit / cardiovascular screening")
            ],

            "monthly_checkpoints": [
                "Blood pressure monitoring",
                "Cardiovascular health assessment",
                "Review BMI and exercise consistency",
                "Consult healthcare provider if symptoms worsen"
            ],

            "tips": [
                "Reduce salt and saturated fat intake",
                "Exercise consistently every week",
                "Manage stress through relaxation techniques",
                "Avoid smoking and excessive alcohol",
                "Monitor blood pressure regularly"
            ]
        }
    }


    report = reports.get(cardio_pred)
    return report