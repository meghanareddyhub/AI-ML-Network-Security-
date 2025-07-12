import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
from utils.feature_utils import extract_features
import os

# Load dataset
df = pd.read_csv("testurls.csv")  # Make sure this file has 'url' and 'label' columns

# Extract features and labels
X = [extract_features(url) for url in df["url"]]
y = df["label"].values

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y)

# Train the model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/rf_model.pkl")
print("✅ Model trained and saved to model/rf_model.pkl")
