from flask import Flask, render_template, request, session, redirect, url_for
import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'X7pL9qT3mW8rZkY2nF6vJ5bC4xD1tN')

# API Keys (replace with your own or use environment variables)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyBRX-q1Pm7plCYBibKVQU4j5TWJ6U6Pbr4')
NEWSAPI_KEY = os.getenv('NEWSAPI_KEY', 'your-newsapi-key')

# Store chat history
chat_history = []

def get_gemini_response(prompt):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": f"You are DisasterAidBot, an expert in disaster management. Provide accurate, concise solutions for disaster-related queries. Use real-time data if available. Query: {prompt}"}]}]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Error fetching response: {str(e)}"

def get_real_time_data(query):
    # Fetch weather data from Open-Meteo
    weather_url = "https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.1&current_weather=true"
    try:
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()
        weather_data = weather_response.json()['current_weather']
    except:
        weather_data = "Weather data unavailable."

    # Fetch disaster news from NewsAPI
    news_url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWSAPI_KEY}"
    try:
        news_response = requests.get(news_url)
        news_response.raise_for_status()
        news_articles = news_response.json()['articles'][:3]
        news_summary = "\n".join([f"- {article['title']} ({article['source']['name']})" for article in news_articles])
    except:
        news_summary = "News data unavailable."

    return f"Weather: {weather_data}\nRecent News:\n{news_summary}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Temporary credentials
    TEMP_USERNAME = "tempuser"
    TEMP_PASSWORD = "temppass123"

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == TEMP_USERNAME and password == TEMP_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('chat'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        user_input = request.form['message']
        real_time_info = get_real_time_data(user_input)
        full_prompt = f"{user_input}\nReal-time info: {real_time_info}"
        NIGGA_response = get_gemini_response(full_prompt)
        chat_history.append({'user': user_input, 'bot': NIGGA_response, 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
        return render_template('chat.html', history=chat_history)
    
    return render_template('chat.html', history=chat_history)

@app.route('/history')
def history():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('history.html', history=chat_history)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
