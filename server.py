from flask import Flask, render_template, url_for, request, jsonify
import pathlib
from pathlib import Path
import os
import json
import requests
from dotenv import load_dotenv
from flask_cors import CORS
load_dotenv()


app = Flask(__name__)
CORS(app)

# Load existing userbase from a file
try:
    with open('userbase.json', 'r') as file:
        userbase = json.load(file)
except FileNotFoundError:
    userbase = []

@app.route('/alive')
def beep():
    return jsonify(), 200

@app.route('/add_user')
def add_user():
    username = request.args.get('username')
    password = request.args.get('password')
    
    if not username or not password:
        return 'Username and password are required.', 400

    newuser = {
        'username': username,
        'password': password,
        'chat': []
    }
    userbase.append(newuser)
    return jsonify()

@app.route("/find_user")
def find():
    username = request.args.get('username')
    password = request.args.get('password')

    for user in userbase:
        if username==user['username']:
            if password==user['password']:
                return jsonify(True)
            
    return jsonify(False)

@app.route('/add_conversation')
def add_conversation():
    username = request.args.get('username')
    password = request.args.get('password')
    conversation = request.args.get('conversation')

    for user in userbase:
        if username==user['username']:
            if password==user['password']:
                chat={'conversation':conversation,
                      'chats':[]}
                user['chat'].append(chat)
                return jsonify(True)
            
    return jsonify(False)

@app.route('/add_conversation_new')
def add_conversation_new():
    username = request.args.get('username')
    password = request.args.get('password')
    conversation = request.args.get('conversation')

    response = requests.get(request.url + '/find_user', params={'username': username, 'password': password})
    if response.json():
        # Perform your task here
        tempuser['chat'].append(conversation)
        return 'Task performed successfully.'
    else:
        return 'User not found or incorrect password.'

@app.route("/showuser")
def showserver():
    return jsonify(userbase)

# Save userbase to a file before shutting down the server
@app.before_request
def save_userbase():
    with open('userbase.json', 'w') as file:
        json.dump(userbase, file)

if __name__ == '__main__':
    app.run(debug=True, port=8080)