
# 🛡️ Phishing Website Detection

A Streamlit web app that detects whether a URL is **phishing** or **legitimate** using a trained machine learning model (XGBoost).

## 🚀 Features
- Real-time URL input and classification
- Extracts features like IP presence, URL length, special characters, etc.
- Uses XGBoost for high accuracy

## 🧠 Model Used
- **XGBoost** trained on a phishing dataset
- Exported as `best_phishing_model.pkl`

## 📦 Requirements

Install dependencies with:
```bash
pip install -r requirements.txt
