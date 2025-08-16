from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import mysql.connector
from werkzeug.utils import secure_filename
from logging_config import setup_logging
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

UPLOAD_FOLDER = '/data/uploads'  # volume mount path or container path
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# MySQL connection details
DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'mysql-db'), 
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', 'password'),
    'database': os.getenv('MYSQL_DATABASE', 'userdb')
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# NEW: Config route for frontend to get API URL dynamically
@app.route("/config", methods=["GET"])
def get_config():
    api_url = os.getenv("API_URL")
    if not api_url:
        logger.error("API_URL environment variable not set")
        return jsonify({"error": "API_URL not set"}), 500
    return jsonify({"API_URL": api_url})

@app.route('/api/upload', methods=['POST'])
def upload():
    logger.debug("Upload endpoint hit")
    name = request.form.get('name')
    email = request.form.get('email')
    resume = request.files.get('resume')

    if not all([name, email, resume]):
        logger.warning("Missing required fields in upload")
        return jsonify({'message': 'Missing required fields'}), 400

    filename = secure_filename(resume.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    resume.save(filepath)
    logger.debug(f"Saved file to {filepath}")

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
        logger.info(f"Inserted user {name} into database")
    except Exception as e:
        logger.error(f"Database error: {str(e)}", exc_info=True)
        return jsonify({'message': f'Database error: {str(e)}'}), 500

    return jsonify({'message': 'File uploaded and data saved successfully'})

@app.route('/api/users', methods=['GET'])
def get_users():
    logger.debug("Get users endpoint hit")
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, email, resume_path, created_at FROM users")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(users)
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}", exc_info=True)
        return jsonify({'message': f'Error fetching users: {str(e)}'}), 500

@app.route('/set-log-level', methods=['POST'])
def set_log_level():
    level = request.args.get('level', 'INFO').upper()
    try:
        new_level = getattr(logging, level)
        logging.getLogger().setLevel(new_level)
        logger.info(f"Log level changed to {level}")
        return jsonify({"message": f"Log level changed to {level}"}), 200
    except AttributeError:
        logger.error(f"Invalid log level attempt: {level}")
        return jsonify({"error": f"Invalid log level: {level}"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
