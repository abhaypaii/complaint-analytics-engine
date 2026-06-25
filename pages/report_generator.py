from utils.parser import parse_file
from utils.prompts import report_prompt
from utils.gemini import generate_ai_report
from utils.pdf import create_pdf
import streamlit as st

st.title('Report Generator')

uploaded = st.file_uploader(

    "Upload Report",

    type=["csv", "xlsx", "docx", "pdf"]

)

if uploaded:

    text = parse_file(uploaded)

    if st.button("Generate Report"):

        prompt = report_prompt(text)

        with st.spinner("Generating..."):

            report = generate_ai_report(prompt)
        
        pdf = create_pdf(report)

        c1, c2 = st.columns([1,4])

        c1.download_button(
            label="📄 Download PDF",
            data=pdf,
            file_name="RBI_Policy_Report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
        st.markdown(report)