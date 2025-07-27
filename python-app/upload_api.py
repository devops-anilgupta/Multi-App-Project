from flask import Flask, request, jsonify
import os
import mysql.connector
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = '/app/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    name = request.form.get('name')
    email = request.form.get('email')
    resume = request.files.get('resume')

    if not (name and email and resume):
        return jsonify({'message': 'All fields are required'}), 400

    filename = secure_filename(resume.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    resume.save(filepath)

    # Save to MySQL
    conn = mysql.connector.connect(
        host='mysql',
        user='root',
        password='root',
        database='mydb'
    )
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, resume_path) VALUES (%s, %s, %s)",
        (name, email, filepath)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'File uploaded successfully'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
