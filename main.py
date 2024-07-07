import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from flask_session import Session
from pymongo import MongoClient
import bcrypt
import redis
import resend  

load_dotenv()


# def send_email(recipient_list: list, email_subject: str, email_body: str):
    # resend.api_key = os.getenv("RESEND_API_KEY")

    # if not resend.api_key:
    #     raise RuntimeError("Environment variable RESEND_API_KEY not set")

    # email_service_response = resend.Emails.send({
    #     "from": "Notifications IJCR <notification@ijcres.in>",
    #     "to": recipient_list,
    #     "reply_to": "Editorial Team IJCR <editorial.team@ijcres.in>",
    #     "subject": email_subject,
    #     "html": email_body  
    # })

    # if email_service_response.get("id") is None:
    #     return False
    # return True

app = Flask(__name__)

# Redis database configuration
# redis_url = os.getenv("REDIS_URL")  # Redis URI
# if not redis_url:
#     raise RuntimeError("Environment variable REDIS_URL not set")

# app.config["SESSION_TYPE"] = "redis"
# app.config["SESSION_REDIS"] = redis.from_url(redis_url)
# app.config["SESSION_COOKIE_SECURE"] = True
# app.config["SESSION_COOKIE_HTTPONLY"] = True
# app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
# app.config["PERMANENT_SESSION_LIFETIME"] = 30*24*60*60  # 30 days

# Session(app)

# app.secret_key = os.getenv('SECRET_KEY')

# client = MongoClient(os.getenv('MONGODB_URI'))
# db = client["IJCR"]
# records_signup = db['signup']

@app.route("/", methods=['GET', 'POST'])
def index():
    return redirect(url_for('home'))

@app.route("/home", methods=['GET'])
def home():
    return render_template("home.html")

@app.route("/editional_team", methods=['GET'])
def editional_team():
    return render_template("editional_team.html")

@app.route("/editional_team/nitish_kumar", methods=['GET'])
def nitish_kumar():
    return render_template("nitish_kumar.html")

@app.route("/call_for_paper/<filename>")
def call_for_paper(filename):
    return send_from_directory('static', filename)

@app.route('/sign_out')
def sign_out():
    email = session.pop('email', None)
    if email:
        records_signup.delete_one({'email': email})
        
        # Send a goodbye email
        email_subject = "Goodbye from IJCR"
        email_body = render_template("goodbye_email.html", email=email)
        email_body = email_body.replace("{{ email }}", email)
        
        send_email([email], email_subject, email_body)
        print("user signed out")
    
    return redirect('/')


    
if __name__ == "__main__":
    app.run(debug=True)
