from flask import Flask, request, jsonify, render_template
import boto3
from botocore.exceptions import ClientError
from flask_socketio import SocketIO
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
socketio = SocketIO(app)

# S3 configuration
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')  # Ensure you have this environment variable set
s3 = boto3.client('s3')

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# File upload route
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Upload file to S3
    try:
        s3.upload_fileobj(file, S3_BUCKET_NAME, file.filename)
        return jsonify({"message": "File uploaded successfully"}), 200
    except ClientError as e:
        return jsonify({"error": str(e)}), 500

@socketio.on('connect')
def handle_connect():
    print("Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8080)