DisasterAidBot
Overview
DisasterAidBot: A web chatbot for disaster management, offering real-time weather (Open-Meteo), news (NewsAPI), and guidance via Gemini API. Built with Flask, HTML, CSS, JS, it features a dark UI, login, and chat history. Deploy on Render/Heroku with a free domain (Freenom). Ideal for crisis support, it’s extensible for more APIs or database integration. 349 chars.
Features

Real-Time Data: Fetches weather updates (Open-Meteo) and disaster news (NewsAPI) to provide accurate information.
Natural Language Processing: Uses the Gemini API to understand and respond to user queries.
User Authentication: Simple login system (username: user, password: pass) with session management.
Chat History: Stores conversation history for easy reference.
Monochromatic UI: Dark, gradient-based design for a clean and focused user experience.
Responsive Design: Works seamlessly across devices.

File Structure
disaster-aid-bot/
├── static/
│   ├── css/
│   │   ├── style.css        # Main stylesheet for the chatbot
│   │   └── login-styles.css # Stylesheet for the login page
│   ├── js/
│   │   └── script.js        # Client-side JavaScript for chat functionality
│   └── images/
│       └── logo.png         # Placeholder for logo (not included)
├── templates/
│   ├── index.html           # Homepage
│   ├── login.html           # Login page
│   ├── chat.html            # Chat interface
│   └── history.html         # Chat history page
├── .gitignore               # Git ignore file
├── app.py                   # Main Flask application
├── requirements.txt         # Python dependencies
├── Procfile                 # Deployment configuration for Render/Heroku
├── runtime.txt              # Python version specification
└── README.md                # Project documentation

Prerequisites

Python 3.9.6 or higher
Git (for version control and deployment)
API Keys:
Gemini API (Google AI Studio): For natural language processing.
NewsAPI: For disaster-related news.


A free hosting account (e.g., Render, Heroku)

Setup Instructions

Clone the Repository:
git clone https://github.com/yourusername/disaster-aid-bot.git
cd disaster-aid-bot


Set Up a Virtual Environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
pip install -r requirements.txt


Set Environment Variables:

Create a .env file in the root directory:GEMINI_API_KEY=your-gemini-api-key
NEWSAPI_KEY=your-newsapi-key
SECRET_KEY=your-secret-key


Replace your-gemini-api-key and your-newsapi-key with your actual API keys from Google AI Studio and NewsAPI, respectively. Use a secure SECRET_KEY for Flask sessions.


Run the Application Locally:
flask run


Open http://127.0.0.1:5000 in your browser.



Usage

Access the Homepage:

Visit the root URL (/) to see the homepage with a "Login to Chat" button.


Login:

Navigate to /login.
Use the credentials: username user, password pass.
Note: This is a basic authentication system for demonstration. For production, implement a secure authentication mechanism (e.g., Flask-Login).


Chat with DisasterAidBot:

After logging in, you’ll be redirected to the chat interface (/chat).
Type queries related to disaster management (e.g., "How to prepare for a flood?").
The bot responds with advice, real-time weather data, and recent news.


View Chat History:

Click "View History" to see past conversations (/history).


Logout:

Click "Logout" to end your session and return to the homepage.



Deployment
Hosting on Render

Push Code to GitHub:

Create a GitHub repository and push your code:git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/disaster-aid-bot.git
git push -u origin main




Set Up Render:

Sign up at render.com.
Create a new web service and connect your GitHub repository.
Configure:
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn --bind 0.0.0.0:$PORT app:app


Add environment variables in Render’s dashboard (e.g., GEMINI_API_KEY, NEWSAPI_KEY, SECRET_KEY).


Deploy:

Trigger a deployment and monitor logs for errors.
Access your app at the provided Render URL (e.g., https://your-app.onrender.com).



Get a Free Domain

Register a free domain at freenom.com or dot.tk (e.g., disasteraidbot.tk).
Update DNS settings to point to your Render URL (e.g., via a CNAME record).

APIs Used

Gemini API (Google AI Studio): For natural language processing.
Sign up at aistudio.google.com to get an API key.


NewsAPI: For disaster-related news.
Register at newsapi.org to get an API key.


Open-Meteo: For weather and disaster alerts.
No API key required; query directly at api.open-meteo.com.



Notes

Security: The login system is basic. For production, use a secure authentication method.
Chat History: Stored in memory. For persistence, integrate a database (e.g., SQLite, PostgreSQL).
API Limits: Monitor usage to stay within free tier limits of Gemini and NewsAPI.
Customization: Extend functionality by adding more APIs (e.g., USGS for earthquakes) or features (e.g., voice support).

Contributing
Feel free to fork this repository, submit issues, or create pull requests to improve DisasterAidBot.
License
This project is licensed under the MIT License.
