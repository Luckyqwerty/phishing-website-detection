import streamlit as st
import joblib
import pandas as pd
import re

# Load the trained model
model = joblib.load('best_phishing_model.pkl')

# Feature extraction from URL
def extract_features(url):
    return {
        'url_length': len(url),
        'has_ip': 1 if re.search(r'\d{1,3}(\.\d{1,3}){3}', url) else 0,
        'count_dots': url.count('.'),
        'count_hyphens': url.count('-'),
        'count_at': url.count('@'),
        'has_https': 1 if 'https' in url else 0,
        'has_http': 1 if 'http' in url else 0,
        'count_www': url.count('www'),
        'count_digits': sum(c.isdigit() for c in url),
        'count_special': sum(not c.isalnum() for c in url),
    }

# Streamlit Interface
st.set_page_config(page_title="Phishing URL Detector")
st.title("🔍 Phishing Website Detection")
st.markdown("Enter a URL to check whether it's **Phishing** or **Legitimate**.")

url = st.text_input("🔗 URL")

if st.button("🚀 Predict"):
    if url:
        features = pd.DataFrame([extract_features(url)])
        prediction = model.predict(features)[0]
        result = "⚠️ Phishing" if prediction == 1 else "✅ Legitimate"
        st.subheader(f"Result: {result}")
    else:
        st.warning("Please enter a valid URL.")
