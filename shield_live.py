from flask import Flask, render_template_string, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_FILE = "shield_secure.db"

def get_stats():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM SecureUsers")
        total = cursor.fetchone()[0]
        conn.close()
        file_size = os.path.getsize(DB_FILE) / (1024 * 1024)
        return total, round(file_size, 2)
    except:
        return 0, 0

@app.route('/api/stats')
def stats():
    total, size = get_stats()
    return jsonify({"total": total, "size": size})

@app.route('/')
def dashboard():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Shield Live Monitor</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: 'Segoe UI', sans-serif; background: #020617; color: #f8fafc; text-align: center; padding: 20px; }
            .container { max-width: 500px; margin: auto; }
            .card { background: #1e293b; border-left: 5px solid #38bdf8; border-radius: 10px; padding: 20px; margin: 15px 0; transition: 0.3s; }
            h1 { color: #38bdf8; text-shadow: 0 0 10px rgba(56, 189, 248, 0.5); }
            .stat { font-size: 3em; font-weight: bold; color: #4ade80; }
            .pulse { width: 10px; height: 10px; background: #ef4444; border-radius: 50%; display: inline-block; animation: blink 1s infinite; }
            @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
        </style>
        <script>
            async function updateStats() {
                const response = await fetch('/api/stats');
                const data = await response.json();
                document.getElementById('total').innerText = data.total.toLocaleString();
                document.getElementById('size').innerText = data.size + " MB";
            }
            setInterval(updateStats, 2000); // हरेक २ सेकेन्डमा अपडेट गर्ने
        </script>
    </head>
    <body>
        <div class="container">
            <h1>🛡️ SHIELD LIVE <span class="pulse"></span></h1>
            <div class="card">
                <div style="font-size: 0.8em; color: #94a3b8;">LIVE USER COUNT</div>
                <div class="stat" id="total">Loading...</div>
            </div>
            <div class="card">
                <div style="font-size: 0.8em; color: #94a3b8;">DATABASE STORAGE</div>
                <div class="stat" id="size" style="color: #fbbf24;">0 MB</div>
            </div>
            <p style="color: #475569;">System Encrypted: AES-256-GCM</p>
        </div>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
