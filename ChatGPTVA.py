import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import speech_recognition as sr
import pyttsx3
import openai
from dotenv import load_dotenv
import threading

# Load environment variables
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')
openai.api_key = OPENAI_KEY

# Global variable to store selected voice path
selected_voice_path = None

class AnimatedGIFViewer:
    def __init__(self, master, gif_folder):
        self.master = master
        self.gif_folder = gif_folder
        self.images = []
        self.current_frame = 0
        self.stop_listening = False
        self.thread = None

        # Load GIF images from folder
        self.load_images()

        # Display the first frame
        self.display_frame()

        # Start listening for speech when the GIF is clicked
        self.image_label.bind("<Button-1>", self.start_listening)

    def load_images(self):
        # Load GIF images from folder
        for filename in sorted(os.listdir(self.gif_folder)):
            if filename.endswith(".png"):  
                image = Image.open(os.path.join(self.gif_folder, filename))
                self.images.append(ImageTk.PhotoImage(image))

    def display_frame(self):
        # Display current frame
        if self.images:
            self.image_label = tk.Label(self.master, image=self.images[self.current_frame])
            self.image_label.pack()

    def update_frame(self):
        # Update to the next frame
        self.current_frame = (self.current_frame + 1) % len(self.images)
        self.image_label.configure(image=self.images[self.current_frame])
        self.master.after(20, self.update_frame)  # Change delay as needed

    def start_listening(self, event):
        # Initialize an empty list to store the conversation history
        self.messages = []

        # Start listening for speech in a separate thread
        self.stop_listening = False
        self.thread = threading.Thread(target=self.listen_for_voice_input)
        self.thread.start()

    def process_user_input(self):
        global selected_voice_path  # Access the global variable
        # Record the user's speech input
        text = record_text()

        if text is not None:
            # Append the user's input to the conversation history
            self.messages.append({"role": "user", "content": text})
            print(text)

            # Check if the user's input contains variations of queries about the assistant's name or what "ARIA" stands for
            if any(keyword in text.lower() for keyword in ["what's your name", "your name", "who are you"]):
                response = "My name is ARIA, which stands for Artificial Response and Interactive Assistant."
            elif any(keyword in text.lower() for keyword in ["what does aria stand for", "aria stands for"]):
                response = "ARIA stands for Artificial Response and Interactive Assistant."
            else:
                # Get response from ChatGPT for other queries
                response = send_to_chatGPT(self.messages)
            
            print(response)

            # Speak the response
            SpeakText(response)

        elif text is None:
            if selected_voice_path == voices["English (UK)"] or selected_voice_path == voices["English (US)"]:
                SpeakText("Goodbye now.")
            elif selected_voice_path == voices["Spanish (ES)"] or selected_voice_path == voices["Spanish (MX)"]:
                SpeakText("Adiós.")
            self.stop_listening = True



    def listen_for_voice_input(self):
        while not self.stop_listening:
            self.process_user_input()

    def stop_listening(self):
        self.stop_listening = True
        if self.thread is not None:
            self.thread.join()

def SpeakText(command):
    global selected_voice_path  # Access the global variable
    engine = pyttsx3.init()
    if selected_voice_path:
        engine.setProperty('voice', selected_voice_path)
    engine.say(command)
    engine.runAndWait()


def record_text(stop_phrases=["Thanks ARIA", "Gracias ARIA", "Gracias area", "Adios", "Goodbye", "See you", "Bye", "You're dismissed", "That's enough", "Exit", "Quit"]):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.2)
        print("I'm listening")
        audio = r.listen(source)
        MyText = r.recognize_google(audio)
        for phrase in stop_phrases:
            if phrase.lower() in MyText.lower():
                print(f"Stopping listening. Detected stop phrase: {phrase}")
                return None
        return MyText

def send_to_chatGPT(messages, model="gpt-3.5-turbo"):
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = response.choices[0].message.content

    # Check if the response contains the phrase you want to replace
    phrase_to_replace = ["I am a language model called GPT-3", "a virtual assistant", "a language model AI", "an AI chatbot", "Mi nombre es Assistant"]
    replacement_phrase = ["I am a virtual assistant known as ARIA.", "a virtual assistant known as ARIA", "a virtual assistant known as ARIA", "a virtual assistant known as ARIA", "Mi nombre es ARIA"]

    for phrase, replacement in zip(phrase_to_replace, replacement_phrase):
        if phrase in message:
            message = message.replace(phrase, replacement)
        
    messages.append(response.choices[0].message)
    return message

# Define available voices
voices = {
    "English (US)": r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0",
    "English (UK)": r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0",
    "Spanish (ES)": r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0",
    "Spanish (MX)": r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0"
}

def main():
    root = tk.Tk()
    root.title("ARIA: Artificial Response and Interactive Assistant")

    # Path to the folder containing the GIF images
    gif_folder = r"C:\Users\averg\Downloads\ARIA"

    # Create and run the AnimatedGIFViewer
    gif_viewer = AnimatedGIFViewer(root, gif_folder)
    gif_viewer.update_frame()

    # Initialize Tkinter window for voice selection
    voice_window = tk.Toplevel(root)
    voice_window.title("ARIA: Voice Selection")
    voice_window.geometry("300x150")  # Set window size

    # Initialize pyttsx3 engine
    global engine
    engine = pyttsx3.init()

    # Create a frame
    frame = ttk.Frame(voice_window, padding="20")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Create a label
    label = ttk.Label(frame, text="Select Voice:")
    label.grid(row=0, column=0, padx=5, pady=5)

    # Create dropdown menu for voice selection
    selected_voice = tk.StringVar(voice_window)
    selected_voice.set("English (US)")  # Set default voice
    global voice_menu
    voice_menu = ttk.Combobox(frame, textvariable=selected_voice, values=list(voices.keys()), state="readonly")
    voice_menu.grid(row=0, column=1, padx=5, pady=5)

    # Create button to apply selected voice
    apply_button = ttk.Button(frame, text="Apply", command=change_voice)
    apply_button.grid(row=1, column=0, columnspan=2, pady=10)

    root.mainloop()

def change_voice():
    global voices, engine, selected_voice_path
    selected_voice_name = voice_menu.get()
    selected_voice_path = voices[selected_voice_name]
    engine = pyttsx3.init()  # Reinitialize the engine with the new voice
    engine.setProperty('voice', selected_voice_path)
    if selected_voice_name == "Spanish (ES)" or selected_voice_name == "Spanish (MX)":
        engine.say("Español")
    elif selected_voice_name == "English (UK)" or selected_voice_name == "English (US)":
        engine.say("English")
    engine.runAndWait()

if __name__ == "__main__":
    main()
