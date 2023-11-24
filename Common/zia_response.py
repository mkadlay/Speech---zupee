import os
import azure.cognitiveservices.speech as speechsdk
import openai
from dotenv import load_dotenv

def load_api():
    load_dotenv()
    openai.api_key = os.environ.get("API_KEY")
    openai.api_base = os.environ.get("API_BASE")
    openai.api_type = os.environ.get("API_TYPE")
    openai.api_version = os.environ.get("API_VERSION")

# input_text = "Please provide your preferred: Players, # winner, Entry Amount"

def reponse_from_zia(input_text):
    load_api()
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    response = openai.ChatCompletion.create(
    model="text-davinci-003",
    engine = "MSZupeePoc",
    messages=[
        {"role": "system", "content": "Translate the following text from English to Hindi. Keep certain english words in english"},
        {"role": "user", "content": input_text}
    ],
    max_tokens=100  # You can adjust the max_tokens as per your requirement
    )

    # Extracting the translated text from the API response
    translated_text = response['choices'][0]['message']['content']

    print(f"Translated text to Hindi: {translated_text}")

    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name='hi-IN-SwaraNeural'

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # Get text from the console and synthesize to the default speaker.

    speech_synthesis_result = speech_synthesizer.speak_text_async(translated_text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(translated_text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

