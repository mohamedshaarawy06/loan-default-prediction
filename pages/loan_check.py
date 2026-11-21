import streamlit as st
import pandas as pd
import joblib
import base64
import plotly.graph_objects as go


@st.cache_data
def load_data():
    return pd.read_csv('credit_risk_clean.csv')


@st.cache_resource
def load_model():
    return joblib.load('catboost_model.pkl')


df = load_data()
ml_model = load_model()

with open('images/advisor.jpg', 'rb') as f:
    advisor_image = base64.b64encode(f.read()).decode()

st.markdown(f'''
<div class="hero" style="padding: 50px; background-image: linear-gradient(90deg, rgba(11,37,69,0.95), rgba(11,37,69,0.4)),
     url(data:image/jpg;base64,{advisor_image});">
    <span class="badge">LOAN CHECK</span>
    <h1>Check a Loan Application</h1>
    <p>Enter the borrower and loan details, then press Predict.</p>
</div>
''', unsafe_allow_html=True)

st.write('')

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True, key='box_borrower'):
        st.subheader(':material/person: Borrower Info')
        age = st.number_input('Age', min_value=20, max_value=94, value=25, step=1)
        income = st.number_input('Annual Income', min_value=4000, max_value=2000000, value=50000, step=1000)
        emp_length = st.number_input('Employment Length (years)', min_value=0, max_value=41, value=3, step=1)
        home_ownership = st.selectbox('Home Ownership', df['person_home_ownership'].unique())
        cred_hist_length = st.number_input('Credit History Length (years)', min_value=2, max_value=30, value=4, step=1)
        default_on_file = st.selectbox('Previous Default', ['N', 'Y'],
                                       help='N = never failed to pay a loan before, Y = failed to pay a loan before')

with col2:
    with st.container(border=True, key='box_loan'):
        st.subheader(':material/payments: Loan Info')
        loan_amnt = st.number_input('Loan Amount', min_value=500, max_value=35000, value=10000, step=500)
        loan_intent = st.selectbox('Loan Intent', df['loan_intent'].unique())
        loan_grade = st.selectbox('Loan Grade', ['A', 'B', 'C', 'D', 'E', 'F', 'G'])
        int_rate = st.number_input('Interest Rate (%)', min_value=5.0, max_value=25.0, value=11.0, step=0.1)

        loan_to_income = loan_amnt / income
        loan_percent_income = round(loan_to_income, 2)

        st.metric('Loan to Income', f'{loan_to_income:.0%}')

predict = st.button('Predict', type='primary', icon=':material/query_stats:', width='stretch')

if predict:
    if emp_length > age - 14 or cred_hist_length > age - 14:
        st.warning('Employment length and credit history must fit the borrower age.')
        st.stop()

    if loan_to_income > 0.83:
        st.warning('The loan is too large compared to the income for this model.')
        st.stop()

    new_data = pd.DataFrame(columns=df.columns.drop('loan_status'),
                            data=[[age, income, home_ownership, emp_length, loan_intent, loan_grade, loan_amnt,
                                   int_rate, loan_percent_income, default_on_file, cred_hist_length, loan_to_income]])

    prediction = ml_model.predict(new_data)[0]
    repay_chance = ml_model.predict_proba(new_data)[0][0]

    if prediction == 0:
        color = '#1E8E5A'
        title = 'Likely to Repay'
        text = 'This borrower looks safe. The loan can move to the next step.'
    else:
        color = '#C0392B'
        title = 'Unlikely to Repay'
        text = 'This borrower is high risk. The loan needs a careful review.'

    st.markdown('<div class="section-title">Result</div><div class="section-line"></div>', unsafe_allow_html=True)

    res1, res2 = st.columns(2)

    with res1:
        fig = go.Figure(go.Indicator(mode='gauge+number', value=repay_chance * 100,
                                     number={'suffix': '%', 'valueformat': '.1f', 'font': {'color': color}},
                                     title={'text': 'Chance to Repay'},
                                     gauge={'axis': {'range': [0, 100]},
                                            'bar': {'color': color},
                                            'steps': [{'range': [0, 50], 'color': '#FBE9E7'},
                                                      {'range': [50, 100], 'color': '#E6F4EC'}]}))
        fig.update_layout(height=300, margin=dict(t=60, b=10, l=30, r=30), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, width='stretch')

    with res2:
        st.markdown(f'''
        <div class="result" style="background: {color};">
            <h3>{title}</h3>
            <p>{text}</p>
            <p><b>Chance to repay:</b> {repay_chance:.1%}<br>
            <b>Loan to income:</b> {loan_to_income:.0%}<br>
            <b>Loan grade:</b> {loan_grade}</p>
        </div>
        ''', unsafe_allow_html=True)
