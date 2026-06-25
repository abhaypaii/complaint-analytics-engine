import streamlit as st
from sentence_transformers import SentenceTransformer
from utils.models import load_models
from utils.data import load_company_data
from utils.data import load_trend_data
import pandas as pd
import plotly.express as px
import streamlit_shadcn_ui as ui

st.title('Complaint Classification Engine')
st.divider()

@st.cache_resource
def call_embedder():
    embedder = SentenceTransformer(
        "sentence-transformers/all-mpnet-base-v2"
    )
    return embedder

embedder = call_embedder()

models = load_models()
product_model = models[0]
issue_model = models[1]
encoder_product = models[5]
encoder_issue = models[4]
risk_model = models[2]

companies = load_company_data()
risk_df = pd.read_csv('Data/risk_distribution.csv')
c1, c2, c3 = st.columns([2,0.1,2])
cont = c1.container(border=True)
company = cont.selectbox('Company', options=companies['Company'], index=None)
complaint = cont.text_area('Enter complaint', placeholder='Please enter at least 5 words', height=150)
button = cont.button('Analyse')


def dist_chart(risk):
    fig = px.histogram(
                risk_df['Risk'],
                x='Risk',
                nbins=100,
            )
    
    fig.add_vline(x=risk,
              line_color='red',
              annotation_text=f'Risk: {risk}')

    fig.update_layout(
        plot_bgcolor='white',
        title={
            'text': "<b>Risk distribution</b><br><span style='color:#6A7383; font-size:12px;'>Overall breakdown of risk scores across 290k records</span>",
            'y': 0.93,
            'x': 0.05,
            'xanchor': 'left',
            'yanchor': 'top',
            'font': dict(family="Inter, Segoe UI, Arial", size=18, color='#1A1F36') # Stripe uses clean sans-serif
        },
        bargap=0.1, # The magic parameter: adds a subtle modern gap between bars
        
        # Clean up X-Axis
        xaxis=dict(
            title=None,
            showgrid=False, # Remove vertical gridlines entirely
            showticklabels=True,
            tickvals=[1,2.5,5],
            tickfont=dict(family="Arial", size=11, color='#4F566B'),
            linecolor='#E3E8EE', # Subtle bottom axis border
        ),
        
        # Clean up Y-Axis
        yaxis=dict(
            title=None,
            showgrid=False,
            showticklabels=False,
            gridcolor='#F7F8F9', # Ultra-faint horizontal gridlines
            zeroline=False
        ),
        
        margin=dict(l=60, r=40, t=80, b=60), # Generous padding
        width=900,
        height=450
    )

    return fig

def risk_metric(risk):
    if risk>4:
        text='Critical'
        color='red'

        return text, color
    
    elif risk>3:
        text='High'
        color='orange'

        return text, color
    
    elif risk>1.5:
        text='Medium'
        color='yellow'

        return text, color
    elif risk>=0:
        text='Low'
        color='grey'

        retunr text, color

valid=0
if button:
    if complaint.count(' ') >=4:
        if company:
            with c3:
                valid=1
                product = encoder_product.inverse_transform([product_model.predict([complaint])[0]])[0]
                issue = encoder_issue.inverse_transform([issue_model.predict([complaint])[0]])[0]
                st.metric('Product', product)
                st.metric('Issue', issue)

                X = embedder.encode([complaint])
                temp = risk_model.predict(X)
                risk = 0.7*temp[0,0] + 0.3*temp[0,1]
                text, color = risk_metric(risk)
                c3.metric(label='Risk', value = str(round(risk,1))+" out of 5", delta=text, delta_arrow='off', delta_color=color)
                st.divider()
                c3.plotly_chart(dist_chart(round(risk,1)), height=270)

                
        else:
            valid=0
            with c3:
                ui.alert(title="Select a company", description ="You need to add a company to analyse the complaint")
            
    else:
        with c3:
                ui.alert(title="Enter more words", description ="You need to enter at least 5 words to classify the complaint")

if valid:
    with c1.expander('Company Analytics for '+company, expanded=True):
        stats = companies[companies['Company']==company]
        c1, c2 = st.columns(2)
        c1.metric(label='Average Risk (out of 5)', value=round(stats['Avg_Risk'], 2))
        c1.metric(label='Average Handling (out of 5)', value=round(stats['Avg_Handling_Score'], 2))
        c2.metric(label='Timely Response (%)', value=round(stats['Timely_Response_Pct'], 2))
        c2.markdown('**Usual Response**')
        c2.write(stats['Typical_Response'].item())

