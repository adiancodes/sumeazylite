from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from datetime import datetime
from config import Config
from summarizer import summarize_article, summarize_youtube_video

import os
from dotenv import load_dotenv
load_dotenv()

ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")


app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "your-very-secret-key")
mongo = PyMongo(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --- User Model for Flask-Login (MongoDB) ---
class User(UserMixin):
    def __init__(self, user_doc):
        self.id = str(user_doc['_id'])
        self.email = user_doc['email']
        self.password_hash = user_doc['password_hash']

    @staticmethod
    def get(user_id):
        user_doc = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        return User(user_doc) if user_doc else None

    @staticmethod
    def get_by_email(email):
        user_doc = mongo.db.users.find_one({'email': email})
        return User(user_doc) if user_doc else None

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# --- ROUTES ---

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    sentiment = None
    meta = {}
    error = None
    if request.method == 'POST':
        url = request.form.get('url')
        try:
            result = summarize_article(url)
            summary = result['summary']
            sentiment = {
                'polarity': f"{result['polarity']:.2f}",
                'label': result['sentiment']
            }
            meta = {
                'title': result['title'],
                'authors': result['authors'],
                'date': result['date'],
                'language': result['language']
            }
            if current_user.is_authenticated:
                summary_doc = {
                    'user_id': ObjectId(current_user.id),
                    'url': url,
                    'title': meta['title'],
                    'summary': summary,
                    'sentiment': sentiment['label'],
                    'polarity': result['polarity'],
                    'language': meta['language'],
                    'date': datetime.utcnow()
                }
                mongo.db.article_summaries.insert_one(summary_doc)
        except Exception as e:
            error = "Could not summarize this article. Please check the URL or try another one."
    return render_template('index.html', summary=summary, sentiment=sentiment, meta=meta, error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    error = None
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']
        user_doc = mongo.db.users.find_one({'email': email})
        if user_doc and check_password_hash(user_doc['password_hash'], password):
            user = User(user_doc)
            login_user(user)
            return redirect(url_for('index'))
        else:
            error = "Invalid email or password."
    return render_template('login.html', error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    error = None
    message = None
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']
        if mongo.db.users.find_one({'email': email}):
            error = "Email already registered."
        else:
            user_doc = {
                'email': email,
                'password_hash': generate_password_hash(password)
            }
            mongo.db.users.insert_one(user_doc)
            message = "Registered successfully! Please login."
            return redirect(url_for('login'))
    return render_template('signup.html', error=error, message=message)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/youtube', methods=['GET', 'POST'])
def youtube():
    summary = None
    sentiment = None
    meta = {}
    error = None
    if request.method == 'POST':
        url = request.form.get('url')
        try:
            result = summarize_youtube_video(url)
            summary = result['summary']
            sentiment = {
                'polarity': f"{result['polarity']:.2f}",
                'label': result['sentiment']
            }
            meta = {
                'title': result['title'],
                'language': result['language']
            }
            if current_user.is_authenticated:
                summary_doc = {
                    'user_id': ObjectId(current_user.id),
                    'url': url,
                    'title': meta['title'],
                    'summary': summary,
                    'sentiment': sentiment['label'],
                    'polarity': float(result['polarity']),
                    'language': meta['language'],
                    'date': datetime.utcnow()
                }
                mongo.db.article_summaries.insert_one(summary_doc)
        except Exception as e:
            error = str(e)
    return render_template('youtube.html', summary=summary, sentiment=sentiment, meta=meta, error=error)

@app.route('/history')
@login_required
def history():
    summaries = mongo.db.article_summaries.find({'user_id': ObjectId(current_user.id)}).sort('date', -1)
    history = []
    for art in summaries:
        history.append({
            'title': art.get('title', ''),
            'summary': art.get('summary', ''),
            'sentiment': art.get('sentiment', ''),
            'polarity': f"{art.get('polarity', 0):.2f}",
            'language': art.get('language', ''),
            'date': art.get('date', '').strftime('%Y-%m-%d %H:%M') if art.get('date') else '',
            'url': art.get('url', '')
        })
    return render_template('history.html', history=history)

if __name__ == '__main__':
    app.run(debug=True)
