import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from pymongo import MongoClient
import redis

load_dotenv()

app = Flask(__name__)


# redish database from here 

# Session Configuration

redis_url = os.getenv("REDIS_URL") # Redis URI
if not redis_url:
    raise RuntimeError("Environment variable REDIS_URL not set")

app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_REDIS"] = redis.from_url(redis_url)
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

Session(app)


# to here



app.secret_key = os.getenv('SECRET_KEY')


client = MongoClient(os.getenv('MONGODB_URI'))
db = client["chatsphere"]
records_signup = db['signup']
records_chats = db['chats']

@app.route("/", methods=['GET']) 
def index():
    return render_template("login.html") 


if __name__ == "__main__":
    app.run(host='0.0.0.0')