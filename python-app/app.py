from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import mysql.connector
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

UPLOAD_FOLDER = '/data/uploads'  # outside container? or volume mount path
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# MySQL connection details (set env variables or hardcode for now)
DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'mysql-db'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', 'password'),
    'database': os.getenv('MYSQL_DATABASE', 'userdb')
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/api/upload', methods=['POST'])
def upload():
    name = request.form.get('name')
    email = request.form.get('email')
    resume = request.files.get('resume')

    if not all([name, email, resume]):
        return jsonify({'message': 'Missing required fields'}), 400

    filename = secure_filename(resume.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    resume.save(filepath)

    # Save to MySQL
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, resume_path) VALUES (%s, %s, %s)",
            (name, email, filepath)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        return jsonify({'message': f'Database error: {str(e)}'}), 500

    return jsonify({'message': 'File uploaded and data saved successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
