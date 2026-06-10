# 🏦 Geldium AI Collections System

> AI-powered Delinquency Prediction and Collections Management System for digital lending companies.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100-green)
![React](https://img.shields.io/badge/React-18-61DAFB)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3-orange)
![Railway](https://img.shields.io/badge/Backend-Railway-blueviolet)
![Vercel](https://img.shields.io/badge/Frontend-Vercel-black)

---

## 🎯 Problem Statement

Geldium, a digital lending and consumer credit company, is experiencing increasing credit card delinquency rates. By the time the collections team identifies at-risk customers, it is often too late to intervene effectively — resulting in significant financial losses.

---

## 💡 Solution

An end-to-end AI-powered system that:
- **Predicts** which customers are likely to miss payments — before it happens
- **Classifies** customers into High / Medium / Low risk categories
- **Automates** collections actions based on risk level
- **Visualizes** risk data through a professional dashboard

---

## 🚀 Live Demo

| Service | URL |
|---|---|
| 🌐 Frontend Dashboard | [geldium-ai.vercel.app](https://geldium-ai.vercel.app) |
| ⚡ Backend API | [web-production-cb024.up.railway.app](https://web-production-cb024.up.railway.app) |
| 📄 API Docs | [/docs](https://web-production-cb024.up.railway.app/docs) |

---

## ✨ Features

### 🤖 AI & Machine Learning
- Random Forest Classifier trained on 1,000 synthetic customers
- 7 input features: Age, Income, Credit Score, Credit Utilization, Debt-to-Income Ratio, Missed Payments, Payment History
- Risk Score (0–100) + Risk Label (High / Medium / Low)
- Probability breakdown for each risk category

### 💻 Frontend Dashboard
- 📊 KPI Cards — Total Customers, High Risk Count, Avg Risk Score, Low Risk Count
- 🍩 Risk Distribution Donut Chart
- 📈 Monthly Delinquency Trend Line Chart
- 🔴 High Risk Alerts Table
- 👥 Customer List with Search & Filter
- 🔍 Live Risk Analyzer — enter details, get instant AI prediction
- 📋 Reports with Bar Charts and Collections Funnel
- 🌙 Dark / Light Mode Toggle

### ⚡ Backend API
- `POST /predict` — Predict risk for a customer
- `GET /customers` — Get all customers with predictions
- `GET /stats` — Get dashboard statistics
- `GET /customers/{id}` — Get specific customer

### 🛡️ Responsible AI
- Fairness checks to prevent discrimination
- Explainable predictions with probability breakdown
- Transparent model decisions
- Regulatory compliance ready

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| ML Model | Python, scikit-learn, Random Forest, pandas, numpy |
| Backend | FastAPI, SQLite, Uvicorn, Pydantic |
| Frontend | React.js, Tailwind CSS, Recharts, Axios, Lucide React |
| Deployment | Railway (Backend) + Vercel (Frontend) |

---

## 📁 Project Structure

```
geldium-ai/
│
├── backend/
│   ├── main.py          # FastAPI routes
│   ├── database.py      # SQLite setup
│   └── schemas.py       # Pydantic models
│
├── frontend/
│   └── src/
│       ├── api/         # API calls
│       ├── components/  # Reusable components
│       └── pages/       # Dashboard, Customers, Analyzer, Reports
│
├── model/
│   ├── train.py         # Model training
│   ├── predict.py       # Prediction logic
│   └── artifacts/       # Saved .pkl model
│
├── data/
│   ├── generate_data.py # Synthetic data generator
│   └── customers.csv    # 1000 customer dataset
│
└── requirements.txt
```

---

## ⚙️ Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/tharanin1301-dotcom/geldium-ai.git
cd geldium-ai
```

### 2. Setup Python environment
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Generate data & train model
```bash
python data/generate_data.py
python model/train.py
```

### 4. Start backend
```bash
uvicorn backend.main:app --reload
```

### 5. Start frontend
```bash
cd frontend
npm install
npm run dev
```

### 6. Open browser
```
http://localhost:5173
```

---

## 📊 Model Performance

| Metric | Value |
|---|---|
| Algorithm | Random Forest (100 estimators) |
| Training samples | 800 |
| Testing samples | 200 |
| Features | 7 |
| Output | Risk Label + Score + Probabilities |

---

## 🔮 Future Improvements

- [ ] Real customer data integration
- [ ] Automated SMS/email reminders
- [ ] Model retraining pipeline
- [ ] Role-based access control
- [ ] Advanced explainability (SHAP values)

---

## 👨‍💻 Author

**Tharani** — AI & Data Science Student, IFET College of Engineering

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://linkedin.com)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black)](https://github.com/tharanin1301-dotcom)

---

## 📄 License

MIT License — feel free to use for learning and portfolio purposes.
