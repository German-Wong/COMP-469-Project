import speech_recognition as sr
import pyttsx3

# Initialize the recognizer object for speech recognition
r = sr.Recognizer()

def record_text():
    """
    Continuously listens to the microphone and converts spoken words into text.
    Returns:
        str: The text converted from speech.
    """
    while True:  # Infinite loop to handle continuous input
        try:
            # Use the default system microphone as the source for input
            with sr.Microphone() as source2:
                # Adjust the recognizer sensitivity to ignore ambient noise
                r.adjust_for_ambient_noise(source2, duration=0.2)

                # Listen for user's speech
                audio2 = r.listen(source2)

                # Use Google's speech recognition to convert audio to text
                MyText = r.recognize_google(audio2)
                
                return MyText  # Return the recognized text

        except sr.RequestError as e:
            # Handle cases where the recognizer could not reach the service
            print("Could not request results; {0}".format(e))
            
        except sr.UnknownValueError:
            # Handle cases where speech was unintelligible
            print("unknown error occurred")

    return  # Return None if the loop exits due to an error

def output_text(text):
    """
    Appends the provided text to a file.
    Args:
        text (str): The text to write to the file.
    """
    # Open the file in append mode to add text without deleting existing data
    f = open("output.txt", "a")
    f.write(text)  # Write the text to the file
    f.write("\n")  # Move to the next line after writing the text
    f.close()  # Close the file to ensure data is saved
    return

# Main loop to handle speech input and writing to file
while True:
    text = record_text()  # Record and convert speech to text
    output_text(text)  # Output the text to a file

    print("Wrote text")  # Notify that the text has been written to the file
