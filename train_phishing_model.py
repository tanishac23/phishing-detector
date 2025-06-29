import pandas as pd
import joblib
from url_feature_extractor import manual_feature_extraction
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load your dataset of real URLs
df = pd.read_csv("raw_urls.csv")  # This should have two columns: url, label

# Extract features using your 30-feature function
feature_data = []
labels = []

for index, row in df.iterrows():
    url = row['url']
    label = row['label']  # 1 for phishing, -1 for legitimate
    features = manual_feature_extraction(url)
    feature_data.append(features)
    labels.append(label)

# Create feature and label arrays
X = pd.DataFrame(feature_data)
y = pd.Series(labels)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Model trained with accuracy: {accuracy * 100:.2f}%")

# Save model
joblib.dump(model, "phishing_model.pkl")
print("🎯 Model saved as phishing_model.pkl")
