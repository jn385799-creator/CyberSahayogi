from flask import Flask, render_template_string
import sqlite3
import os

app = Flask(__name__)

def get_stats():
    conn = sqlite3.connect("shield_secure.db")
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM SecureUsers")
    total = cursor.fetchone()[0]
    conn.close()
    
    file_size = os.path.getsize("shield_secure.db") / (1024 * 1024) # MB मा
    return total, round(file_size, 2)

@app.route('/')
def dashboard():
    total_users, db_size = get_stats()
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Shield Cloud Dashboard</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: sans-serif; background: #0f172a; color: white; text-align: center; padding: 20px; }}
            .card {{ background: #1e293b; border-radius: 15px; padding: 20px; margin: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }}
            h1 {{ color: #38bdf8; }}
            .stat {{ font-size: 2.5em; font-weight: bold; color: #4ade80; }}
            .label {{ color: #94a3b8; text-transform: uppercase; font-size: 0.8em; letter-spacing: 1px; }}
        </style>
    </head>
    <body>
        <h1>🛡️ SHIELD CLOUD CONTROL</h1>
        <div class="card">
            <div class="label">Total Reach (Users)</div>
            <div class="stat">{total_users:,}</div>
        </div>
        <div class="card">
            <div class="label">Database Storage Used</div>
            <div class="stat">{db_size} MB</div>
        </div>
        <div class="card">
            <div class="label">Security Level</div>
            <div class="stat" style="color: #fbbf24;">AES-256 + Bcrypt</div>
        </div>
        <p style="color: #64748b;">Status: Server is Running on Termux</p>
    </body>
    </html>
    '''
    return render_template_string(html)

if __name__ == '__main__':
    print("🚀 ड्यासबोर्ड सुरु भयो! http://127.0.0.1:8080 मा हेर्नुहोस्")
    app.run(host='127.0.0.1', port=8080)
