from flask import Flask, render_template, request, redirect
import sqlite3
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# इमेल पठाउने सेटिङ
def send_notification(name, contact, issue):
    sender_email = "तपाईँको_jn385799@gmail.com"  # यहाँ आफ्नो Gmail राख्नुहोस्
    receiver_email = "तपाईँको_jn385799@gmail.com" # यहाँ पनि आफ्नै Gmail राख्नुहोस्
    password = "ubwrkrtltzhcdgyc"       # यहाँ त्यो १६ अक्षरको App Password राख्नुहोस्

    msg = MIMEText(f"नयाँ मद्दत अनुरोध!\n\nनाम: {name}\nसम्पर्क: {contact}\nसमस्या: {issue}")
    msg['Subject'] = 'CyberSahayogi - New Help Request'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/help', methods=['POST'])
def help_request():
    name = request.form.get('name')
    contact = request.form.get('contact')
    issue = request.form.get('issue')
    
    # डेटाबेसमा सेभ गर्ने
    try:
        conn = sqlite3.connect('shield_secure.db')
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS recovery_requests (name TEXT, contact TEXT, issue TEXT)")
        cursor.execute("INSERT INTO recovery_requests (name, contact, issue) VALUES (?, ?, ?)", (name, contact, issue))
        conn.commit()
        conn.close()
        
        # नोटिफिकेसन पठाउने
        send_notification(name, contact, issue)
    except Exception as e:
        print(f"Database error: {e}")

    return "<h1>तपाईँको अनुरोध प्राप्त भयो!</h1><p>हामी तपाईँलाई छिट्टै सम्पर्क गर्नेछौँ।</p><a href='/'>फर्कनुहोस्</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
