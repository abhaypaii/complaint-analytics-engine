import streamlit as st
import pandas as pd
from utils.data import load_complaint_data, load_company_data, load_trend_data, load_predicted_issue_data
import streamlit as st
import pandas as pd

#GenAI Libraries
from utils.context import get_company_context, get_prediction_context, get_trend_context
from utils.prompts import company_prompt, trend_prompt, prediction_prompt
from utils.gemini import generate_ai_report

df = load_complaint_data()
trends = load_trend_data()
companies = load_company_data()
pred = load_predicted_issue_data()

st.title('Inputs for policy formulation')

tab1, tab2, tab3 = st.tabs(['Emerging Trends', 'Institutions', 'Complaint Predictions'], default='Emerging Trends')

with tab1:
    @st.cache_data
    def report():
        context = get_trend_context(trends)

        prompt = trend_prompt(context)

        with st.spinner("Generating report..."):
            report = generate_ai_report(prompt)
        st.markdown(report)

    c1, c2 = st.columns([1,4])
    button1 = c1.button('Generate Report', key='tab1')
    c2.write('(The LLM Model may experience temporary periods of high demand, keep trying to generate periodically)')

    if button1:
        report()

with tab2:
    @st.cache_data
    def report():
        context = get_company_context(companies) 

        prompt = company_prompt(context)

        with st.spinner("Generating report..."):
            report = generate_ai_report(prompt)
        st.markdown(report)
    
    c1, c2 = st.columns([1,4])
    button2 = c1.button('Generate Report', key='tab2')
    c2.write('(The LLM Model may experience temporary periods of high demand, keep trying to generate periodically)')

    if button2:
        report()


with tab3:
    @st.cache_data
    def report():
        context = get_prediction_context(pred)

        prompt = prediction_prompt(context)

        with st.spinner("Generating report..."):
            report = generate_ai_report(prompt)
        st.markdown(report)
    
    c1, c2 = st.columns([1,4])
    button3 = c1.button('Generate Report', key='tab3')
    c2.write('(The LLM Model may experience temporary periods of high demand, keep trying to generate periodically)')

    if button3:
        report()