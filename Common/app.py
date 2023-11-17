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
    openai.api_version = os.environ.get("API_VERSION")
    return ("Loaded API Creds")

app = Flask(__name__)

# @app.route('/capture_intent', methods=['GET'])
# def capture_intent():
#     load_api()
#     # trans_text = request.args.get('text') 
#     # text_to_translate = data.get('text', '')
#     output = extract_information(request.args.get('text'))

#     return output

@app.route('/translate', methods=['GET'])
def translate():
    try:
        text_to_translate = request.args.get('text')  # Get 'text' from the query parameters

        if not text_to_translate:
            return jsonify({'error': 'No text to translate provided'})

        # Use the extract_information function for translation
        translated_text = extract_information(text_to_translate)

        return ({'translated_text': translated_text})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    # trans_text = "I want to play a game of Ludo with 2 players"
    app.run(debug=True)  # Run the Flask app
