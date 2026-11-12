# 🏦 Loan Default Prediction — Credit Risk

Predicting whether a borrower will **fail to repay a loan** from borrower and loan details, with a tuned **CatBoost** classification pipeline served through an interactive **Streamlit** app.

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.9-F7931E?logo=scikitlearn&logoColor=white)
![CatBoost](https://img.shields.io/badge/CatBoost-1.2-FFCC00)
![Optuna](https://img.shields.io/badge/Optuna-Tuning-4B8BBE)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)

> Built with a banking background in mind: I spent 3 years as a Settlement Officer & Transactions Analyst at Suez Canal Bank, so the analysis focuses on what a credit team actually cares about: catching risky borrowers without rejecting good ones.

---

## 📌 Problem

Banks lose money when borrowers default. The goal is to **flag risky borrowers before the loan is given**, while keeping false alarms on good customers low.

---

## 📊 Results

Final model: **CatBoost** inside a scikit-learn / imbalanced-learn `Pipeline`, evaluated with **Stratified 5-fold cross-validation**.

| Metric ("Failed to Pay" class) | Score |
|---|---|
| **F1** | **0.85** (84.68%, folds 83.3% – 86.7%) |
| Precision | **95.4%** |
| Recall | 76.1% |
| Accuracy (overall) | 94% |

> When the model flags a borrower as risky, it is right **95% of the time**, and it catches about **3 out of 4** borrowers who default.

**Top features:** `person_income`, `loan_to_income`, `loan_grade`, `home_ownership = RENT`, `loan_percent_income`.

### Model comparison (Stratified 5-fold CV, F1)

| Model | Test F1 |
|---|---|
| Logistic Regression | 0.62 |
| KNN | 0.72 |
| Decision Tree | 0.76 |
| Random Forest | 0.83 |
| LightGBM | 0.83 |
| XGBoost | 0.84 |
| CatBoost | 0.84 |
| **CatBoost (tuned with Optuna)** | **0.85** |

SMOTE and BorderlineSMOTE were tested on all 7 models and **did not improve** the results, so the final model is trained on the original data.

### Choosing a decision threshold

Lowering the threshold catches more defaulters but rejects more good borrowers. The right choice depends on which mistake costs the bank more.

| Threshold | Precision | Recall |
|---|---|---|
| **0.5 (used)** | **95.4%** | **76.1%** |
| 0.3 | 87.6% | 80.3% |
| 0.2 | 79.3% | 83.6% |
| 0.1 | 63.0% | 89.1% |

---

## 🗂️ Dataset

**Source:** [Credit Risk Dataset — Kaggle](https://www.kaggle.com/datasets/laotse/credit-risk-dataset) · 32,581 loans · 12 columns · Target: `loan_status` (1 = default, 0 = paid) · Class balance: **78% paid / 22% default**

| Column | Description |
|---|---|
| `person_age` | Borrower age |
| `person_income` | Annual income |
| `person_home_ownership` | RENT / OWN / MORTGAGE / OTHER |
| `person_emp_length` | Employment length (years) |
| `loan_intent` | EDUCATION, MEDICAL, VENTURE, PERSONAL, HOMEIMPROVEMENT, DEBTCONSOLIDATION |
| `loan_grade` | Risk grade from A (lowest) to G (highest) |
| `loan_amnt` | Loan amount |
| `loan_int_rate` | Interest rate (%) |
| `loan_percent_income` | Loan amount as a share of income |
| `cb_person_default_on_file` | Previous default (Y / N) |
| `cb_person_cred_hist_length` | Credit history length (years) |
| `loan_status` | **Target**: 1 = default, 0 = paid |

---

## 🔍 Key Insights from EDA

- **Loan grade:** default rate rises from ~10% in grade A to **98% in grade G**, with a sharp jump between C (21%) and D (59%).
- **Loan-to-income:** the default rate rises sharply once the loan is more than **~30% of income**.
- **Hidden pattern:** even grade A/B borrowers default **62%** of the time when the loan is above 30% of their income, vs **7%** below it.
- **Home ownership:** renters default the most (32%), home owners the least (7.5%).
- **Loan intent:** debt consolidation (28.7%) and medical (26.8%) loans are the riskiest; venture (14.9%) is the safest.
- **Previous default:** 37.9% default rate vs 18.4% for borrowers with a clean record.
- **Age and credit history length** have almost no effect.

### 🧪 Data quality finding

`loan_percent_income` should equal loan amount ÷ income, but in **387 rows** it is clearly lower than the real ratio (not a rounding issue), and **every one of these borrowers defaulted**. The engineered `loan_to_income` feature holds the correct value.

Adding `loan_to_income` raised F1 from 84.25 to 84.68, but most of that gain comes from those 387 rows, so a realistic score is about **84%**.

---

## 🔧 Methodology

1. **Data cleaning**: removed 165 duplicates and impossible records (age > 120, employment length longer than age).
2. **Feature engineering**: `loan_to_income = loan_amnt / person_income`.
3. **EDA**: default rate by every categorical and numerical feature (interactive Plotly charts).
4. **Preprocessing** in a `ColumnTransformer`:

   | Step | Columns |
   |---|---|
   | `RobustScaler` + `KNNImputer` | numerical features (fills missing interest rate & employment length) |
   | `OneHotEncoder` | home ownership, loan intent, previous default |
   | `OrdinalEncoder` (A → G) | `loan_grade`, keeping the risk order |

5. **Model comparison**: 7 models with Stratified 5-fold CV, scored with **F1** because of the class imbalance.
6. **Imbalance handling**: tested `SMOTE` and `BorderlineSMOTE`.
7. **Hyperparameter tuning**: `RandomizedSearchCV`, then **Optuna**. Best: `depth=5`, `learning_rate≈0.147`, `iterations=1489`, `l2_leaf_reg=4`.
8. **Evaluation**: classification report, confusion matrix, threshold analysis and feature importance.
9. **Deployment**: Streamlit app.

---

## ⚠️ Limitations

- There is no separate hold-out test set: all scores come from cross-validation, and the tuned score is slightly optimistic (84.38 on a different CV split).
- The model leans on `loan_grade` and `loan_int_rate`, which already reflect the bank's own risk assessment. Without both, F1 drops to about 73.6.
- Some overfitting remains (train F1 93.9 vs CV 84.7), although scores are stable across folds.
- The data has very clear patterns and no dates, so results may not carry over to real bank data.

---

## 📁 Project Structure

```
.
├── loan-default-prediction.ipynb   # Full workflow: cleaning, EDA, modeling, evaluation
├── app.py                          # Streamlit web app
├── catboost_model.pkl              # Trained pipeline (preprocessing + CatBoost)
├── credit_risk_dataset.csv         # Raw dataset
├── credit_risk_clean.csv           # Cleaned dataset (used by the app)
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/mohamedshaarawy06/loan-default-prediction.git
cd loan-default-prediction
```

### 2. Create a virtual environment & install dependencies
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

> ⚠️ Keep the pinned versions: `catboost_model.pkl` was saved with these library versions and may not load with others.

### 3. Run the app
```bash
streamlit run app.py
```
Then open `http://localhost:8501` in your browser.

### 4. Reproduce the analysis
Open `loan-default-prediction.ipynb` and run all cells. It recreates `credit_risk_clean.csv`, `catboost_model.pkl` and `app.py` (about an hour, because of the tuning).

> The charts are interactive Plotly charts, so GitHub may not render them. Open the notebook locally to see them.

---

## 🖥️ The App

- Enter borrower details (age, income, employment, home ownership, credit history, previous default) and loan details (amount, intent, grade, interest rate).
- Shows the live **loan-to-income** ratio, then predicts whether the borrower will repay, with the **probability of repayment**.
- Rejects impossible inputs, such as employment length or credit history that does not fit the borrower's age, or a loan far too large for the income.
- It gives **no advice on how to get approved**. I tested that feature and removed it, because similar real borrowers repaid less than the model predicted: the model shows correlation, not cause.

---

## 🛠️ Tech Stack

`Python` · `pandas` · `NumPy` · `scikit-learn` · `imbalanced-learn` · `CatBoost` · `XGBoost` · `LightGBM` · `Optuna` · `Plotly` · `Streamlit` · `joblib`

---

## 👤 Author

**Mohamed Shaarawy**, Data Scientist
[LinkedIn](https://www.linkedin.com/in/mohamed-shaarawy-22232a22b) · [GitHub](https://github.com/mohamedshaarawy06)
