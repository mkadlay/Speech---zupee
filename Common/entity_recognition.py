import pandas as pd
import speech_translation
import string
import openai
import os
from dotenv import load_dotenv
import json
from zia_response import *

def load_api():
    load_dotenv()
    openai.api_key = os.environ.get("API_KEY")
    openai.api_base = os.environ.get("API_BASE")
    openai.api_type = os.environ.get("API_TYPE")
    openai.api_version = os.environ.get("API_VERSION")

# trans_text = "I want to complete my kyc"
# trans_text = "I want to play 2 player Ludo with 1 rs entry amount"
# trans_text = "I want to play Snakes and Ladder for 5 rs"

# trans_text = "play Ludo with entry amount of 3000 rupees with 2 players"
# trans_text = "I want to play 5 player ludo game"
# trans_text = "I want to play ludo game starting in half a minute"
# trans_text = "I want to play a quick Ludo game two players one winner entry amount twenty rupees in one minute"
trans_text = "I want to play Ludo's game"

def classify_intent(trans_text):
    load_api()
    response = openai.ChatCompletion.create(
        engine="MSZupeePoc", # The deployment name you chose when you deployed the GPT-3.5-Turbo or GPT-4 model.
        messages=[
            {"role": "system", "content": "Assistant is a large language model trained by OpenAI.\
            Identify the intent of the user - whether the user is trying to start a new game or do e-kyc\
            If the user's intention is to start a new game of Ludo then intent name is 'Start New Game'\
            The following are the rules, if the extracted values don't follow the rules, return null for the parameter\
            1. Never change THE JSON structure \
            2. Never give information not mentioned by the user \
            3. Accpeted value for number of players is 2 or 4, if a wrong value or none is entered return null\
            4. Accepted value for number of winners is upto 2 else set to null\
            5. Accepted value for entry amount is any positive number less than rupees 200000 for any other input return null\
            6. Accepted value for wait time should be upto 2 minutes else set to null\
            7. Winners, Type of tournament and tournament Wait Time are optional if not part of the first utterance by user, dont create a nextQ with these entities\
            8. Only when required entities like Players or EntryAmount or GameName are null create a prompt for nextQ\
            9. If the user is willing to start e-KYC set the intent name to 'Start e-KYC' and return other keys as null including nextQ\
            Output JSON Format:\
             {'Intent' : 'Intent',\
             'GameName' : 'Name of the game, required entity',\
             'Players' : 'Number of players, required entity',\
             'Winners':'Number of winner, it is an optional entity, dont add to nextQ',\
             'EntryAmount':'Entry Amount, required entity',\
             'Type':'Tournament type - is it regular or quick? If not defined return null, it is an optional entity, dont add to nextQ',\
             'WaitTime':'Preferred wait time for the game. Convert value to seconds, it is an optional entity, dont add to nextQ',\
             'nextQ':'Prompt that starts with please provide and include names of only the missing entities that are mentioned as required entities , ignore the optional entities.'\
             'error':'Only when an entity value is set to null by the Assisstant please share reason for all the entities here'\
             }"},
            {"role": "user", "content": f"What is the intent for the following utterance -{trans_text}.\
            Return an json object with curly braces of without any extra word or signs"}])
    intent = response['choices'][0]['message']['content']
    # print(intent)
    return intent

def extract_information(text_with_json):
    text_with_json = text_with_json.replace("'", '"')
    start_index = text_with_json.find('{')  # Find the starting index of JSON data
    end_index = text_with_json.rfind('}')   # Find the ending index of JSON data

    # Print keys and corresponding values

    if start_index != -1 and end_index != -1:
        json_data = text_with_json[start_index:end_index+1]# Extract JSON data
        try:
            parsed_data = json.loads(json_data)
            keys = parsed_data.keys()
            for key in keys:
                value = parsed_data[key]
        except json.JSONDecodeError as e:
            print("Error parsing JSON:", e)
    else:
        print("No JSON data found in the text.")

    return json_data

text_with_json = classify_intent(trans_text)

output = extract_information(text_with_json)
print(output)

api_text = "\
{            'Intent' : 'Intent',\
             'GameName' : 'Ludo',\
             'Players' : null,\
             '# winner':'2',\
             'Entry Amount':null,\
             'Type':'quick',\
             'Wait time': '2'\
             }\
"
api_text = extract_information(api_text)

def find_null_keys(json_obj):
    null_keys = []
    data = json.loads(json_obj)
    for key, value in data.items():
        if value is None:
            null_keys.append(key)
    return null_keys

# Replace sample_json with your actual JSON object or provide the path to a JSON file
null_keys = find_null_keys(api_text)

# if null_keys:
#     print(f"The following keys have null values: {', '.join(null_keys)}")
# else:
#     print("No keys with null values found.")
    
if null_keys:
    text_to_zia = f"Please provide your preferred: {', '.join(null_keys)}"
    reponse_from_zia(text_to_zia)

res_text = "2 players 1.5 rs"

def clasiify_response(trans_text):
    load_api()
    response = openai.ChatCompletion.create(
        engine="MSZupeePoc", # The deployment name you chose when you deployed the GPT-3.5-Turbo or GPT-4 model.
        messages=[
            {"role": "system", "content": "Assistant is a large language model trained by OpenAI.\
            Please provide a JSON structure that identifies a gamer's intent to play Ludo \
            Intent Name: 'Start New Ludo Game'\
            The following are the rules, if the extracted values don't follow the rules retun null for the parameter\
            1. Number of players can either be 2 or 4\
            Output JSON Format:\
             {'Intent' : 'Intent',\
             'GameName' : 'Name of the game',\
             '# Players' : 'Number of players',\
             '# winner':'Number of winner.',\
             'Entry Amount':'Entry Amount',\
             'Type':'Tournament type - is it regular or quick? If not defined return null',\
             'Wait time':'Preferred wait time for the game'\
             }"},
            {"role": "user", "content": f"What is the intent for the following utterance -{trans_text}.\
            Return an json object with curly braces of without any extra word or signs"}
        ])
    intent = response['choices'][0]['message']['content']
    # print(intent)
    return intent

text_with_json = classify_intent(res_text)

output = extract_information(text_with_json)
print(output)




