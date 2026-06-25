import streamlit as st
import joblib

@st.cache_resource
def load_models():
    product_model = joblib.load("/Users/abhaypai/Library/Mobile Documents/com~apple~CloudDocs/Job stuff/Pre 2026/Projects/Portfolio Projects/RBI/Models/product_classifier.joblib")
    issue_model = joblib.load("/Users/abhaypai/Library/Mobile Documents/com~apple~CloudDocs/Job stuff/Pre 2026/Projects/Portfolio Projects/RBI/Models/issue_classifier.joblib")
    risk_model = joblib.load("/Users/abhaypai/Library/Mobile Documents/com~apple~CloudDocs/Job stuff/Pre 2026/Projects/Portfolio Projects/RBI/Models/risk_model.joblib")
    tfidf = joblib.load("/Users/abhaypai/Library/Mobile Documents/com~apple~CloudDocs/Job stuff/Pre 2026/Projects/Portfolio Projects/RBI/Models/text_tfidf_vectorizer.joblib")
    encoder_issue = joblib.load("/Users/abhaypai/Library/Mobile Documents/com~apple~CloudDocs/Job stuff/Pre 2026/Projects/Portfolio Projects/RBI/Models/encoder_issue.joblib")
    encoder_product = joblib.load("/Users/abhaypai/Library/Mobile Documents/com~apple~CloudDocs/Job stuff/Pre 2026/Projects/Portfolio Projects/RBI/Models/encoder_product.joblib")

    return product_model, issue_model, risk_model, tfidf, encoder_issue, encoder_product

product_model, issue_model, risk_model, tfidf, encoder_issue, encoder_product = load_models()