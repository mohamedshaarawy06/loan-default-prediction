import streamlit as st
import pandas as pd
import plotly.express as px
import base64


@st.cache_data
def load_data():
    return pd.read_csv('credit_risk_clean.csv')


df = load_data()

with open('images/insights.jpg', 'rb') as f:
    insights_image = base64.b64encode(f.read()).decode()

st.markdown(f'''
<div class="hero" style="padding: 50px; background-image: linear-gradient(90deg, rgba(11,37,69,0.95), rgba(11,37,69,0.4)),
     url(data:image/jpg;base64,{insights_image});">
    <span class="badge">INSIGHTS</span>
    <h1>What Drives Loan Default?</h1>
    <p>Key findings from more than 32,000 real loans.</p>
</div>
''', unsafe_allow_html=True)


def style_chart(fig, x_title):
    fig.update_traces(marker_color='#13315C', textposition='outside', textfont_color='#0B2545', cliponaxis=False)
    fig.update_layout(height=340, xaxis_title=x_title, yaxis_title='Failure to Pay Rate', yaxis_tickformat='.0%', bargap=0.15,
                      margin=dict(t=50, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig


st.markdown('<div class="section-title">Key Findings</div><div class="section-line"></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True, key='box_grade'):
        fig = px.histogram(df, x='loan_grade', y='loan_status', histfunc='avg', text_auto='.0%',
                           category_orders={'loan_grade': ['A', 'B', 'C', 'D', 'E', 'F', 'G']},
                           title='Failure to Pay Rate by Loan Grade')
        st.plotly_chart(style_chart(fig, 'Loan Grade'), width='stretch')
        st.caption('Risk rises from 10% in grade A to 98% in grade G, with a big jump from C to D.')

with col2:
    with st.container(border=True, key='box_income'):
        data = df[df['loan_to_income'] <= df['loan_to_income'].quantile(0.99)]
        fig = px.histogram(data, x='loan_to_income', y='loan_status', histfunc='avg', nbins=10, text_auto='.0%',
                           title='Failure to Pay Rate by Loan to Income')
        st.plotly_chart(style_chart(fig, 'Loan to Income'), width='stretch')
        st.caption('When the loan is more than 30% of the income, most borrowers fail to pay.')

col3, col4 = st.columns(2)

with col3:
    with st.container(border=True, key='box_home'):
        fig = px.histogram(df, x='person_home_ownership', y='loan_status', histfunc='avg', text_auto='.0%',
                           title='Failure to Pay Rate by Home Ownership')
        st.plotly_chart(style_chart(fig, 'Home Ownership'), width='stretch')
        st.caption('Renters fail to pay the most, home owners the least.')

with col4:
    with st.container(border=True, key='box_intent'):
        fig = px.histogram(df, x='loan_intent', y='loan_status', histfunc='avg', text_auto='.0%',
                           title='Failure to Pay Rate by Loan Intent')
        st.plotly_chart(style_chart(fig, 'Loan Intent'), width='stretch')
        st.caption('Debt consolidation and medical loans are the riskiest, venture loans the safest.')

# About the project: model scores and tools
st.markdown('<div class="section-title">About This Project</div><div class="section-line"></div>', unsafe_allow_html=True)

st.write('A machine learning project that predicts if a borrower will fail to pay a loan. '
         'The final model is a CatBoost classifier tuned with Optuna and tested with Stratified 5-Fold cross-validation.')

scores = [('85%', 'F1 Score'), ('95%', 'Precision'), ('76%', 'Recall')]

cols = st.columns(3)
for col, (value, label) in zip(cols, scores):
    col.markdown(f'<div class="card"><div class="card-value">{value}</div><div class="card-label">{label}</div></div>',
                 unsafe_allow_html=True)

st.write('')

st.markdown('**Built with:** Python · Pandas · Scikit-learn · CatBoost · Optuna · Plotly · Streamlit')
