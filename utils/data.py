import streamlit as st
import pandas as pd

@st.cache_data
def load_company_data():
    return pd.read_csv("Data/institutions.csv")

@st.cache_data
def load_trend_data():
    return pd.read_csv("Data/emerging_trends.csv")

@st.cache_data
def load_complaint_data():
    return pd.read_csv('Data/complaints_final.csv')

@st.cache_data
def load_predicted_issue_data():
    return pd.read_csv('Data/issues_predicted.csv')

