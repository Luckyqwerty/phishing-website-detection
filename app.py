import streamlit as st
import joblib
import re
import tldextract

st.title("🔐 Phishing Website Detection")
st.markdown("Enter a website URL to check if it's **legit or phishing**")

# Load the improved model
model = joblib.load('improved_model.pkl')

# Feature extraction
def has_ip(url): return 1 if re.search(r'\d{1,3}(\.\d{1,3}){3}', url) else 0
def count_special_chars(url): return sum(not c.isalnum() and c not in ['.', ':', '/'] for c in url)
def uses_shortener(url): return 1 if re.search(r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|tinyurl", url) else 0
def suspicious_keywords(url): 
    return sum(1 for word in ['login','account','secure','ebayisapi','verify','bank'] if word in url.lower())
def extract_features(url):
    ext = tldextract.extract(url)
    return [
        len(url),
        has_ip(url),
        count_special_chars(url),
        sum(c.isdigit() for c in url),
        1 if url.startswith("https") else 0,
        uses_shortener(url),
        suspicious_keywords(url),
        len(ext.subdomain.split('.')) if ext.subdomain else 0
    ]

# Streamlit Input
url_input = st.text_input("Enter URL:")

if url_input:
    features = extract_features(url_input)
    prediction = model.predict([features])[0]
    
    if prediction == 0:
        st.success("✅ Legitimate Website")
    else:
        st.error("🚨 Phishing Website Detected")
