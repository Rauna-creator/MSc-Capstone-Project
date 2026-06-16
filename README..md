# MSc Capstone Project — Medical Aid Uptake Prediction

A machine learning project predicting medical aid uptake intention among young Namibians, built for Namibia Medical Care (NMC) as part of an MSc in Data Science at the University of Europe for Applied Sciences.

## What this project does
- Analyses primary survey data collected from 553 young Namibians aged 18 to 35
- Predicts likelihood of signing up for medical aid using supervised machine learning
- Trains and compares three classification models: Logistic Regression, Random Forest, and XGBoost
- Runs sentiment analysis on open-text survey responses using TextBlob
- Applies LDA topic modelling using Gensim to identify thematic clusters
- Delivers findings through an interactive Streamlit dashboard for NMC's marketing team

## Model results
| Model | Accuracy |
|-------|----------|
| Logistic Regression | 91% |
| Random Forest | 88% |
| XGBoost | 92% |

XGBoost was selected as the best performing model and is used in the dashboard.

## Key findings
- Willingness to pay is the strongest predictor of medical aid membership by a significant margin
- The majority of respondents are willing to pay under N$500 per month — below NMC's entry-level pricing of N$735
- 38% of open-text responses carry negative sentiment, with frustration around cost as the dominant theme
- Four LDA topics identified: perceived expensiveness, cost and benefit awareness, structural unemployment barrier, and general avoidance perception

## Files
- `Capstone_Project.ipynb` — main notebook with all code and analysis
- `app.py` — Streamlit dashboard
- `NMC_survey_cleaned.csv` — cleaned survey data (553 responses, 551 usable records, 25 features)
- `model_rf.pkl` — saved XGBoost model (best performing)
- `feature_names.pkl` — saved feature names used by the dashboard

## How to run the dashboard
```bash
cd your-project-folder
streamlit run app.py
```

## Status
Dashboard complete and running locally. Deployment to Streamlit Cloud in progress.

## Built with
Python, Jupyter Notebook, scikit-learn, XGBoost, NLTK, TextBlob, Gensim, Streamlit, Plotly, Pandas, Matplotlib, Seaborn, Joblib
