#General Libraries
import streamlit as st
import pandas as pd
from utils.data import load_complaint_data, load_company_data, load_trend_data, load_predicted_issue_data
import streamlit_shadcn_ui as ui
import plotly.graph_objects as go
import plotly.express as px
import datetime
import streamlit as st

#GenAI Libraries
from utils.context import get_company_context, get_prediction_context, get_trend_context
from utils.prompts import company_prompt, trend_prompt, prediction_prompt
from utils.gemini import generate_ai_report

df = load_complaint_data()
trends = load_trend_data()
companies = load_company_data()
pred = load_predicted_issue_data()
risk_df = pd.read_csv('Data/risk_distribution.csv')


hc1, hc2=st.columns([1,1])
hc1.title('Executive Dashboard')


#KPIs

c1, c2, c3, c4 = st.columns(4)

with c1:
    ui.metric_card(title='High Risk Complaints', 
                content=len(risk_df[risk_df['Risk']>=3]), 
                description=str(round(len(risk_df[risk_df['Risk']>=3])/len(risk_df)*100, 2))+"% of total ("+str(len(risk_df))+")")
with c2:
    ui.metric_card(title='Average Risk Score', \
            content=round(risk_df['Risk'].mean(), 2), 
            description='out of 5')
    
with c3:
    ui.metric_card('Average Handling Score',
                content=round(companies['Avg_Handling_Score'].mean(), 2),
                description='out of 5')    

with c4:
    ui.metric_card('Firms of high concern',
                content=len(companies[companies['Cluster']==3]),
                description=f'{round(len(companies[companies['Cluster']==3])/len(companies)*100,2)}% of 3699 firms')    

with st.sidebar:
    c1, c2=st.columns(2)
    start = c1.date_input("Start Date",datetime.date(2015, 7, 1))
    end = c2.date_input("End Date", datetime.date(2018, 5, 31))

df = df[
    (pd.to_datetime(df["Date"]) >= pd.to_datetime(start)) &
    (pd.to_datetime(df["Date"]) <= pd.to_datetime(end))
]

state_counts = (
    df.groupby("State")
    .size()
    .reset_index(name="Complaints")
    )

#Row 1
c1, c2, c3 = st.columns([1,1.4, 1])
with c1:
    st.subheader('Monthly Complaints')
    df["Date"] = pd.to_datetime(df["Date"])

    complaints_by_date = (
        df.groupby(pd.Grouper(key="Date", freq="MS"))
        .size()
        .reset_index(name="Complaint_Count")
    )

    complaints_by_date.columns = ["Date", "Complaint_Count"]
    fig = px.line(complaints_by_date,
                x='Date', 
                y='Complaint_Count',
                line_shape='spline')
    fig.update_yaxes(range=[3000,None],
                    showgrid=False, title=None)
    fig.update_xaxes(title=None)
    fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0))
    fig.update_traces(
        line_shape='spline',
        fill="tozeroy",
        fillgradient=dict(
            type="vertical",
            colorscale=[
                [0.00, "rgba(59,130,246,0.00)"],  # bottom
                [0.15, "rgba(59,130,246,0.05)"],
                [0.30, "rgba(59,130,246,0.15)"],
                [0.60, "rgba(59,130,246,0.35)"],
                [1.00, "rgba(59,130,246,0.80)"]   # near line
            ]
        ),
        line=dict(color="rgb(59,130,246)", width=3)
    )
    fig.add_vline(
        x=pd.to_datetime("2017-09"),
        line_width=2,
        line_color="crimson",
        opacity=0.6,
        annotation_text='Equifax <br>Data Breach',
        annotation_position='bottom right'
    )

    fig.add_vline(
        x=pd.to_datetime("2017-01"),
        line_width=2,
        line_color="crimson",
        opacity=0.6,
        annotation_text='CFPB sues Navient',
        annotation_position='bottom left'
    )
    
    st.plotly_chart(fig, height=150)

with c2:
    sc1, sc2=st.columns([1.8,1])
    sc1.subheader('   '+'Complaint by states')
    
    fig = px.choropleth(
    state_counts,
    locations="State",
    locationmode="USA-states",
    color="Complaints",
    scope="usa",
    color_continuous_scale="Blues",
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0)
    )
    fig.update_layout(
    map_style="carto-positron",
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor="white",
    coloraxis_showscale=False,
    height=350,
)

    fig.update_traces(
        marker=dict(
            opacity=1,
            line=dict(color="grey", width=1)
        )
    )
    st.plotly_chart(fig, height=130)

    sc2.write('')
    with sc2.popover(label='List'):
        with st.container(height=190):
            ui.table(data=state_counts.sort_values(by='Complaints', ascending=False), maxHeight=50)

with c3:
    sc1, sc2 =st.columns([5,1])
    sc1.subheader('Emerging Trends')
    with sc2.popover(label='',icon='ℹ'):
        st.write('These are the top 4 trends as calculated by a weighted score of Risk(0.4) and Emergence(0.6)')
    top = trends.nlargest(20, "PriorityScore").iloc[[0,1,3,13]]

    plot_df = top.melt(

        id_vars=[
            "Phrase",
            "AverageRisk",
            "ComplaintCount",
            "PriorityScore"
        ],

        value_vars=["2016","2017","2018"],

        var_name="Year",

        value_name="TFIDF"

    )
    fig = px.line(

        plot_df,

        x="Year",

        y="TFIDF",

        color="Phrase",

        markers=True,

        line_shape='spline',

        hover_data=[
            "AverageRisk",
            "ComplaintCount",
            "PriorityScore"
        ]

    )
    fig.update_layout(showlegend=False)
    fig.update_xaxes(tickvals=[2016, 2017, 2018], title=None)
    fig.update_yaxes(
        title=None,
        showticklabels=False,
        showgrid=False,
        tickvals=[0.76,0.9,1.0]
    )

    for phrase in plot_df["Phrase"].unique():

        d = plot_df[plot_df["Phrase"] == phrase]

        fig.add_annotation(
            x=d["Year"].iloc[-1],
            y=d["TFIDF"].iloc[-1],
            text=phrase,
            showarrow=False,
            xanchor="left",
            xshift=8,
            font=dict(size=11)
        )
    fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0))

    st.plotly_chart(fig, height=150)

c1, spacer, c2, c3 = st.columns([0.84,0.1,1,1])

with c1:
    st.subheader('Product Distribution')

    product_dist = (
        df["Product"]
        .value_counts(normalize=True)
        .mul(100)
    )

    colors = [
        "#1D4ED8",
        "#2563EB",
        "#3B82F6",
        "#60A5FA",
        "#93C5FD",
        "#BFDBFE",
        "#DBEAFE",
    ]

    fig = go.Figure()

    for i, (product, pct) in enumerate(product_dist.items()):
        fig.add_trace(
            go.Bar(
                x=[pct],
                y=[""],
                name=product,
                orientation="h",
                marker=dict(color=colors[i % len(colors)]),
                text=f"{pct:.0f}%",
                textposition="inside",
                insidetextanchor="middle",
                hovertemplate=f"<b>{product}</b><br>{pct:.1f}%<extra></extra>",
            )
        )

    fig.update_layout(
        barmode="stack",
        height=90,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(
            visible=False,
            range=[0, 100],
            fixedrange=True,
        ),
        yaxis=dict(
            visible=False,
            fixedrange=True,
        ),
        legend=dict(
            orientation="h",
            y=-0.4,
            x=0,
            font=dict(size=11),
        ),
    )

    st.plotly_chart(fig, use_container_width=True, height=200)

with c2:
    sc1, sc2 = st.columns([1.8,1])
    sc1.subheader('Firm Risk Matrix')
    plot_df = pd.read_csv('Data/institution_anomalies.csv')
    # Convert to categorical
    plot_df["Cluster"] = plot_df["Cluster"].astype(str)
    sc2.write('')
    with sc2.popover(label='At-Risk Firms'):
        data = plot_df[plot_df['Avg_Risk']<=plot_df["Avg_Risk"].mean()]
        data = data[data['Avg_Response_Score']<=plot_df["Avg_Response_Score"].mean()].iloc[:,1:]
        st.dataframe(data)

    fig = px.scatter(
        plot_df,
        x="Avg_Response_Score",
        y="Avg_Risk",
        hover_name="Company",
        hover_data=[
            "Complaint_Count",
            "Avg_Handling_Score",
            "Timely_Response_Pct"
        ],
        labels={
            "Avg_Risk": "Average Risk Score",
            "Avg_Response_Score": "Average Response Score",
        }
    )
    
    fig.update_layout(
        margin=dict(l=10, r=0, t=0, b=0)
    )

    fig.update_traces(
        marker=dict(
            size=11,
            line=dict(width=1, color="white"),
            opacity=0.85
        )
    )

    fig.update_xaxes(tickvals=[1,2,3,4,5])
    fig.update_yaxes(tickvals=[1,2,3,4,5])


    # Optional: add average reference lines
    fig.add_vline(
        x=plot_df["Avg_Response_Score"].mean(),
        line_dash="dash",
        line_color="gray",
        opacity=0.7
    )

    fig.add_hline(
        y=plot_df["Avg_Risk"].mean(),
        line_dash="dash",
        line_color="gray",
        opacity=0.7
    )
    fig.update_yaxes(showgrid=False)

    x_avg = plot_df["Avg_Response_Score"].mean()
    y_avg = plot_df["Avg_Risk"].mean()

    fig.add_annotation(
        x=x_avg * 0.5,
        y=y_avg * 1.85,
        text="<b>Needs<br>Supervision</b>",
        showarrow=False,
        bgcolor="rgba(255,245,245,0.95)",
        bordercolor="crimson",
        borderwidth=1,
        font=dict(size=9, color="crimson")
    )

    fig.add_annotation(
        x=x_avg * 2.2,
        y=y_avg * 0.30,
        text="<b>Best<br>Performers</b>",
        showarrow=False,
        bgcolor="rgba(240,255,240,0.95)",
        bordercolor="forestgreen",
        borderwidth=0,
        font=dict(size=9, color="forestgreen")
    )


    fig.update_layout(
        template="plotly_white",
        height=600,
        legend_title="Institution Cluster"
    )

    st.plotly_chart(fig, use_container_width=True, height=240)

with c3:
    st.subheader('Expected Change (Monthly)')
    
    plot_df = pred.sort_values("Delta", ascending=False).head(4)

    fig = go.Figure()

    # 2018 complaints (blue)
    fig.add_bar(
        x=plot_df["Issue_Category"],
        y=plot_df["2018"],
        name="2018 Complaints"
    )

    # Predicted increase (red)
    fig.add_bar(
        x=plot_df["Issue_Category"],
        y=plot_df["Delta"]/12,
        name="Predicted Increase",
        text=[
                f"{cat}<br>{pct:+.1f}%"
                for cat, pct in zip(plot_df["Issue_Category"], plot_df["Change_Pct"])
            ],
            textposition="outside",
            textfont=dict(size=14),
            cliponaxis=True
    )

    fig.update_layout(
        barmode="stack",
        template="plotly_white",
        xaxis_title="Issue",
        yaxis_title="Complaints",
        xaxis_tickangle=-35,
        showlegend=True,
        height=220
    )

    fig.update_xaxes(showticklabels=False, showgrid=False, title=None)
    fig.update_yaxes(showgrid=False, title=None)
    fig.update_layout(
        bargap=0.26,
        barcornerradius=4
        )

    fig.update_layout(
            legend=dict(
                x=0.98,
                y=0.98,
                xanchor="right",
                yanchor="top",
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="lightgray",
                borderwidth=1
            )
        )


    fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0))

    st.plotly_chart(fig, use_container_width=True)
