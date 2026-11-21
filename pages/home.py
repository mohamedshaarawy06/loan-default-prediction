import streamlit as st
import base64

# Read the image as text so it can be used as a background
with open('images/hero.jpg', 'rb') as f:
    hero_image = base64.b64encode(f.read()).decode()

st.markdown(f'''
<div class="hero" style="background-image: linear-gradient(90deg, rgba(11,37,69,0.95), rgba(11,37,69,0.45)),
     url(data:image/jpg;base64,{hero_image});">
    <div class="brand">NILE <span>BANK</span></div>
    <div class="after-brand">
        <span class="badge">AI-POWERED LENDING</span>
        <h1>Smarter Loan Decisions</h1>
        <p>Nile Bank uses machine learning to predict if a borrower will repay a loan,
        in seconds, from simple borrower and loan details.</p>
    </div>
</div>
''', unsafe_allow_html=True)

st.write('')
st.page_link('pages/loan_check.py', label='Check Your Loan in Seconds', icon=':material/arrow_forward:')

# Numbers about the project
st.markdown('<div class="section-title">Why Nile Bank</div><div class="section-line"></div>',
            unsafe_allow_html=True)

numbers = [('32K+', 'Loans Analyzed'), ('95%', 'Accurate Risk Alerts'),
           ('3 of 4', 'Risky Borrowers Caught'), ('Seconds', 'Instant Decision')]

cols = st.columns(4)
for col, (value, label) in zip(cols, numbers):
    col.markdown(f'<div class="card"><div class="card-value">{value}</div><div class="card-label">{label}</div></div>',
                 unsafe_allow_html=True)

# How the website works
st.markdown('<div class="section-title">How It Works</div><div class="section-line"></div>',
            unsafe_allow_html=True)

steps = [('1', 'Enter Details', 'Fill in the borrower info and the loan info.'),
         ('2', 'Model Analysis', 'A tuned CatBoost model studies the risk.'),
         ('3', 'Get the Result', 'See the chance that the borrower repays.')]

cols = st.columns(3)
for col, (num, title, text) in zip(cols, steps):
    col.markdown(f'''<div class="card"><div class="step-num">{num}</div>
                 <h4>{title}</h4><div class="card-label">{text}</div></div>''', unsafe_allow_html=True)
