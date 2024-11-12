from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO
import boto3
import os

app = Flask(__name__)




if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')
    