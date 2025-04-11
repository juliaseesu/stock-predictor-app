from flask import Flask, render_template, request, redirect, url_for, session
import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression
import plotly.graph_objs as go
import plotly.io as pio
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stockapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    watchlist = db.relationship('Watchlist', backref='user', lazy=True)

class Watchlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username'].strip().lower()
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            error = "Username already exists."
        else:
            new_user = User(username=username, password_hash=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            session['user'] = username
            return redirect(url_for('index'))
    return render_template('register.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username'].strip().lower()
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user'] = username
            return redirect(url_for('index'))
        else:
            error = 'Invalid username or password.'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/remove/<ticker>', methods=['POST'])
def remove_ticker(ticker):
    if 'user' not in session:
        return redirect(url_for('login'))
    user = User.query.filter_by(username=session['user']).first()
    item = Watchlist.query.filter_by(user_id=user.id, ticker=ticker).first()
    if item:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = User.query.filter_by(username=session['user']).first()
    chart_html = None
    error = None
    selected_ticker = request.form.get('ticker') or request.args.get('ticker')

    if selected_ticker:
        ticker = selected_ticker.strip().upper()
        try:
            data = yf.download(ticker, period='6mo')
            if data.empty:
                raise ValueError("No data found. Try another ticker.")

            data['Days'] = range(len(data))
            model = LinearRegression()
            model.fit(data[['Days']], data['Close'])
            data['Prediction'] = model.predict(data[['Days']])

            trace_actual = go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Actual Price')
            trace_predicted = go.Scatter(x=data.index, y=data['Prediction'], mode='lines', name='Predicted Price')
            layout = go.Layout(title=f"{ticker} Price Prediction", xaxis_title="Date", yaxis_title="Price (USD)", template="plotly_dark")
            fig = go.Figure(data=[trace_actual, trace_predicted], layout=layout)
            chart_html = pio.to_html(fig, full_html=False)

            existing = Watchlist.query.filter_by(user_id=user.id, ticker=ticker).first()
            if not existing:
                db.session.add(Watchlist(ticker=ticker, user_id=user.id))
                db.session.commit()

        except Exception as e:
            error = str(e)

    watchlist_items = Watchlist.query.filter_by(user_id=user.id).all()
    watchlist = [item.ticker for item in watchlist_items]

    return render_template("index.html", chart_html=chart_html, error=error, watchlist=watchlist)
