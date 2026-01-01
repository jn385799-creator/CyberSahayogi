from flask import Flask, render_template_string, request, redirect
import sqlite3

app = Flask(__name__)

# डाटाबेस सेटअप
def init_db():
    conn = sqlite3.connect("shield_secure.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS RecoveryForms 
                     (id INTEGER PRIMARY KEY, name TEXT, platform TEXT, 
                      has_phone TEXT, email_changed TEXT, last_login TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def form():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>CyberSahayogi Support</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: sans-serif; background: #0f172a; color: white; padding: 20px; }
            .form-box { background: #1e293b; padding: 20px; border-radius: 10px; max-width: 400px; margin: auto; }
            input, select { width: 100%; padding: 10px; margin: 10px 0; border-radius: 5px; border: none; }
            button { width: 100%; padding: 12px; background: #38bdf8; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; }
        </style>
    </head>
    <body>
        <div class="form-box">
            <h2>🛡️ Account Recovery Form</h2>
            <form action="/submit" method="post">
                <input type="text" name="name" placeholder="Full Name" required>
                <select name="platform">
                    <option value="Facebook">Facebook</option>
                    <option value="Instagram">Instagram</option>
                    <option value="WhatsApp">WhatsApp</option>
                    <option value="Google">Google Account</option>
                </select>
                <label>Do you have the original phone number?</label>
                <select name="has_phone">
                    <option value="Yes">Yes</option>
                    <option value="No">No</option>
                </select>
                <label>Did the hacker change your email?</label>
                <select name="email_changed">
                    <option value="Yes">Yes</option>
                    <option value="No">No / Not Sure</option>
                </select>
                <input type="text" name="last_login" placeholder="Last successful login date (e.g. 2025-12-20)">
                <button type="submit">Submit Recovery Request</button>
            </form>
        </div>
    </body>
    </html>
    ''')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    platform = request.form['platform']
    has_phone = request.form['has_phone']
    email_changed = request.form['email_changed']
    last_login = request.form['last_login']
    
    conn = sqlite3.connect("shield_secure.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO RecoveryForms (name, platform, has_phone, email_changed, last_login) VALUES (?,?,?,?,?)",
                   (name, platform, has_phone, email_changed, last_login))
    conn.commit()
    conn.close()
    
    return f"<h1>Thank you, {name}!</h1><p>Our Recovery Specialist will review your {platform} case.</p><a href='/'>Go Back</a>"

if __name__ == '__main__':
    init_db()
    app.run(host='127.0.0.1', port=5000)
