#!/usr/bin/env python3

"""
Code written by Mattias Kockum
On 02/10/2023
The aim of this program is to let my blind grand father use chat GPT
"""

import os
import subprocess
import json
import speech_recognition as sr
import yaml

from AssistantVocal.GPT_api import *
from AssistantVocal.TTS_api import *

### INIT

config_dir = "config"
vocal_dir = "vocals"

if not os.path.exists(vocal_dir):
    os.makedirs(vocal_dir)

with open(f"{config_dir}/config.yaml", 'r') as file:
    config = yaml.safe_load(file)

with open(f"{config_dir}/gpt_config.yaml", 'r') as file:
    gpt_config = yaml.safe_load(file)


figlet_greetings = config["figlet_greetings"]

LANG = config["LANG"]
preprompt = config[LANG]["preprompt"]
languages_recognizer = config[LANG]["languages_recognizer"]
languages_tts = config[LANG]["languages_tts"]

# Reading api keys
with open("credentials/keys.json", 'r') as f:
    keys = json.load(f)

recognizer = sr.Recognizer()

Tts_api = TTS_API("credentials/credentials.json")
Gpt_api = GPT_API(
        keys["GPT"],
        model_name=gpt_config["model_name"],
        temperature=gpt_config["temperature"],
        max_tokens=gpt_config["max_tokens"],
        top_p=gpt_config["top_p"],
        frequency_penalty=gpt_config["frequency_penalty"],
        presence_penalty=gpt_config["presence_penalty"]
)
Chatbot = ChatBot(
        Gpt_api,
        preprompt=preprompt,
)


def reset_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(figlet_greetings)
    print(Chatbot.get_chat_history())


### MAIN FUNCTION

def chat_iteration():
    # Voice input
    #with sr.Microphone(sample_rate=14000) as source:
    with sr.Microphone() as source:
        reset_screen()
        print("\nJe vous écoute...")
        audio = recognizer.listen(source)

    # Speech to Text
    input_audio_text = "[Mauvais son, demandez moi de recommencer]"
    try:
        input_audio_text = recognizer.recognize_google(
                audio,
                language=languages_recognizer)
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
    except sr.RequestError as e:
        print(f"Request error: {e}")
    
    reset_screen()

    # Text to Text (GPT)
    chatbot_response = Chatbot.chat(input_audio_text)

    # Text to Speech
    output_file_wav = Tts_api.text_to_wav(
            languages_tts,
            chatbot_response,
            folder="vocals"
    )

    reset_screen()

    # Voice output
    with open(os.devnull, 'wb') as devnull:
        subprocess.check_call(
            ["aplay", output_file_wav],
            stdout=devnull, stderr=subprocess.STDOUT)


### LOOP

while True:
    chat_iteration()

