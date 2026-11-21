import streamlit as st

st.set_page_config(page_title='Nile Bank', page_icon='🏦', layout='wide')

st.logo('images/logo.svg', size='large')

# Style for the whole website: colors, cards and animations
st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

h1, h2, h3, .hero h1, .card-value, .step-num {font-family: 'Poppins', sans-serif;}

.block-container {padding-top: 2rem; max-width: 1200px;}

/* Top menu: bigger and bold */
[data-testid="stTopNavLink"] {padding: 8px 16px;}
[data-testid="stTopNavLink"] * {font-size: 18px !important; font-weight: 600 !important;}
[data-testid="stTopNavLink"]:hover {background: #E3E8F0;}

/* Animations */
@keyframes fadeUp {
    from {opacity: 0; transform: translateY(25px);}
    to {opacity: 1; transform: translateY(0);}
}
@keyframes grow {
    from {width: 0;}
    to {width: 70px;}
}

/* Big image at the top of each page */
.hero {
    background-size: cover;
    background-position: center;
    border-radius: 18px;
    padding: 80px 50px;
    color: white;
    animation: fadeUp 0.8s ease-out;
}
.hero h1 {color: white; font-size: 44px; margin: 0 0 10px;}

/* Big "NILE BANK" name: shows first, then the rest of the text */
@keyframes zoomIn {
    from {opacity: 0; transform: scale(0.6); letter-spacing: 30px;}
    to {opacity: 1; transform: scale(1); letter-spacing: 6px;}
}
.brand {
    font-family: 'Poppins', sans-serif;
    font-size: 72px;
    font-weight: 700;
    color: white;
    letter-spacing: 6px;
    line-height: 1.1;
    margin-bottom: 22px;
    transform-origin: left;
    animation: zoomIn 1.2s ease-out;
}
.brand span {color: #C9A227;}
.after-brand {animation: fadeUp 0.8s ease-out 1.1s both;}
.hero p {font-size: 19px; max-width: 620px; color: #E8ECF3;}
.badge {
    display: inline-block;
    background: #C9A227;
    color: #0B2545;
    font-weight: 700;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 13px;
    margin-bottom: 14px;
}

/* Section titles */
.section-title {
    color: #0B2545;
    font-size: 28px;
    font-weight: 700;
    margin: 40px 0 6px;
    font-family: 'Poppins', sans-serif;
}
.section-line {
    height: 4px;
    width: 70px;
    background: #C9A227;
    border-radius: 2px;
    margin-bottom: 22px;
    animation: grow 1s ease-out;
}

/* White cards */
.card {
    background: white;
    border-radius: 14px;
    padding: 26px 20px;
    text-align: center;
    box-shadow: 0 4px 14px rgba(11, 37, 69, 0.08);
    border-top: 4px solid #C9A227;
    animation: fadeUp 0.9s ease-out;
    transition: transform 0.3s, box-shadow 0.3s;
    height: 100%;
}
.card:hover {transform: translateY(-6px); box-shadow: 0 10px 24px rgba(11, 37, 69, 0.16);}
.card-value {font-size: 34px; font-weight: 700; color: #0B2545;}
.card-label {font-size: 15px; color: #5A6B7D;}

.step-num {
    width: 46px; height: 46px; line-height: 46px;
    margin: 0 auto 12px;
    border-radius: 50%;
    background: #0B2545; color: #C9A227;
    font-size: 20px; font-weight: 700;
}
.card h4 {color: #0B2545; margin: 0 0 6px;}

/* Streamlit containers with a key that starts with "box" */
[class*="st-key-box"] {
    background: white;
    border-radius: 14px;
    box-shadow: 0 4px 14px rgba(11, 37, 69, 0.08);
    border: none;
    animation: fadeUp 0.9s ease-out;
}

/* "Check a Loan Now" link looks like a gold button */
[data-testid="stPageLink"] a {
    background: #C9A227;
    padding: 10px 22px;
    width: fit-content;
    position: relative;
    overflow: hidden;
}

/* Shine: a white light passes over the button */
@keyframes shine {
    0% {left: -60%;}
    60%, 100% {left: 130%;}
}
[data-testid="stPageLink"] a::after {
    content: '';
    position: absolute;
    top: 0;
    left: -60%;
    width: 40%;
    height: 100%;
    background: linear-gradient(120deg, transparent, rgba(255, 255, 255, 0.6), transparent);
    animation: shine 3s infinite;
}
[data-testid="stPageLink"] a p {color: #0B2545; font-weight: 800; font-size: 17px;}
[data-testid="stPageLink"] a:hover {transform: scale(1.04); background: #D9B43A;}

/* Result box after prediction */
.result {
    border-radius: 14px;
    padding: 26px;
    color: white;
    animation: fadeUp 0.7s ease-out;
}
.result h3 {color: white; margin: 0 0 8px;}

/* Buttons */
.stButton button, [data-testid="stPageLink"] a {
    border-radius: 10px;
    transition: transform 0.2s;
}
.stButton button:hover {transform: scale(1.03);}

.footer {
    text-align: center;
    color: #8392A5;
    font-size: 13px;
    margin-top: 50px;
    padding: 20px;
    border-top: 1px solid #DDE3EA;
}
</style>
''', unsafe_allow_html=True)

home = st.Page('pages/home.py', title='Home', icon=':material/home:', default=True)
loan_check = st.Page('pages/loan_check.py', title='Loan Check', icon=':material/fact_check:')
insights = st.Page('pages/insights.py', title='Insights', icon=':material/insights:')

page = st.navigation([home, loan_check, insights], position='top')
page.run()

st.markdown('<div class="footer">© 2026 Nile Bank · Demo project by Mohamed Shaarawy · Not a real bank</div>',
            unsafe_allow_html=True)
