# %%
import kagglehub
import pandas as pd
import os

# 1. download dataset
path = kagglehub.dataset_download("sahilislam007/health-and-lifestyle-dataset")

print("Path to dataset files:", path)

files = os.listdir(path)
print("Including files:", files)

# 3. read dataset
csv_path = os.path.join(path, files[0]) 
df = pd.read_csv(csv_path)

print(df.head())
# %%
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# %%
order = ['None', '1-2 times/week', '3-5 times/week', 'Daily']

sns.boxplot(data=df, x="Exercise_Freq", y="BMI", order=order, palette="Set2")
plt.title("Relationship between Exercise Frequency and BMI")
plt.show()

sns.violinplot(data=df, x="Exercise_Freq", y="BMI", order=order, inner="quart")
plt.show()

# %%
# how smoke is related to BMI
sns.boxplot(data = df, x = "Smoker", y = "BMI" )

# %%
cov_matrix = df.cov(numeric_only=True)

# The rest of your plotting code remains the same
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))
# Add numeric_only=True inside the corr() function
sns.heatmap(df.drop(columns=['ID']).corr(numeric_only=True), annot=True, fmt='.2f', cmap='coolwarm')
plt.title('Covariance Matrix Heatmap')
plt.show()
# %%
