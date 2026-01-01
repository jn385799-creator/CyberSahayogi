import os
db_path = os.path.join(os.getcwd(), 'shield_secure.db')

import sqlite3, csv, io
from flask import Flask, request, send_file, Response
from functools import wraps

app = Flask(__name__)

# Admin Credentials
ADMIN_USER = "admin"
ADMIN_PASS = "sahayogi2026"

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not (auth.username == ADMIN_USER and auth.password == ADMIN_PASS):
            return Response('Login Required', 401, {'WWW-Authenticate': 'Basic realm="Login"'})
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="ne">
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CyberSahayogi - Digital Safety</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f4f8; margin: 0; color: #333; }
            .navbar { background: #1a73e8; color: white; padding: 15px; text-align: center; font-weight: bold; font-size: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
            .container { max-width: 600px; margin: 20px auto; padding: 20px; }
            .card { background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin-bottom: 20px; }
            h2 { color: #1a73e8; margin-top: 0; }
            input, textarea { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; }
            button { width: 100%; padding: 14px; background: #28a745; color: white; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; transition: 0.3s; }
            button:hover { background: #218838; }
            .badge { display: inline-block; padding: 5px 12px; background: #e8f0fe; color: #1a73e8; border-radius: 20px; font-size: 12px; margin-bottom: 15px; font-weight: bold; }
            .link-checker { background: #fff3cd; border: 1px solid #ffeeba; padding: 15px; border-radius: 10px; }
            #result { font-weight: bold; margin-top: 10px; }
        </style>
    </head>
    <body>
        <div class="navbar">🇳🇵 CyberSahayogi (साइबर सहयोगी)</div>
        <div class="container">
            <div class="card">
                <div class="badge">🔒 Secure & Encrypted</div>
                <h2>लिङ्कको सत्यता जाँच्नुहोस्</h2>
                <p style="font-size: 14px; color: #666;">शंकास्पद म्यासेजमा आएको लिङ्क यहाँ पेस्ट गरी जाँच गर्नुहोस्।</p>
                <div class="link-checker">
                    <input type="text" id="linkInput" placeholder="https://example.com">
                    <button onclick="checkLink()" style="background: #856404;">जाँच गर्नुहोस्</button>
                    <div id="result"></div>
                </div>
            </div>

            <div class="card">
                <h2>मद्दत प्राप्त गर्नुहोस्</h2>
                <p>तपाईँको अकाउन्ट ह्याक भएको छ वा कुनै साइबर समस्या छ? विवरण भर्नुहोस्।</p>
                <form action="/submit" method="POST">
                    <input type="text" name="name" placeholder="पुरा नाम" required>
                    <input type="text" name="phone" placeholder="WhatsApp नम्बर (Ex: 98XXXXXXXX)" required>
                    <textarea name="issue" placeholder="तपाईँको समस्याको बारेमा छोटकरीमा लेख्नुहोस्..." rows="4"></textarea>
                    <button type="submit">मद्दतको लागि पठाउनुहोस्</button>
                </form>
            </div>
            <p style="text-align: center; color: #888; font-size: 12px;">© 2026 CyberSahayogi | १ मिलियन नेपालीको सुरक्षा लक्ष्य</p>
        </div>

        <script>
            function checkLink() {
                let link = document.getElementById('linkInput').value.toLowerCase();
                let res = document.getElementById('result');
                if (link === "") { res.innerHTML = "लिङ्क हाल्नुहोस्!"; return; }
                if (link.includes('http://')) {
                    res.innerHTML = "❌ खतरा: यो लिङ्क असुरक्षित छ!";
                    res.style.color = "red";
                } else if (link.includes('gift') || link.includes('free') || link.includes('login-') || link.includes('bit.ly')) {
                    res.innerHTML = "⚠️ सावधानी: यो फिसिङ लिङ्क हुन सक्छ!";
                    res.style.color = "orange";
                } else {
                    res.innerHTML = "✅ यो लिङ्क सुरक्षित देखिन्छ।";
                    res.style.color = "green";
                }
            }
        </script>
    </body>
    </html>
    '''

@app.route('/submit', methods=['POST'])
def submit():
    name, phone, issue = request.form['name'], request.form['phone'], request.form['issue']
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO victims (name, phone, issue) VALUES (?, ?, ?)", (name, phone, issue))
    conn.commit()
    conn.close()
    return "<div style='text-align:center; padding:50px;'><h1>✅ पठाइयो!</h1><p>हामी तपाईँलाई चाँडै सम्पर्क गर्नेछौँ।</p><a href='/'>फर्कनुहोस्</a></div>"

@app.route('/admin')
@requires_auth
def admin():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM victims")
    data = c.fetchall()
    conn.close()
    rows = "".join([f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td><a href='https://wa.me/{r[2]}'>WhatsApp</a></td></tr>" for r in data])
    return f'''<h2>Admin Dashboard</h2><table border="1" style="width:100%">{rows}</table>'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
