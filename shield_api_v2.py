from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sqlite3
import bcrypt

app = Flask(__name__)

# रेट लिमिटर सेटअप: १ मिनेटमा ५ पटक मात्र प्रयास गर्न मिल्ने
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute") # सुरक्षा थपियो
def login():
    # लगइन कोड यहाँ...
    return jsonify({"status": "secure_access_active"})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
