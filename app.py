from flask import Flask, render_template, url_for, request, jsonify
import pathlib
from pathlib import Path
import textwrap
import os
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

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/aboutfuture")
def showfuture():
    return render_template("future.html")

@app.route("/testchat")
def showchat():
    return render_template("chat.html")

@app.route("/demo")
def demo():
    response=gem.generate_content("in 1000 words 4 paragraphs describe quantum mechanics.")
    response.text
    return response.text

@app.route('/process', methods=['POST'])
def process_message():
    data = request.get_json()
    user_message = data.get('message')

    # Process the user's message (you can add your logic here)
    # For now, let's just return a simple response
    response=gem.generate_content(user_message)
    bot_response = response.text
    print(bot_response)
    # Return the bot's response as JSON
    return jsonify({'message': bot_response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)