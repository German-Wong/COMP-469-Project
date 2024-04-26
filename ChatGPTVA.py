import tkinter as tk
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
        # Record the user's speech input
        text = record_text()

        if text is not None:
            # Append the user's input to the conversation history
            self.messages.append({"role": "user", "content": text})
            print(text)

            # Get response from ChatGPT
            response = send_to_chatGPT(self.messages)
            print(response)

            # Speak the response
            SpeakText(response)

        elif text is None:
            SpeakText("Goodbye now.", lang = "usenglishf")
            self.stop_listening = True

    def listen_for_voice_input(self):
        while not self.stop_listening:
            self.process_user_input()

    def stop_listening(self):
        self.stop_listening = True
        if self.thread is not None:
            self.thread.join()


def SpeakText(command, lang="usenglishf"):
    engine = pyttsx3.init()
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
    engine.say(command)
    engine.runAndWait()

def record_text(stop_phrases=["Thanks ARIA", "Goodbye", "See you", "Bye", "You're dismissed", "That's enough", "Exit", "Quit"]):
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
    messages.append(response.choices[0].message)
    return message

def main():
    root = tk.Tk()
    root.title("ARIA: Artificial Response and Interactive Assistant")



    # Path to the folder containing the GIF images
    gif_folder = r"C:\Users\averg\Downloads\ARIA"

    # Create and run the AnimatedGIFViewer
    gif_viewer = AnimatedGIFViewer(root, gif_folder)
    gif_viewer.update_frame()

    root.mainloop()

if __name__ == "__main__":
    main()
