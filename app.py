import pandas as pd
import streamlit as st
import joblib

st.set_page_config(layout='wide', page_title='loan project')

st.title('Loan Status Prediction')
st.write('Enter the borrower and loan details, then press **Predict** to see if the borrower is likely to repay.')

df = pd.read_csv('credit_risk_clean.csv')

ml_model = joblib.load('catboost_model.pkl')

with st.expander('Show sample of the data'):
    st.dataframe(df.head())

st.sidebar.header('Borrower Info')

age = st.sidebar.number_input('Age', min_value=20, max_value=94, value=25, step=1)

income = st.sidebar.number_input('Annual Income', min_value=4000, max_value=2000000, value=50000, step=1000)

emp_length = st.sidebar.number_input('Employment Length (years)', min_value=0, max_value=41, value=3, step=1)

home_ownership = st.sidebar.selectbox('Home Ownership', df['person_home_ownership'].unique())

cred_hist_length = st.sidebar.number_input('Credit History Length (years)', min_value=2, max_value=30, value=4, step=1)

default_on_file = st.sidebar.selectbox('Previous Default', ['N', 'Y'])
st.sidebar.caption('N = never failed to pay a loan before')
st.sidebar.caption('Y = failed to pay a loan before')

col1, col2 = st.columns(2)

with col1:
    loan_amnt = st.number_input('Loan Amount', min_value=500, max_value=35000, value=10000, step=500)
    loan_intent = st.selectbox('Loan Intent', df['loan_intent'].unique())

with col2:
    loan_grade = st.selectbox('Loan Grade', ['A', 'B', 'C', 'D', 'E', 'F', 'G'])
    int_rate = st.number_input('Interest Rate (%)', min_value=5.0, max_value=25.0, value=11.0, step=0.1)

loan_to_income = loan_amnt / income
loan_percent_income = round(loan_to_income, 2)

st.metric('Loan to Income', f'{loan_to_income:.0%}')

if st.button('Predict', type='primary'):
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
        st.success(f'The borrower is likely to repay the loan ({repay_chance:.1%} chance to repay)')
    else:
        st.error(f'The borrower is unlikely to repay the loan ({repay_chance:.1%} chance to repay)')
