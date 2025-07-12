import streamlit as st
import pandas as pd
import joblib
from utils.feature_utils import extract_features, classify_attack
import matplotlib.pyplot as plt

st.set_page_config(page_title="Attack Detection", layout="centered")
st.title("🛡️ SQLi & XSS Attack Detection Dashboard")

st.info("""
✅ Always validate inputs  
⚠️ Avoid suspicious characters in URLs  
🔒 Use HTTPS wherever possible
""")

# Load model
model = joblib.load("model/rf_model.pkl")

# Choose Mode
option = st.radio("Choose Mode:", ("Upload URLs", "Enter Single URL"))

# For file upload
if option == "Upload URLs":
    uploaded_file = st.file_uploader("Upload CSV with column 'url'", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        results = []

        for url in df["url"]:
            features = extract_features(url)
            pred = model.predict([features])[0]
            prob = model.predict_proba([features])[0][pred] * 100
            attack_type = classify_attack(url)
            results.append({
                "URL": url,
                "Result": "🔴 Malicious" if pred else "🟢 Safe",
                "Confidence": f"{prob:.1f}%",
                "Type": attack_type
            })

            result_df = pd.DataFrame(results)

        # Show table and pie chart side by side
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("### 📋 Detection Results")
            st.dataframe(result_df)

        with col2:
            st.markdown("### 📊 Threat Distribution")
            labels = ['Malicious', 'Safe']
            values = [sum(result_df['Result'] == "🔴 Malicious"), sum(result_df['Result'] == "🟢 Safe")]
            fig, ax = plt.subplots()
            ax.pie(values, labels=labels, autopct='%1.1f%%', colors=['red', 'green'], startangle=90)
            ax.axis("equal")
            st.pyplot(fig)


# For single URL
else:
    url = st.text_input("Enter a URL:")
    if url:
        features = extract_features(url)
        pred = model.predict([features])[0]
        prob = model.predict_proba([features])[0][pred] * 100
        attack_type = classify_attack(url)

        result = "🔴 Malicious" if pred else "🟢 Safe"
        st.markdown(f"### Prediction: {result}")
        st.markdown(f"**Confidence:** {prob:.2f}%")
        st.markdown(f"**Attack Type:** {attack_type}") # what is the errors
        