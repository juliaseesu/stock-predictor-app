# 📈 Stock & Crypto Price Predictor

This is a Flask web app that predicts the next 30 days of stock or cryptocurrency prices using basic linear regression. Users can register, log in, save a personal watchlist, and view future forecasts in an interactive Plotly graph.

### 🔗 Live Demo  
👉 [View Live App on Render](https://stock-predictor-app-0yj5.onrender.com)

---

## ✨ Features

- 🔒 User registration & login with password hashing
- 📊 Stock and crypto predictions using `yfinance` & `scikit-learn`
- 📈 Interactive graphs with `plotly` showing 30-day future forecasts
- 📌 Persistent personal watchlist (stored in SQLite via SQLAlchemy)
- 🌓 Dark mode interface with clean design
- ✅ Deployed live using Render

---

## 🛠 Tech Stack

- Python + Flask
- SQLite + SQLAlchemy
- Plotly
- YFinance
- Scikit-learn (Linear Regression)
- HTML/CSS + Jinja templates
- Render (for deployment)

---

## 🚀 How to Run Locally

```bash
git clone https://github.com/juliaseesu/stock-predictor-app.git
cd stock-predictor-app
pip install -r requirements.txt
python app.py


---

## ⚠️ Disclaimer

This project is intended for educational and portfolio purposes only.  
It does **not** provide financial advice or real investment recommendations.  
Always do your own research and consult with a licensed financial advisor before making investment decisions.
