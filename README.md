# 🩺 FutureFit AI

FutureFit AI is a machine learning health prediction system that uses user health data to predict:

- Diabetes Risk  
- Blood Pressure Risk  
- Cholesterol Risk  
- Cardiovascular Risk  
- Lifestyle Score  


Step 1: install requirements 
pip install -r requirements.txt

Step 2: Preprocess all datasets
python3 -m src.data_preprocessing.preprocess_diabetes
python3 -m src.data_preprocessing.preprocess_cardio
python3 -m src.data_preprocessing.preprocess_lifestyle

Step 3: Train models 
python3 -m src.models.train_diabetes_model
python3 -m src.models.train_cardio_models

Step 4: launch app 
streamlit run src/app/app.py