import pandas as pd
import speech_translation
import string
import openai
import os
from dotenv import load_dotenv
import json

def load_api():
    load_dotenv()
    openai.api_key = os.environ.get("API_KEY")
    openai.api_base = os.environ.get("API_BASE")
    openai.api_type = os.environ.get("API_TYPE")
    openai.api_version = os.environ.get("API_VERSION")

# trans_text = speech_translation.recognize_from_microphone()

# trans_text = "Recharge wallet with 50 rs"
# trans_text = "I want to play a game of Ludo with 2 players"

def classify_intent(trans_text):
    load_api()
    response = openai.ChatCompletion.create(
        engine="gptForAds", # The deployment name you chose when you deployed the GPT-3.5-Turbo or GPT-4 model.
        messages=[
            {"role": "system", "content": "Assistant is a large language model trained by OpenAI.\
            Please provide a JSON response that identifies a gamer's intent to load or recharge their wallet \
            Intent Name: 'Load Money'\
            JSON Format:\
             {'Intent' : [Intent Name],\
             'Amount': [Amount] ,\
             'Curreny' : [Currency]\
             }\
            Please provide a JSON response that identifies a gamer's intent to start a new game\
            Intent Name: 'Start New Game'\
            JSON Format:\
             {'Intent' : [Name of the game],\
             '# Players' : [Number of players]\
             }"},
            {"role": "user", "content": f"What is the intent for the following utterance -{trans_text}"}
        ])
    intent = response['choices'][0]['message']['content']
    # print(intent)
    return intent

def extract_information(trans_text):

    text_with_json = classify_intent(trans_text)

    text_with_json = text_with_json.replace("'", '"')

    start_index = text_with_json.find('{')  # Find the starting index of JSON data
    end_index = text_with_json.rfind('}')   # Find the ending index of JSON data

    # Print keys and corresponding values

    if start_index != -1 and end_index != -1:
        json_data = text_with_json[start_index:end_index+1]  # Extract JSON data
        # Parse JSON
        try:
            parsed_data = json.loads(json_data)

            # Extract keys
            keys = parsed_data.keys()
            # Extract information
            for key in keys:
                value = parsed_data[key]
                print(f"Key: {key}, Value: {value}")
        except json.JSONDecodeError as e:
            print("Error parsing JSON:", e)
    else:
        print("No JSON data found in the text.")

    return json_data

output = extract_information(trans_text)
# print(output)