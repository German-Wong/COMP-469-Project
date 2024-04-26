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
def SpeakText(command, lang = "usenglishf"):
    """
    Function to speak out the given text using the text-to-speech engine.
    Args:
    command (str): Text that needs to be spoken.
    gender (str): Gender of the voice ("male" or "female").
    """
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    voices = engine.getProperty('voices')
    for voice in voices:
        print(voice.name)

    # Set the gender of the voice when initializing the engine
    if lang == "usenglishf":
        engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
    elif lang == "usenglishm":
        engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0')    
    elif lang == "gbenglish":
        engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0')
    elif lang == "esspanish":
        engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0')
    elif lang == "mxspanish":
        engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0')
    

    engine.say(command)  # Pass the text to be spoken
    engine.runAndWait()  # Process and play the audio


# Initialize the recognizer for speech recognition
r = sr.Recognizer()

def record_text(stop_phrases=["Thanks ARIA", "Goodbye", "See you", "Bye", "You're dismissed", "That's enough", "Exit", "Quit"]):
    """
    Function to record speech from the microphone and convert it to text.
    Returns:
    str: Recognized text from speech.
    """
    while(1):  # Infinite loop to continuously listen to speech
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
            
                # Check if any of the stop phrases are detected
                for phrase in stop_phrases:
                    if phrase.lower() in MyText.lower():
                        print(f"Stopping listening. Detected stop phrase: {phrase}")
                        return None  # Return None to indicate stopping

                return MyText  # Return the recognized text

        except sr.RequestError as e:
            # Handle cases where the recognizer could not request results
            print(f"Could not request results; {e}")

        except sr.UnknownValueError:
            # Handle cases where the recognizer could not understand the speech
            print("unknown error occurred")
            break

def send_to_chatGPT(messages, model="gpt-3.5-turbo"):
    """
    Function to send messages to the OpenAI API and get a response.
    Args:
        messages (list): List of previous interactions/messages.
        model (str): Specifies which GPT model to use.
    Returns:
        str: Response from GPT model.
    """
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].message.content
    messages.append(response.choices[0].message)
    return message

messages = []
while(1):
    text = record_text()
    if text is None:
        SpeakText("Goodbye now.", lang = "usenglishm")
    messages.append({"role": "user", "content": text})
    print(text)
    response = send_to_chatGPT(messages)
    print(response)
    SpeakText(response, lang = "usenglishf")
    

    
