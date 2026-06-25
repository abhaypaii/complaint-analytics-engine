# streamlit_app.py

import streamlit as st
from sentence_transformers import SentenceTransformer

st.set_page_config(
    page_title="Abhay's Complaint Analytics App",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': 'A personal project by abhaypai@vt.edu',
    }
)

st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 100px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)

dashboard = st.Page(
    page = "pages/dashboard.py",
    title = "Executive Dashboard",
)


classifier = st.Page(
    page = "pages/classifier.py",
    title = "Complaint Classifier",
    default=True
)

findings = st.Page(
    page = "pages/findings.py",
    title = "Findings from the data",
)


report = st.Page(
    page = "pages/report_generator.py",
    title = "Report Generator"
)


st.markdown(
    """
    <style>
        .main-header {
            font-size:32px !important;
            font-weight:600;
            padding-bottom:10px;
            padding-top:5px;
            border-bottom: 1px solid #eee;
        }
    </style>
    """, unsafe_allow_html=True
)

st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)


pg=st.navigation(
    {
        'Classifier': [classifier],
        "Dashboard":[dashboard],
        'Policy Insights':[findings],
        'Automation':[report]
    })


pg.run()
