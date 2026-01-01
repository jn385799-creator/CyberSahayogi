import os
from flask import Flask, request, render_template_string
from cryptography.fernet import Fernet

app = Flask(__name__)
UPLOAD_FOLDER = 'encrypted_vault'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# मास्टर की लोड गर्ने (पहिलेकै key प्रयोग गर्ने)
KEY_FILE = "master.key"
if not os.path.exists(KEY_FILE):
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f: f.write(key)
else:
    key = open(KEY_FILE, "rb").read()

cipher = Fernet(key)

@app.route('/')
def upload_page():
    return '''
    <html>
    <body style="background:#0f172a; color:white; font-family:sans-serif; text-align:center; padding:50px;">
        <h2>🛡️ Secure Identity Vault</h2>
        <p>Upload ID Document (Citizenship/Passport) for Verification</p>
        <form action="/upload" method="post" enctype="multipart/form-data" style="background:#1e293b; padding:20px; border-radius:10px; display:inline-block;">
            <input type="file" name="doc" required><br><br>
            <button type="submit" style="background:#38bdf8; padding:10px 20px; border:none; border-radius:5px; font-weight:bold;">Encrypt & Upload</button>
        </form>
    </body>
    </html>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['doc']
    if file:
        file_data = file.read()
        # फाइललाई इन्क्रिप्ट गर्ने
        encrypted_data = cipher.encrypt(file_data)
        
        # सुरक्षित नाममा सेभ गर्ने
        secure_name = f"enc_{file.filename}.shield"
        with open(os.path.join(UPLOAD_FOLDER, secure_name), "wb") as f:
            f.write(encrypted_data)
            
        return f"<h1>✅ Document Secured!</h1><p>File saved as: {secure_name}</p><a href='/'>Back</a>"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9000)
