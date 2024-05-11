from flask import Flask, render_template, url_for, request, jsonify, redirect, session
import pathlib
from pathlib import Path
import textwrap
import os
import json
import secrets
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
from dotenv import load_dotenv
from flask_cors import CORS
load_dotenv()

genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

#model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
#                              generation_config=generation_config,
#                              safety_settings=safety_settings)
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

gem=model

def to_markdown(text):
  text = text.replace('•', ' *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

app = Flask(__name__)
CORS(app)
app.secret_key = secrets.token_hex(16)

try:
    with open('userbase.json', 'r') as file:
        userbase = json.load(file)
except FileNotFoundError:
    userbase = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/aboutfuture")
def showfuture():
    return render_template("future.html")

@app.route("/testchat")
def showchat():
    if 'logged_in' in session and session['logged_in'] == True:
      return render_template("chat.html")
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session and session['logged_in'] == True:
        return redirect(url_for('showchat'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for user in userbase:
            if user['username']==username:
                if user['password']==password:
                    session['logged_in'] = True
                    session['username'] = username
                    return redirect(url_for('showchat'))
        else:
            return render_template('failed_login.html')
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for user in userbase:
            if user['username']==username:
                if user['password']==password:
                    session['logged_in'] = True
                    return render_template('failed_signup.html')
        else:
            newuser = {
            'username': username,
            'password': password,
            'chat': []
            }
            userbase.append(newuser)
            return render_template('passed_signup.html')
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


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

@app.route("/showuser")
def showserver():
    return jsonify(userbase)

# Save userbase to a file before shutting down the server
@app.before_request
def save_userbase():
    with open('userbase.json', 'w') as file:
        json.dump(userbase, file)


@app.route("/demo")
def demo():
    response=gem.generate_content("in 1000 words 4 paragraphs describe quantum mechanics.")
    response.text
    return response.text

@app.route('/process', methods=['POST'])
def process_message():
    if 'username' not in session:
        return 'Unauthorized', 401
    data = request.get_json()
    user_message = data.get('message')
    username = session['username']
    for user in userbase:
        if username==user['username']:
            user['chat'].append(user_message)
    # Process the user's message (you can add your logic here)
    # For now, let's just return a simple response
    prompt=""
    for i in user['chat']:
        prompt=prompt+"\n"+i
    response=gem.generate_content(prompt)
    bot_response = response.text
    user['chat'].append(bot_response)
    print(bot_response)
    # Return the bot's response as JSON
    return jsonify({'message': bot_response})

@app.route('/get_previous_messages')
def get_previous_messages():
    if 'username' not in session:
        return 'Unauthorized', 401
    username = session['username']
    for user in userbase:
        if username==user['username']:
            return jsonify(user['chat'])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)