import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session,send_from_directory
from flask_session import Session
from pymongo import MongoClient
import bcrypt
import redis

load_dotenv()

app = Flask(__name__)

# Redis database configuration
redis_url = os.getenv("REDIS_URL")  # Redis URI
if not redis_url:
    raise RuntimeError("Environment variable REDIS_URL not set")

app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_REDIS"] = redis.from_url(redis_url)
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["PERMANENT_SESSION_LIFETIME"] = 30*24*60*60  # 30 days

Session(app)

app.secret_key = os.getenv('SECRET_KEY')

client = MongoClient(os.getenv('MONGODB_URI'))
db = client["IJCR"]
records_signup = db['signup']
# records_chats = db['chats']

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("psw")
        repeat_password = request.form.get("psw-repeat")
        remember = request.form.get("remember")

        if password == repeat_password:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            records_signup.insert_one({"email": email, "password": hashed_password})

            if remember:
                session.permanent = True  # Session will last for the duration of 30 days
            else:
                session.permanent = False  # Session will be a browser session

            session['email'] = email
            return redirect(url_for('index'))

    email = session.get('email')
    return render_template("dashboard.html", email=email)



@app.route("/editional_team", methods=['GET'])
def editional_team():
    return render_template("editional_team.html")


@app.route("/call_for_paper/<filename>")
def call_for_paper(filename):
    return send_from_directory('static', filename)

@app.route('/sign_out')
def sign_out():
    email = session.pop('email', None)
    if email:
        records_signup.delete_one({'email': email})
    return redirect('/')
    
if __name__ == "__main__":
    app.run(debug=True)
