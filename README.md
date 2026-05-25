<h2>#PRIME FUNDS TRACKER AI</h2>

<h4>This is a highly impressive, full-stack personal finance application. Based on the app.py file you provided, you have built a comprehensive tool that tackles personal wealth management from three distinct angles: tracking past spending, analyzing present market opportunities, and predicting future savings.</h4>

<h4><h3>💡 The Core Concept: "PRIME FUNDS TRACKER AI"</h3>
Most financial apps do only one thing: they either track your budget or they act as an investment broker. Nexus Finance bridges that gap. It is designed to be a holistic "financial co-pilot" that helps a user stop leaking money, intelligently allocate their remaining cash using live market data, and visually plot their path to major life goals.
Instead of relying on generic advice, the application leverages Generative AI (Google Gemini 2.5 Flash) and Live Market APIs (Yahoo Finance) to provide dynamic, mathematically sound strategies tailored to the user's exact financial situation.</h4>

<h4>
<h3>🚀 Breakdown of Core Features</h3>
 
1. Budget Tracker (The Past)<br>
This module acts as the user's foundational cash-flow manager.
Full CRUD Functionality: Users can seamlessly Add, View, Edit, and Delete daily expenses.
Automated Data Processing: The app uses Pandas to instantly group and sum raw transaction data by category.
Server-Side Rendering Visualization: Instead of relying on heavy frontend JavaScript libraries for this section, the app securely generates a Matplotlib bar chart on the backend, converts it to a Base64 image stream, and serves it directly to the HTML. This ensures lightweight, instantaneous rendering.

3. AI Investment Simulator (The Present)<br>
This is the "Next-Gen" feature of the application, transforming it from a simple tracker into an intelligent advisor.
Live Financial Data: When a user submits an inquiry, the app uses the yfinance library to fetch the real-time 30-day historical performance of three major market sectors: the S&P 500 (SPY), Gold (GLD), and Tech (QQQ).
Multi-Currency Support: Users can simulate investments in USD ($), EUR (€), or INR (₹).
Prompt-Engineered AI: The app bundles the user's chosen currency, their exact investment amount, and the live market data into a highly strict prompt. It forces the Gemini 2.5 Flash model to act as an expert quantitative analyst, outputting exact mathematical dollar/rupee allocations rather than generic advice.
3. Smart Savings Planner (The Future)<br>
A highly motivational tool designed to project wealth milestones.
Dynamic Timelines: Users input a target goal (e.g., "$10,000 for a car"), what they currently have, and what they can contribute monthly.
Algorithmic ETA Calculation: The backend uses Python's math and datetime libraries to calculate exactly how many months it will take to reach the goal, dynamically outputting the precise target month and year (e.g., "October 2026").
Visual Progress: Calculates percentage completion on the fly, which powers the sleek CSS progress bars on the frontend.
<h3>🛠️ Technical Architecture</h3>
 
Under the hood, the application is built using a robust, modern Python stack:

Backend Framework: Flask. It handles the routing, form submissions, and orchestration between the database and external APIs.

Database: SQLite managed via Flask-SQLAlchemy. It uses an Object-Relational Mapper (ORM) to securely store Expense and SavingsGoal data without writing raw SQL queries.

Data Science Layer: NumPy and Pandas for structuring and aggregating the database queries, and Matplotlib for static charting.

External Integrations: * yfinance for scraping live ticker data from Yahoo Finance.

google-genai for communicating with Google's Large Language Models.

Install dependencies: pip install Flask Flask-SQLAlchemy pandas numpy matplotlib yfinance google-genai</h4>

<img width="2816" height="1536" alt="Gemini_Generated_Image_c1dagjc1dagjc1da" src="https://github.com/user-attachments/assets/6812e21c-c123-4d32-ace5-9997fb0309e2" />

<h4>AUTHOR - ANUJ SAINI</h4>
<h4>AUTHOR - SHREYA JAISWAL</h4>
<h4>AUTHOR - SHUBHI SINGH</h4>
