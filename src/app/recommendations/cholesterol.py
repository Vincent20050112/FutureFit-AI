def cholesterol_recommendation(chol_pred):

    reports = {

        0: {
            "risk_level": "Cholesterol Level: Healthy",
            "summary":
                "Your cholesterol indicators appear to be within a healthy range. "
                "Continue maintaining a balanced lifestyle and healthy eating habits.",

            "daily_schedule": [
                ("07:30 AM", "[EXERCISE]", "Morning walk – 20 minutes"),
                ("10:00 AM", "[HYDRATION]", "Drink 500ml of water"),
                ("01:00 PM", "[NUTRITION]", "Balanced lunch with vegetables and lean protein"),
                ("06:00 PM", "[EXERCISE]", "Light physical activity or stretching"),
                ("09:00 PM", "[MONITORING]", "Log meals and daily activity")
            ],

            "weekly_reminders": [
                ("Wednesday", "[MONITORING]", "Track body weight and activity progress"),
                ("Friday", "[NUTRITION]", "Review weekly eating habits"),
                ("Sunday", "[HEALTH]", "Prepare healthy meals for next week")
            ],

            "monthly_checkpoints": [
                "Review exercise consistency",
                "Monitor body weight and BMI",
                "Routine health checkup if needed"
            ],

            "tips": [
                "Continue eating fruits and vegetables",
                "Maintain regular physical activity",
                "Limit excessive fast food consumption",
                "Stay hydrated throughout the day",
                "Maintain a healthy sleep schedule"
            ]
        },



        1: {
            "risk_level": "Cholesterol Risk: Moderate",
            "summary":
                "Your cholesterol indicators suggest mildly elevated cholesterol levels. "
                "Lifestyle improvements are recommended to reduce future cardiovascular risk.",

            "daily_schedule": [
                ("07:00 AM", "[EXERCISE]", "Morning walk – 30 minutes"),
                ("10:00 AM", "[HYDRATION]", "Drink 500ml of water"),
                ("12:30 PM", "[NUTRITION]", "Choose low-fat and high-fiber lunch"),
                ("03:00 PM", "[HYDRATION]", "Water reminder – avoid sugary drinks"),
                ("06:30 PM", "[EXERCISE]", "Evening cardio – 20 minutes"),
                ("09:00 PM", "[MONITORING]", "Track meals and exercise")
            ],

            "weekly_reminders": [
                ("Monday", "[NUTRITION]", "Plan healthier meals for the week"),
                ("Wednesday", "[MONITORING]", "Check body weight"),
                ("Friday", "[EXERCISE]", "Complete at least 4 workouts this week"),
                ("Sunday", "[HEALTH]", "Review weekly eating habits")
            ],

            "monthly_checkpoints": [
                "Review cholesterol management progress",
                "Monitor BMI and weight changes",
                "Schedule routine health screening if needed"
            ],

            "tips": [
                "Reduce fried and oily foods",
                "Increase vegetables and fiber intake",
                "Choose grilled food over fried food",
                "Exercise at least 4 times per week",
                "Reduce sugary beverages and snacks"
            ]
        },



        2: {
            "risk_level": "Cholesterol Risk: High",
            "summary":
                "Your indicators suggest high cholesterol levels, which may increase the risk "
                "of heart disease and cardiovascular complications. Immediate lifestyle changes "
                "and medical monitoring are strongly recommended.",

            "daily_schedule": [
                ("07:00 AM", "[EXERCISE]", "Morning walk – 30 minutes"),
                ("10:00 AM", "[HYDRATION]", "Drink 500ml of water"),
                ("01:00 PM", "[NUTRITION]", "Eat high-fiber, low-fat lunch"),
                ("03:00 PM", "[HYDRATION]", "Avoid sugary drinks and processed snacks"),
                ("06:00 PM", "[EXERCISE]", "Evening workout – 30 min light cardio"),
                ("09:00 PM", "[MONITORING]", "Log meals, exercise, and symptoms")
            ],

            "weekly_reminders": [
                ("Tuesday", "[MONITORING]", "Track blood pressure and body weight"),
                ("Thursday", "[EXERCISE]", "Complete at least 5 exercise sessions this week"),
                ("Saturday", "[NUTRITION]", "Review food log and reduce saturated fats"),
                ("Sunday", "[MEDICAL]", "Schedule lipid profile test / doctor reminder")
            ],

            "monthly_checkpoints": [
                "Lipid profile blood test",
                "Review BMI and cardiovascular health progress",
                "Consult healthcare provider if cholesterol remains high"
            ],

            "tips": [
                "Avoid fried and processed foods",
                "Increase vegetables, oats, and whole grains",
                "Exercise consistently every week",
                "Reduce saturated fats and sugary drinks",
                "Avoid smoking and excessive alcohol consumption"
            ]
        }
    }


    report = reports.get(chol_pred)
    return report