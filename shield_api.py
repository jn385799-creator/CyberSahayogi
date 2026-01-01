from flask import Flask, request, jsonify
import sqlite3
import bcrypt
import jwt
import datetime

app = Flask(__name__)
DB_FILE = "shield_cloud.db"
SECRET_KEY = "shield_auth_api_secret"

# १. लगइन चेक गर्ने फङ्सन
def verify_user(email, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM Users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')):
        return True
    return False

# २. API Route: लगइनको लागि
@app.route('/login', methods=['POST'])
def login_api():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if verify_user(email, password):
        token = jwt.encode({
            'user': email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, SECRET_KEY, algorithm='HS256')
        return jsonify({"status": "success", "token": token})
    else:
        return jsonify({"status": "error", "message": "Invalid Credentials"}), 401

if __name__ == '__main__':
    print("🚀 Shield API Server सुरु हुँदैछ...")
    app.run(host='0.0.0.0', port=5000)
