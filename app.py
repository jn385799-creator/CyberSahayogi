from flask import Flask, request
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="ne">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cyber Sahayogi Portal</title>
        <style>
            body { font-family: sans-serif; background-color: #e9ecef; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .card { background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); width: 100%; max-width: 350px; }
            h2 { color: #333; text-align: center; }
            input, textarea { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
            button { width: 100%; padding: 10px; background: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Cyber Sahayogi</h2>
            <form action="/help" method="post">
                <input type="text" name="name" placeholder="तपाईँको नाम" required>
                <input type="text" name="contact" placeholder="सम्पर्क नम्बर" required>
                <textarea name="issue" placeholder="के समस्या छ?" required></textarea>
                <button type="submit">मद्दत माग्नुहोस्</button>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/help', methods=['POST'])
def help_request():
    name = request.form.get('name')
    contact = request.form.get('contact')
    issue = request.form.get('issue')

    # यहाँ आफ्नो सही विवरण हाल्नुहोस्
    sender = "jn385799@gmail.com"
    pw = "ubwrkrtltzhcdgyc" # यहाँ आफ्नो App Password हाल्नुहोस्

    msg = MIMEText(f"नाम: {name}\nसम्पर्क: {contact}\nसमस्या: {issue}")
    msg['Subject'] = 'नयाँ साइबर सहयोग अनुरोध'
    msg['From'] = sender
    msg['To'] = sender

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, pw)
            server.sendmail(sender, sender, msg.as_string())
        return "<h2>धन्यवाद!</h2><p>हामी तपाईँलाई छिट्टै सम्पर्क गर्नेछौँ।</p><a href='/'>फर्कनुहोस्</a>"
    except Exception as e:
        # एरर आएमा यहाँ देखिनेछ
        return f"<h2>इमेल पठाउन सकिएन</h2><p>कारण: {str(e)}</p><a href='/'>फेरि कोसिस गर्नुहोस्</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
