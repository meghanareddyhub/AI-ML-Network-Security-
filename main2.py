# app.py
import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from utils.feature_utils import extract_features, classify_attack

# Load the trained model
model = joblib.load("model/rf_model.pkl")

# App title and instructions
st.title("🔍 GuardURL - Smart Threat Detection Dashboard")

st.info("""
✅ Always validate inputs  
⚠️ Avoid suspicious characters in URLs  
🔒 Use HTTPS wherever possible
""")

# Function to check a single URL
def check_url(url):
    features = extract_features(url)
    prediction = model.predict([features])[0]
    confidence = model.predict_proba([features])[0][prediction] * 100
    attack_type = classify_attack(url)
    return prediction, confidence, attack_type

# Choose input mode
mode = st.radio("Choose Mode:", ["Single URL", "Upload File"])

if mode == "Single URL":
    url = st.text_input("Enter a URL to check:")
    if url:
        pred, conf, attack_type = check_url(url)
        st.markdown(f"### ✅ Result: {'🟢 Safe' if pred == 0 else '🔴 Malicious'}")
        st.markdown(f"**Confidence:** {conf:.2f}%")
        if pred == 1:
            st.markdown(f"**Attack Type:** {attack_type}")

else:
    uploaded_file = st.file_uploader("Upload a CSV with a 'url' column", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        results = []
        for url in df["url"]:
            pred, conf, attack_type = check_url(url)
            results.append({
                "URL": url,
                "Result": "Malicious" if pred else "Safe",
                "Confidence": f"{conf:.1f}%",
                "Attack Type": attack_type
            })

        result_df = pd.DataFrame(results)
        st.dataframe(result_df)

        # Pie chart visualization
        labels = ["Malicious", "Safe"]
        sizes = [sum(result_df["Result"] == "Malicious"), sum(result_df["Result"] == "Safe")]
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=["red", "green"], startangle=90)
        st.pyplot(fig)
