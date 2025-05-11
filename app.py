import streamlit as st
import joblib
import re

# Load model and vectorizer
@st.cache_resource
def load_model():
    try:
        model = joblib.load("rf_model_compressed.pkl")
        vectorizer = joblib.load("tfidf_vectorizer.pkl")
        return model, vectorizer
    except Exception as e:
        st.error(f"Error loading model/vectorizer: {e}")
        raise e


# Preprocessing function
def preprocess_url(url):
    url = url.lower()
    url = re.sub(r"https?://", "", url)
    url = re.sub(r"www\.", "", url)
    url = re.sub(r"[^a-zA-Z0-9]", " ", url)
    return url

# Prediction function
def predict_url(url):
    processed = preprocess_url(url)
    features = vectorizer.transform([processed])
    prediction = model.predict(features)[0]
    probas = model.predict_proba(features)[0]
    confidence = max(probas)
    return prediction, confidence

# Streamlit UI
st.set_page_config(page_title="Phishing Website Detection", page_icon="🔗")
st.title("Phishing Website Detection")
st.markdown("Enter a URL below to check whether it is **safe** or a **phishing link** using our trained machine learning model.")

input_url = st.text_input("Enter URL here:")

if st.button("Check"):
    if input_url:
        prediction, confidence = predict_url(input_url)
        if prediction == 1:
            st.error(f"Phishing Link Detected! (Confidence: {confidence:.2f})")
        else:
            st.success(f"This link appears safe. (Confidence: {confidence:.2f})")
    else:
        st.warning("Please enter a URL.")
