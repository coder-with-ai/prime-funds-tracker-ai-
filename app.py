import io
import base64
import json
import math
from datetime import datetime
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import yfinance as yf
from google import genai

# Set Matplotlib to a non-interactive backend
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configure Gemini Client
# IMPORTANT: Replace the string below with your actual API key
client = genai.Client(api_key="AIzaSyAJHNbu9njMA_9fSgsQ5XEYRLAWE908jyk")

# --- DATABASE MODELS ---

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)

class SavingsGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    current_saved = db.Column(db.Float, nullable=False)
    monthly_contribution = db.Column(db.Float, nullable=False)

# Initialize the database file on startup
with app.app_context():
    db.create_all()

# --- ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

# 1. Budget Tracker Routes
@app.route('/budget')
def budget():
    expenses = Expense.query.all()
    if not expenses:
        return render_template('budget.html', plot_url=None, raw_expenses=[])
        
    data = [{'Category': e.category, 'Amount': e.amount} for e in expenses]
    df = pd.DataFrame(data)
    df_grouped = df.groupby('Category', as_index=False).sum()
    
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(df_grouped['Category'], df_grouped['Amount'], color='#4facfe')
    ax.set_title("Total Expenses by Category", pad=15)
    ax.set_ylabel("Amount ($)")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', transparent=True)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()
    
    return render_template('budget.html', plot_url=plot_url, raw_expenses=expenses)

@app.route('/add_expense', methods=['POST'])
def add_expense():
    cat = request.form.get('category')
    amt = request.form.get('amount')
    if cat and amt:
        new_expense = Expense(category=cat, amount=float(amt))
        db.session.add(new_expense)
        db.session.commit()
    return redirect(url_for('budget'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_expense(id):
    expense_to_delete = Expense.query.get_or_404(id)
    db.session.delete(expense_to_delete)
    db.session.commit()
    return redirect(url_for('budget'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):
    expense_to_edit = Expense.query.get_or_404(id)
    if request.method == 'POST':
        expense_to_edit.category = request.form.get('category')
        expense_to_edit.amount = float(request.form.get('amount'))
        db.session.commit()
        return redirect(url_for('budget'))
    return render_template('edit.html', expense=expense_to_edit)

# 2. AI Analysis Route
@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    ai_suggestion = None
    market_data_summary = None
    
    if request.method == 'POST':
        investment_amount = request.form.get('amount')
        currency = request.form.get('currency', 'USD')
        symbol = "₹" if currency == "INR" else "$" if currency == "USD" else "€"
        
        tickers = ['SPY', 'GLD', 'QQQ']
        market_trends = {}
        for ticker in tickers:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1mo") 
            if not hist.empty:
                start_price = hist['Close'].iloc[0]
                end_price = hist['Close'].iloc[-1]
                percent_change = ((end_price - start_price) / start_price) * 100
                market_trends[ticker] = round(percent_change, 2)
        
        market_data_summary = f"S&P 500: {market_trends.get('SPY', 0)}%, Gold: {market_trends.get('GLD', 0)}%, Tech: {market_trends.get('QQQ', 0)}%"

        prompt = f"""
        You are a highly analytical financial assistant. A user wants to invest exactly {symbol}{investment_amount} {currency}.
        Here is the 1-month performance of key market indicators: {market_data_summary}.
        
        CRITICAL INSTRUCTIONS:
        1. Do NOT give generic advice. Tailor your strategy specifically for a portfolio size of {symbol}{investment_amount}.
        2. You MUST provide exact mathematical allocations (e.g., 40% = {symbol}X amount). 
        3. Explain WHY you allocated that specific amount based on the provided live market data.
        4. Format the response as a bulleted list. Do not give guaranteed financial advice.
        """
        
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            ai_suggestion = response.text
        except Exception as e:
            ai_suggestion = f"Error communicating with AI: {str(e)}"
            
    return render_template('analysis.html', ai_suggestion=ai_suggestion, market_data_summary=market_data_summary)

# 3. Smart Savings Planner Routes
@app.route('/savings')
def savings():
    goals = SavingsGoal.query.all()
    goals_data = []
    
    for g in goals:
        progress = min(100, (g.current_saved / g.target_amount) * 100) if g.target_amount > 0 else 0
        remaining = max(0, g.target_amount - g.current_saved)
        
        if remaining == 0:
            months_left = 0
            eta = "Goal Reached! 🎉"
        elif g.monthly_contribution > 0:
            months_left = math.ceil(remaining / g.monthly_contribution)
            now = datetime.now()
            future_month = now.month - 1 + months_left
            future_year = now.year + (future_month // 12)
            
            month_idx = (future_month % 12) + 1
            future_month_name = datetime(2000, month_idx, 1).strftime('%B')
            eta = f"{future_month_name} {future_year}"
        else:
            months_left = "∞"
            eta = "Needs monthly contribution"
            
        goals_data.append({
            'id': g.id,
            'name': g.name,
            'target': g.target_amount,
            'current': g.current_saved,
            'monthly': g.monthly_contribution,
            'progress': round(progress, 1),
            'months_left': months_left,
            'eta': eta
        })
        
    return render_template('savings.html', goals=goals_data)

@app.route('/add_goal', methods=['POST'])
def add_goal():
    name = request.form.get('name')
    target = float(request.form.get('target', 0))
    current = float(request.form.get('current', 0))
    monthly = float(request.form.get('monthly', 0))
    
    if name and target > 0:
        new_goal = SavingsGoal(name=name, target_amount=target, current_saved=current, monthly_contribution=monthly)
        db.session.add(new_goal)
        db.session.commit()
        
    return redirect(url_for('savings'))

@app.route('/delete_goal/<int:id>', methods=['POST'])
def delete_goal(id):
    goal = SavingsGoal.query.get_or_404(id)
    db.session.delete(goal)
    db.session.commit()
    return redirect(url_for('savings'))

if __name__ == '__main__':
    app.run(debug=True)