import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from flask_session import Session
import redis
import resend  

load_dotenv()


def send_email(recipient_list: list, email_subject: str, email_body: str):
    resend.api_key = os.getenv("RESEND_API_KEY")

    if not resend.api_key:
        raise RuntimeError("Environment variable RESEND_API_KEY not set")

    email_service_response = resend.Emails.send({
        "from": "Notifications IJCR <notification@ijcres.in>",
        "to": recipient_list,
        "reply_to": "Editorial Team IJCR <editorial.team@ijcres.in>",
        "subject": email_subject,
        "html": email_body  
    })

    if email_service_response.get("id") is None:
        return False
    return True

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')

@app.route("/", methods=['GET', 'POST'])
def index():
    return redirect(url_for('home'))

@app.route("/home", methods=['GET'])
def home():
    return render_template("home.html")

@app.route("/call-for-papers", methods=['GET'])
def call_for_papers():
    return send_from_directory('static', 'assets/pdfs/call-for-paper-ijcr.pdf')

@app.route("/editional-team", methods=['GET'])
def editional_team():
    return render_template("editional-team.html")

@app.route("/editorial-team/<editor_name>", methods=['GET'])
def editor(editor_name):
    print(editor_name)
    return render_template(f"editor-{editor_name}.html")

@app.route("/call_for_paper/<filename>")
def call_for_paper(filename):
    return send_from_directory('static', filename)

    
if __name__ == "__main__":
    app.run(debug=True, port=1024)
