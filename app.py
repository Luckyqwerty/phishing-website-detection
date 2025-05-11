import streamlit as st
import joblib
import re

# Load model and vectorizer once
@st.cache_resource
def load_artifacts():
    model = joblib.load("rf_model_compressed.pkl")
    vectorizer = joblib.load("tfidf_vectorizer.pkl")
    return model, vectorizer

model, vectorizer = load_artifacts()

# Preprocess input URL
def preprocess_url(url):
    url = url.lower()
    url = re.sub(r"https?://", "", url)
    url = re.sub(r"www\.", "", url)
    url = re.sub(r"[^a-zA-Z0-9]", " ", url)
    return url

# Predict URL class
def predict_url(url, model, vectorizer):
    processed = preprocess_url(url)
    features = vectorizer.transform([processed])
    prediction = model.predict(features)[0]
    confidence = max(model.predict_proba(features)[0])
    return prediction, confidence

# Streamlit UI
st.set_page_config(page_title="Phishing Website Detection", page_icon="🔗")
st.title("Phishing Website Detection")
st.markdown("Enter a URL to check whether it's **safe** or a **phishing site** using our trained ML model.")

url_input = st.text_input("Enter URL here:")

if st.button("Check"):
    if url_input:
        try:
            prediction, confidence = predict_url(url_input, model, vectorizer)
            if prediction == 1:
                st.error(f"Phishing Link Detected! (Confidence: {confidence:.2f})")
            else:
                st.success(f"This link appears safe. (Confidence: {confidence:.2f})")
        except Exception as e:
            st.error(f"Something went wrong during prediction: {e}")
    else:
        st.warning("Please enter a URL.")
