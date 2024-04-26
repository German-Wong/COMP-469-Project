import tkinter as tk
from tkinter import ttk
import pyttsx3

def change_voice():
    selected_voice = voice_menu.get()
    engine.setProperty('voice', selected_voice)
    engine.say("Voice changed to " + selected_voice)
    engine.runAndWait()

def main():
    # Initialize Tkinter window
    root = tk.Tk()
    root.title("ARIA: Voice Selection")
    root.geometry("300x150")  # Set window size

    # Define available voices
    voices = ["HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0",
              "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0",
              "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0",
              "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0",
              "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0"]

    # Initialize pyttsx3 engine
    global engine
    engine = pyttsx3.init()

    # Create a frame
    frame = ttk.Frame(root, padding="20")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Create a label
    label = ttk.Label(frame, text="Select Voice:")
    label.grid(row=0, column=0, padx=5, pady=5)

    # Create dropdown menu for voice selection
    selected_voice = tk.StringVar(root)
    selected_voice.set(voices[0])  # Set default voice
    global voice_menu
    voice_menu = ttk.Combobox(frame, textvariable=selected_voice, values=voices, state="readonly")
    voice_menu.grid(row=0, column=1, padx=5, pady=5)

    # Create button to apply selected voice
    apply_button = ttk.Button(frame, text="Apply", command=change_voice)
    apply_button.grid(row=1, column=0, columnspan=2, pady=10)

    # Run the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
