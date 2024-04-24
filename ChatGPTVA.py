# Python program to translate speech to text and text to speech

# Importing necessary libraries
import speech_recognition as sr  # For speech recognition
import pyttsx3  # For text to speech conversion

# Importing OS library and dotenv to handle environment variables
import os
from dotenv import load_dotenv

# Loading environment variables from the .env file
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')  # Retrieve the OpenAI API key

# Importing OpenAI library and setting the API key
import openai
openai.api_key = OPENAI_KEY

# Function to convert text to speech
def SpeakText(command):
    """
    Function to speak out the given text using the text-to-speech engine.
    Args:
    command (str): Text that needs to be spoken.
    """
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
    engine.say(command)  # Pass the text to be spoken
    engine.runAndWait()  # Process and play the audio

# Initialize the recognizer for speech recognition
r = sr.Recognizer()

def record_text():
    """
    Function to record speech from the microphone and convert it to text.
    Returns:
    str: Recognized text from speech.
    """
    while True:  # Infinite loop to continuously listen to speech
        try:
            # Use the default microphone as the audio source
            with sr.Microphone() as source2:
                # Adjust the recognizer sensitivity to ambient noise
                r.adjust_for_ambient_noise(source2, duration=0.2)

                print("I'm listening")  # Inform user that the system is ready to listen

                # Listen for the user's speech
                audio2 = r.listen(source2)

                # Use Google's speech recognition
                MyText = r.recognize_google(audio2)
                return MyText  # Return the recognized text

        except sr.RequestError as e:
            # Handle cases where the recognizer could not request results
            print(f"Could not request results; {e}")

        except sr.UnknownValueError:
            # Handle cases where the recognizer could not understand the speech
            print("unknown error occurred")

def send_to_chatGPT(messages, model="gpt-3.5-turbo"):
    """
    Function to send messages to the OpenAI API and get a response.
    Args:
    messages (list): List of previous interactions/messages.
    model (str): Specifies which GPT model to use.

    Returns:
    str: Response from GPT model.
    """
    # Send the messages to the OpenAI API for processing
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Extract the response message
    message = response.choices[0].message.content
    messages.append(response.choices[0].message)  # Append the response to messages
    return message

# Starting conversation with a predefined message
messages = [{"role": "user", "content": "Please act like Jarvis from Iron man. From now on your name is Jarvis"}]

# Main loop to keep the program running
while True:
    text = record_text()  # Record and convert speech to text
    messages.append({"role": "user", "content": text})  # Append the new text to messages
    response = send_to_chatGPT(messages)  # Get response from OpenAI GPT
    SpeakText(response)  # Speak out the response

    print(response)  # Print the response
