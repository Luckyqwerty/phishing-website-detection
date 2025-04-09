import streamlit as st
import pandas as pd
import tldextract
import re
import pickle
import joblib  
import pickle
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from flask import Flask, request, jsonify  # <-- NEW
import threading  

# Load models
with open("xgb_model.pkl", "rb") as f:
    xgb_model = pickle.load(f)

# Load compressed Random Forest model
rf_model = joblib.load("rf_model_compressed.pkl")

# Load TF-IDF vectorizer
with open("tfidf_vectorizer.pkl", "rb") as f:
    tfidf = pickle.load(f)


# URL preprocessing function
def preprocess_url(url):
    ext = tldextract.extract(url)
    domain = ext.domain + '.' + ext.suffix
    path = url.split(domain, 1)[-1] if domain in url else ''
    return domain + path

def clean_url(url):
    url = re.sub(r'https?://', '', url)
    url = re.sub(r'www\.', '', url)
    return preprocess_url(url)

# Prediction function using ensemble
def predict_url(url):
    cleaned = clean_url(url)
    vectorized = tfidf.transform([cleaned])
    
    xgb_pred = xgb_model.predict(vectorized)[0]
    rf_pred = rf_model.predict(vectorized)[0]
    
    # Voting mechanism
    final_pred = 1 if (xgb_pred + rf_pred) >= 1 else 0
    return final_pred

# Streamlit UI
st.title("Phishing Website Detection")
st.markdown("Enter a URL to check if it's **phishing** or **legitimate**.")

user_input = st.text_input("Enter URL:", "")

if st.button("Check"):
    if user_input.strip() == "":
        st.warning("Please enter a valid URL.")
    else:
        result = predict_url(user_input)
        if result == 1:
            st.error("Phishing Website Detected!")
        else:
            st.success("Legitimate Website.")


# ===== (1) Flask API Setup =====
flask_app = Flask(__name__)

@flask_app.route('/api/detect', methods=['POST'])
def api_detect():
    data = request.get_json()
    url = data.get('url', '')
    
    # Reuse your existing prediction logic
    is_phishing = predict(url)  # Call your predict() function from model.py
    return jsonify({'is_phishing': bool(is_phishing)})

def run_flask():
    flask_app.run(port=8502)  # Different port than Streamlit

# Start Flask in background
threading.Thread(target=run_flask, daemon=True).start()

# ===== (2) Your Existing Streamlit UI ===== 
# ... (keep all your existing Streamlit code below) ...
