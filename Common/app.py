from flask import Flask, request, jsonify
import openai
import pandas as pd
import speech_translation
import string
import os
from dotenv import load_dotenv
import json
from entity_recognition import *
from speech_translation import *

trans_text = "I want to play a game of Ludo with 2 players"

def load_api():
    load_dotenv()
    openai.api_key = os.environ.get("API_KEY")
    openai.api_base = os.environ.get("API_BASE")
    openai.api_type = os.environ.get("API_TYPE")
    openai.api_version = os.environ.get("API_VERSION"

app1 = Flask(__name__)

@app1.route('/capture_intent', methods=['POST'])
def capture_intent(trans_text):
    load_api()
    output = extract_information(trans_text)

    return output

if __name__ == '__main__':
    app1.run(debug=True)  # Run the Flask app
