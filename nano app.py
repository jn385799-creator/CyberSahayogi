import sqlite3, csv, io
from flask import Flask, request, send_file

app = Flask(__name__)

# डाटाबेस तयार गर्ने
def init_db():
    conn = sqlite3.connect('shield_secure.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS victims 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, issue TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return '''
    <body style="font-family:Arial; text-align:center; padding:50px; background:#f0f2f5;">
        <div style="background:white; padding:30px; border-radius:15px; display:inline-block; box-shadow:0 4px 15px rgba(0,0,0,0.1);">
            <h2 style="color:#1a73e8;">CyberSahayogi Recovery</h2>
            <p>विवरण भर्नुहोस्, हामी मद्दत गर्नेछौँ।</p>
            <form action="/submit" method="POST">
                <input type="text" name="name" placeholder="पुरा नाम" required style="width:100%; padding:10px; margin:10px 0;"><br>
                <input type="text" name="phone" placeholder="WhatsApp नम्बर" required style="width:100%; padding:10px; margin:10px 0;"><br>
                <textarea name="issue" placeholder="तपाईँको समस्या के हो?" style="width:100%; padding:10px; margin:10px 0;"></textarea><br>
                <button type="submit" style="background:#28a745; color:white; border:none; padding:10px 25px; border-radius:5px; cursor:pointer;">मद्दत माग्नुहोस्</button>
            </form>
        </div>
    </body>
    '''

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    phone = request.form['phone']
    issue = request.form['issue']
    conn = sqlite3.connect('shield_secure.db')
    c = conn.cursor()
    c.execute("INSERT INTO victims (name, phone, issue) VALUES (?, ?, ?)", (name, phone, issue))
    conn.commit()
    conn.close()
    return "<h1 style='text-align:center; color:green;'>सफल भयो! हामी छिट्टै सम्पर्क गर्नेछौँ।</h1>"

@app.route('/admin')
def admin():
    conn = sqlite3.connect('shield_secure.db')
    c = conn.cursor()
    c.execute("SELECT * FROM victims")
    data = c.fetchall()
    conn.close()
    rows = ""
    for r in data:
        rows += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td><a href='https://wa.me/{r[2]}' style='color:green; text-decoration:none; font-weight:bold;'>Chat</a></td></tr>"
    
    return f'''
    <body style="font-family:sans-serif; padding:20px;">
        <h2>Admin Dashboard - CyberSahayogi</h2>
        <a href="/export" style="background:#1a73e8; color:white; padding:10px 15px; text-decoration:none; border-radius:5px;">Download CSV (Excel)</a>
        <table border="1" style="width:100%; margin-top:20px; border-collapse:collapse; text-align:left;">
            <tr style="background:#eee;"><th>ID</th><th>नाम</th><th>फोन नम्बर</th><th>समस्या</th><th>एक्सन</th></tr>
            {rows}
        </table>
    </body>
    '''

@app.route('/export')
def export():
    conn = sqlite3.connect('shield_secure.db')
    c = conn.cursor()
    c.execute("SELECT * FROM victims")
    data = c.fetchall()
    conn.close()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Name', 'Phone', 'Issue'])
    writer.writerows(data)
    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name='cybersahayogi_data.csv')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
