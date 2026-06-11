# MSc Capstone Project - Medical Aid Uptake Prediction

A machine learning project predicting medical aid uptake intention among young Namibians, built for NMC.

## What this project does
- Analyses survey data from 539 respondents
- Predicts likelihood of signing up for medical aid
- Uses three machine learning models: Logistic Regression, Random Forest, and XGBoost
- Includes sentiment analysis on open-text responses using TextBlob
- Topic modelling using LDA

## Model results
| Model | Accuracy |
|-------|----------|
| Logistic Regression | 91% |
| Random Forest | 88% |
| XGBoost | 92% |

## Files
- Capstone Project.ipynb - main notebook with all code and analysis
- NMC_survey_cleaned.csv - cleaned survey data
- model_rf.pkl - saved Random Forest model

## Status
Work in progress - Streamlit dashboard coming soon.

## Built with
Python, Jupyter Notebook, scikit-learn, XGBoost, NLTK, TextBlob, Gensim