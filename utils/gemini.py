import streamlit as st
from google import genai

@st.cache_resource
def get_client():

    return genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"]
    )


def generate_ai_report(prompt):

    client = get_client()

    response = client.models.generate_content(

        model="gemini-3.1-flash-lite",

        contents=prompt,

    )

    return response.text

#gemini-2.5-flash
#gemini-2.5-flash-lite
#gemini-2.0-flash