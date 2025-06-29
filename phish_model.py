# phish_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
data = pd.read_csv("phishing_site_data.csv")

# Drop the index column if it exists
if 'index' in data.columns:
    data = data.drop(['index'], axis=1)

# Split into features (X) and label (y)
X = data.drop('Result', axis=1)
y = data['Result']

# Split into train and test sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {acc * 100:.2f}%")

# Save the model
joblib.dump(model, "phishing_model.pkl")
