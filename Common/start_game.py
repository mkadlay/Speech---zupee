import os
import json
import string
import openai
import pandas as pd
from dotenv import load_dotenv
from speech_translation import *
from zia_response import *
from entity_recognition import *

def load_api():
    load_dotenv()
    openai.api_key = os.environ.get("API_KEY")
    openai.api_base = os.environ.get("API_BASE")
    openai.api_type = os.environ.get("API_TYPE")
    openai.api_version = os.environ.get("API_VERSION")

print("Hello. Which game do you want to play today? Speak into your microphone.")
trans_text = recognize_from_microphone()
text_with_json = classify_intent(trans_text)
output = extract_information(text_with_json)

print(output)

null_keys = find_null_keys(output)
if null_keys:
    myjson= json.loads(output)
    text_to_zia = myjson['nextQ']
    if text_to_zia:
        reponse_from_zia(text_to_zia)
        trans_text2 = recognize_from_microphone()
        text_with_json = classify_intent(trans_text+trans_text2)
        output = extract_information(text_with_json)
        print(output)
    else:
        print("Try another prompt")





