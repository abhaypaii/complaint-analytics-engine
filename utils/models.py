import streamlit as st
import joblib

@st.cache_resource
def load_models():
    product_model = joblib.load("Models/product_classifier.joblib")
    issue_model = joblib.load("Models/issue_classifier.joblib")
    risk_model = joblib.load("Models/risk_model.joblib")
    tfidf = joblib.load("Models/text_tfidf_vectorizer.joblib")
    encoder_issue = joblib.load("Models/encoder_issue.joblib")
    encoder_product = joblib.load("Models/encoder_product.joblib")

    return product_model, issue_model, risk_model, tfidf, encoder_issue, encoder_product

product_model, issue_model, risk_model, tfidf, encoder_issue, encoder_product = load_models()
