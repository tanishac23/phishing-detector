import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
from url_feature_extractor import manual_feature_extraction

# Load the raw URLs dataset
try:
    df = pd.read_csv("raw_urls.csv")
except FileNotFoundError:
    print("❌ raw_urls.csv file not found!")
    exit()

# Extract features and labels
X = []
y = []

for i, row in df.iterrows():
    url = row['url']
    label = row['label']
    features = manual_feature_extraction(url)
    if features and len(features) == 30:
        X.append(features)
        y.append(label)
    else:
        print(f"⚠️ Skipped: {url} due to feature extraction failure.")

# Train/Test Split
if not X or not y:
    print("❌ No data to train the model.")
    exit()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Save model
joblib.dump(model, "phishing_model.pkl")
print(f"✅ Model trained successfully with accuracy: {accuracy * 100:.2f}%")
print("📦 Saved as phishing_model.pkl")
