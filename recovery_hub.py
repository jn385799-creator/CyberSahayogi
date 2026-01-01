from flask import Flask, render_template_string, jsonify
import sqlite3

app = Flask(__name__)

def get_recovery_stats():
    conn = sqlite3.connect("shield_secure.db")
    cursor = conn.cursor()
    # नयाँ रिकभरी टेबल बनाउने
    cursor.execute('''CREATE TABLE IF NOT EXISTS RecoveryCases 
                     (id INTEGER PRIMARY KEY, name TEXT, platform TEXT, status TEXT)''')
    cursor.execute("SELECT count(*) FROM RecoveryCases")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT count(*) FROM RecoveryCases WHERE status='Recovered'")
    recovered = cursor.fetchone()[0]
    conn.close()
    return total, recovered

@app.route('/')
def dashboard():
    total, recovered = get_recovery_stats()
    html = f'''
    <html>
    <head>
        <title>Shield Recovery Hub</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background: #0f172a; color: white; padding: 20px; }}
            .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
            .card {{ background: #1e293b; padding: 20px; border-radius: 10px; border-top: 4px solid #38bdf8; }}
            .success {{ border-top: 4px solid #4ade80; }}
            h1 {{ color: #38bdf8; text-align: center; }}
            .guide {{ background: #334155; padding: 10px; border-radius: 5px; margin-top: 10px; font-size: 0.9em; }}
        </style>
    </head>
    <body>
        <h1>🛡️ CYBERSAHAYOGI HUB</h1>
        <div class="grid">
            <div class="card">
                <div style="font-size: 0.8em; color: #94a3b8;">ACTIVE CASES</div>
                <div style="font-size: 2.5em; font-weight: bold;">{total}</div>
            </div>
            <div class="card success">
                <div style="font-size: 0.8em; color: #94a3b8;">ACCOUNTS RECOVERED</div>
                <div style="font-size: 2.5em; font-weight: bold; color: #4ade80;">{recovered}</div>
            </div>
        </div>
        
        <h3>🚀 Platform Recovery Guides</h3>
        <div class="guide">
            <b>Facebook:</b> facebook.com/hacked<br>
            <b>Instagram:</b> instagram.com/hacked<br>
            <b>Google:</b> accounts.google.com/signin/recovery
        </div>
        <p style="text-align: center; color: #64748b; margin-top: 30px;">
            Helping people reclaim their digital lives.
        </p>
    </body>
    </html>
    '''
    return render_template_string(html)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
