import streamlit as st
import pandas as pd

@st.cache_data
def load_company_data():
    return pd.read_csv("/Users/abhaypai/Library/Mobile Documents/com~apple~CloudDocs/Job stuff/Pre 2026/Projects/Portfolio Projects/RBI/Data/institutions.csv")

@st.cache_data
def load_trend_data():
    return pd.read_csv("/Users/abhaypai/Library/Mobile Documents/com~apple~CloudDocs/Job stuff/Pre 2026/Projects/Portfolio Projects/RBI/Data/emerging_trends.csv")

@st.cache_data
def load_complaint_data():
    return pd.read_csv('/Users/abhaypai/Library/Mobile Documents/com~apple~CloudDocs/Job stuff/Pre 2026/Projects/Portfolio Projects/RBI/Data/complaints_final.csv')

@st.cache_data
def load_predicted_issue_data():
    return pd.read_csv('/Users/abhaypai/Library/Mobile Documents/com~apple~CloudDocs/Job stuff/Pre 2026/Projects/Portfolio Projects/RBI/Data/issues_predicted.csv')

