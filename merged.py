#this code merges both ChatGPTVA and speech_to_text
#thought it would be nice to have options


import speech_recognition as sr
import pyttsx3
import os
from dotenv import load_dotenv
import openai

# Load environment variables and set OpenAI key
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')
openai.api_key = OPENAI_KEY

# Initialize the text-to-speech and speech recognition engines
engine = pyttsx3.init()
recognizer = sr.Recognizer()

def speak_text(text):
    """
    Converts given text to speech.
    Args:
        text (str): Text to be spoken.
    """
    engine.say(text)
    engine.runAndWait()

def record_text():
    """
    Listens to the microphone, recognizes speech, and converts it to text.
    Returns:
        str: Text converted from spoken words.
    """
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.2)
                audio = recognizer.listen(source)
                recognized_text = recognizer.recognize_google(audio)
                return recognized_text
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except sr.UnknownValueError:
            print("unknown error occurred")

def send_to_chatGPT(messages, model="gpt-3.5-turbo"):
    """
    Sends messages to OpenAI GPT and receives a response.
    Args:
        messages (list): List of previous interactions/messages.
        model (str): Specifies which GPT model to use.
    Returns:
        str: Response from GPT model.
    """
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=150
    )
    message = response.choices[0].message.content
    messages.append({"role": "system", "content": message})
    return message

def output_text(text):
    """
    Writes the provided text to a file.
    Args:
        text (str): Text to write.
    """
    with open("output.txt", "a") as f:
        f.write(text + "\n")

# Main loop
messages = []
while True:
    user_text = record_text()
    messages.append({"role": "user", "content": user_text})
    response = send_to_chatGPT(messages)
    speak_text(response)
    output_text("User: " + user_text)
    output_text("Jarvis: " + response)
    print("Response: " + response)
